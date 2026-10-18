"""Offline hotel-to-hotel reachability with land waits and historical hindsight."""
from bisect import bisect_left
from datetime import datetime, timedelta
import json
import argparse
from zoneinfo import ZoneInfo
from simulate_wind import ROOT, DATA, load_weather, route_actions, attempt


def reachable(start, paths, distances, hotels, opening, closing, cap, pause):
    """Earliest arrival dominates: later departures remain possible by waiting on land."""
    now=opening; km=0; travel=[]; out={}
    for edge in range(start,len(paths)):
        km+=distances[edge]
        if km>cap+1e-8:break
        departures, duration=paths[edge]
        k=bisect_left(departures,now)
        if k==len(departures):break
        dep=departures[k];arr=dep+duration
        if arr>closing:break
        travel=travel+[dict(edge=edge,departure=dep,arrival=arr,land_minutes=(dep-now)/60)]
        if edge+1 in hotels:
            out[edge+1]=dict(km=km,legs=travel,arrival=arr)
        now=arr+pause
    return out


def solve(start_day, days, terminal):
    # All overnight positions retained; a greedy farthest-stop strategy is not assumed.
    states={0:[]}
    for d in range(start_day,len(days)):
        nxt=dict(states)
        for origin,history in states.items():
            for dest,trip in days[d].get(origin,{}).items():
                candidate=history+[dict(day=d,start=origin,end=dest,**trip)]
                if dest not in nxt or len(candidate)<len(nxt[dest]):nxt[dest]=candidate
        states=nxt
        if terminal in states:return terminal,states[terminal],d
    dest=max(states)
    return dest,states[dest],len(days)-1


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--all-directions', action='store_true', help='Run the 360-degree wind scenario')
    args=parser.parse_args()
    config_name='simulation-config-360.json' if args.all_directions else 'simulation-config.json'
    output_name='adaptive-results-360.json' if args.all_directions else 'adaptive-results.json'
    cfg=json.loads((DATA/config_name).read_text()); zone=ZoneInfo(cfg['local_timezone'])
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    sampling=json.loads((DATA/'sampling.json').read_text())
    extra=json.loads((DATA/'hotel-network.json').read_text())
    hotel_ids={s for s,x in plan['spots'].items() if x.get('hotel')}|set(extra['additional_hotels'])
    ccw=[x['start'] for x in plan['legs']]+['poetto']
    results=[]; diagnostics=[]; leg_windows=[]
    for year in cfg['years']:
        base,weather=load_weather(year);first=datetime(year,9,1,tzinfo=zone)
        for direction,nodes in [('ccw',ccw),('cw',ccw[::-1])]:
            actions=[route_actions(dict(path=[a,b],stops=[a,b]),sampling,plan,cfg) for a,b in zip(nodes,nodes[1:])]
            distances=[sum(x['seconds'] for x in seq)*cfg['speed_kmh']/3600 for seq in actions]
            hotels={i for i,s in enumerate(nodes) if s in hotel_ids}
            tables={cap:[] for cap in [50,75,125]}
            for day in range(61):
                date=first+timedelta(days=day)
                opening=date.replace(hour=9).timestamp();closing=date.replace(hour=17).timestamp()
                paths=[]
                for seq in actions:
                    duration=sum(x['seconds'] for x in seq);departures=[]
                    for offset in range(0,8*3600+1,300):
                        dep=opening+offset
                        if dep+duration>closing:break
                        arrival,_=attempt(seq,dep,base,weather,cfg)
                        if arrival is not None:departures.append(dep)
                    paths.append((departures,duration))
                    if departures:leg_windows.append(dict(year=year,direction=direction,date=date.date().isoformat(),start=nodes[len(paths)-1],end=nodes[len(paths)],windows=len(departures)))
                for cap,days in tables.items():
                    days.append({i:reachable(i,paths,distances,hotels,opening,closing,min(cap,cfg['max_riding_hours']*cfg['speed_kmh']),cfg['pause_minutes']*60) for i in sorted(hotels) if i<len(actions)})
            for cap,days in tables.items():
                for start in range(30):
                    dest,history,last=solve(start,days,len(nodes)-1)
                    for trip in history:
                        trip['date']=(first+timedelta(days=trip['day'])).date().isoformat()
                        trip['from']=nodes[trip['start']];trip['to']=nodes[trip['end']]
                        for leg in trip['legs']:
                            leg['from']=nodes[leg['edge']];leg['to']=nodes[leg['edge']+1]
                    results.append(dict(year=year,direction=direction,daily_cap_km=cap,start=(first+timedelta(days=start)).date().isoformat(),completed=dest==len(nodes)-1,completed_km=round(sum(distances[:dest]),3),last_hotel=nodes[dest],riding_days=len(history),waiting_days=last-start+1-len(history),travel=history))
                diagnostics.append(dict(year=year,direction=direction,daily_cap_km=cap,first_departure_days=[(first+timedelta(days=i)).date().isoformat() for i,day in enumerate(days) if day[0]]))
            print(year,direction,'done',flush=True)
    output=dict(assumptions=dict(departure_grid_minutes=5,day_local='09:00–17:00',minimum_land_pause_minutes=25,daily_caps_km=[50,75,125],overnight_hotel_ids=sorted(hotel_ids),strategy='All reachable hotel states; earliest completion, otherwise maximum progress by 31 October; fewest riding days as tie break'),runs=results,diagnostics=diagnostics,leg_windows=leg_windows)
    output['config']=cfg
    (DATA/output_name).write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    for cap in [50,75,125]:
        for direction in ['ccw','cw']:
            rows=[r for r in results if r['daily_cap_km']==cap and r['direction']==direction]
            print(cap,direction,'complete',sum(r['completed'] for r in rows),'departed',sum(r['riding_days']>0 for r in rows),'km',min(r['completed_km'] for r in rows),max(r['completed_km'] for r in rows))


if __name__=='__main__':main()
