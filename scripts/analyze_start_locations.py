"""Hotel-gap calendar and complete-loop comparison from every known hotel."""
import argparse
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from collections import Counter
import gzip,json
from statistics import median
from simulate_tacking import Engine,ROOT,DATA,day_reachable,SETTINGS

OUT=DATA/'start-analysis'


def evaluate(nodes,hotel_indices,days,origin,start):
    n=len(nodes)-1;states={0:[]}
    for day in range(start,len(days)):
        nxt=dict(states)
        for progress,history in states.items():
            i=(origin+progress)%n
            for dest,trip in days[day].get(i,{}).items():
                advanced=progress+dest-i
                if advanced>n:continue
                candidate=history+[dict(day=day,**trip)]
                if advanced not in nxt or len(candidate)<len(nxt[advanced]):nxt[advanced]=candidate
        states=nxt
        if n in states:return n,states[n],day
    best=max(states)
    return best,states[best],len(days)-1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--years',nargs='+',type=int,default=[2022,2023,2024,2025]);args=parser.parse_args();OUT.mkdir(exist_ok=True)
    zone=ZoneInfo('Europe/Rome')
    for year in args.years:
        for model in ['base','cautious']:
            engine=Engine(model,year);ccw=[l['start'] for l in engine.plan['legs']]+['poetto']
            hotel_ids={k for k,s in engine.plan['spots'].items() if s.get('hotel')}|set(json.loads((DATA/'hotel-network.json').read_text())['additional_hotels'])
            for direction,nodes in [('ccw',ccw),('cw',ccw[::-1])]:
                n=len(nodes)-1;ring=nodes[:-1];doubled=ring+ring+[ring[0]]
                hotels={i for i,site in enumerate(doubled) if site in hotel_ids};origins=sorted(i for i in hotels if i<n)
                first=datetime(year,8,1,tzinfo=zone);days=[];name=f'{year}-{model}-{direction}'
                calendar_path=OUT/f'{name}-calendar.json.gz'
                if calendar_path.exists():
                    raw=json.loads(gzip.decompress(calendar_path.read_bytes()));assert raw['settings']==SETTINGS
                    days=[{int(k):{int(d):t for d,t in v.items()} for k,v in day.items()} for day in raw['days']]
                else:
                    for day in range(92):
                        date=first+timedelta(days=day);opening=date.replace(hour=9).timestamp();closing=date.replace(hour=17).timestamp();cache={}
                        options={i:day_reachable(i,doubled,hotels,opening,closing,engine,cache) for i in origins}
                        days.append(options)
                        if day%15==0:print(name,date.date(),flush=True)
                    calendar_path.write_bytes(gzip.compress(json.dumps(dict(settings=SETTINGS,nodes=nodes,days=days),ensure_ascii=False).encode(),mtime=0))
                gaps=[]
                for i in origins:
                    j=next(k for k in sorted(hotels) if k>i)
                    dates=[(first+timedelta(days=d)).date().isoformat() for d,day in enumerate(days) if j in day[i]]
                    km=sum(engine.route(doubled[k],doubled[k+1])[2] for k in range(i,j))
                    gaps.append(dict(start=ring[i],end=doubled[j],route_km=km,feasible_dates=dates))
                runs=[];best_trips={}
                for i in origins:
                    candidates=[]
                    for start in range(61):
                        dest,history,last=evaluate(nodes,origins,days,i,start)
                        finish=(first+timedelta(days=last)).date().isoformat()
                        first_ride=(first+timedelta(days=history[0]['day'])).date().isoformat() if history else None
                        record=dict(start_hotel=ring[i],start=(first+timedelta(days=start)).date().isoformat(),completed=dest==n,
                            completed_km=round(sum(t['route_km'] for t in history),3),last_hotel=ring[(i+dest)%n],
                            finish=finish,riding_days=len(history),waiting_days=last-start+1-len(history),first_ride=first_ride)
                        runs.append(record);candidates.append((record,history))
                    # Keep a reviewable representative: fastest completed trip, else furthest then earliest start.
                    completed=[c for c in candidates if c[0]['completed']]
                    record,history=min(completed,key=lambda c:c[0]['riding_days']+c[0]['waiting_days']) if completed else max(candidates,key=lambda c:c[0]['completed_km'])
                    best_trips[ring[i]]=dict(summary=record,travel=[dict(date=(first+timedelta(days=t['day'])).date().isoformat(),**t) for t in history])
                payload=dict(year=year,model=model,direction=direction,gaps=gaps,runs=runs,best_trips=best_trips)
                (OUT/f'{name}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
                print('DONE',name,'complete',sum(r['completed'] for r in runs),'max',max(r['completed_km'] for r in runs),'zero gaps',[(g['start'],g['end']) for g in gaps if not g['feasible_dates']],flush=True)

if __name__=='__main__':main()
