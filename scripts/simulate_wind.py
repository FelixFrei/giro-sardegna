"""Historical fixed-itinerary simulation. Offline, retrospective perfect-weather knowledge."""
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import gzip
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/phase2'


def components(speed,direction):
    if speed is None or direction is None:return None
    angle=math.radians(direction)
    return -speed*math.sin(angle),-speed*math.cos(angle)


def compatible(u,v,bearing,config):
    speed=math.hypot(u,v)
    if speed<config['wind_min_kn']-1e-9:return False,'too_light'
    if speed>config['wind_max_kn']+1e-9:return False,'too_strong'
    tail=u*math.sin(math.radians(bearing))+v*math.cos(math.radians(bearing))
    angle=math.degrees(math.acos(max(-1,min(1,-tail/speed))))
    if not config['wind_angle_min_deg']-1e-9 <= angle <= config['wind_angle_max_deg']+1e-9:return False,'headwind'
    return True,'ok'


def load_weather(year):
    weather={};base=None
    for manifest in sorted((DATA/'raw').glob(f'ifs-{year}-*.request.json')):
        m=json.loads(manifest.read_text());name=manifest.name.replace('.request.json','.json.gz')
        rows=json.loads(gzip.decompress((manifest.parent/name).read_bytes()))
        rows=rows if isinstance(rows,list) else [rows]
        for ident,row in zip(m['point_ids'],rows):
            h=row['hourly'];base=h['time'][0]
            weather[ident]=[components(s,d) for s,d in zip(h['wind_speed_10m'],h['wind_direction_10m'])]
    return base,weather


def route_actions(row,sampling,plan,cfg):
    grouped=defaultdict(list)
    for piece in sampling['segments']:grouped[(piece['start'],piece['end'])].append(piece)
    lengths={(x['start'],x['end']):x['km'] for x in plan['legs']}
    actions=[]; ride=0
    for a,b in zip(row['path'],row['path'][1:]):
        reverse=(a,b) not in grouped;key=(b,a) if reverse else (a,b)
        pieces=grouped[key][::-1] if reverse else grouped[key]
        ratio=lengths[key]/sum(x['km'] for x in pieces)
        for piece in pieces:
            seconds=piece['km']*ratio/cfg['speed_kmh']*3600;ride+=seconds
            actions.append(dict(seconds=seconds,weather_id=piece['weather_id'],bearing=(piece['bearing_ccw']+(180 if reverse else 0))%360))
        if b in row['stops'][1:-1]:actions.append(dict(seconds=cfg['pause_minutes']*60))
    assert ride<=cfg['max_riding_hours']*3600+1e-6
    return actions


def attempt(actions,departure,base,weather,cfg):
    now=departure
    for action in actions:
        duration=action['seconds']
        if 'weather_id' in action:
            values=weather[action['weather_id']]
            checks=max(1,math.ceil(duration/(cfg['weather_check_step_minutes']*60)))
            for sample in range(checks+1):
                index=(now+duration*sample/checks-base)/3600;i=math.floor(index);fraction=index-i
                if i<0 or i+1>=len(values) or values[i] is None or values[i+1] is None:return None,'missing'
                u=values[i][0]*(1-fraction)+values[i+1][0]*fraction
                v=values[i][1]*(1-fraction)+values[i+1][1]*fraction
                ok,why=compatible(u,v,action['bearing'],cfg)
                if not ok:return None,why
        now+=duration
    return now,'ok'


def main():
    cfg=json.loads((DATA/'simulation-config.json').read_text())
    assert cfg['gust_limit_kn'] is None, 'A gust limit requires explicit gust filtering; not implemented in this scenario.'
    sampling=json.loads((DATA/'sampling.json').read_text());plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    variants=json.loads((ROOT/'data/phase1/variants.json').read_text());zone=ZoneInfo(cfg['local_timezone'])
    actions={name:[route_actions(row,sampling,plan,cfg) for row in rows] for name,rows in variants.items()}
    all_runs=[]; feasibility=[]; availability=[]
    for year in cfg['years']:
        base,weather=load_weather(year)
        assert set(weather)=={p['id'] for p in sampling['points']}
        first=datetime(year,9,1,tzinfo=zone)
        # Length-weighted local wind compatibility, not a trip success probability.
        for month in [9,10]:
            counters=Counter();den=0
            for index in range(1464):
                local=datetime.fromtimestamp(base+index*3600,zone)
                if local.month!=month or not cfg['departure_start_hour']<=local.hour<cfg['arrival_limit_hour']:continue
                for piece in sampling['segments']:
                    uv=weather[piece['weather_id']][index]
                    if uv is None:continue
                    den+=piece['km']
                    for direction,offset in [('ccw',0),('cw',180)]:
                        ok,_=compatible(*uv,(piece['bearing_ccw']+offset)%360,cfg)
                        if ok:counters[direction]+=piece['km']
            availability.append(dict(year=year,month=month,ccw_percent=100*counters['ccw']/den,cw_percent=100*counters['cw']/den))
        for name,rows in variants.items():
            schedules=[]
            for number,act in enumerate(actions[name]):
                days=[];reasons=Counter()
                for day in range(61):
                    date=first+timedelta(days=day);accepted=None
                    deadline=date.replace(hour=cfg['arrival_limit_hour']).timestamp()
                    for minutes in range(cfg['departure_start_hour']*60,cfg['departure_last_hour']*60+1,cfg['departure_step_minutes']):
                        departure=date.replace(hour=minutes//60,minute=minutes%60).timestamp()
                        if departure+sum(x['seconds'] for x in act)>deadline:continue
                        arrival,reason=attempt(act,departure,base,weather,cfg)
                        if arrival is not None:
                            accepted=dict(departure=datetime.fromtimestamp(departure,zone).isoformat(),arrival=datetime.fromtimestamp(arrival,zone).isoformat());break
                        reasons[reason]+=1
                    days.append(accepted)
                schedules.append(days)
                feasibility.append(dict(year=year,variant=name,stage=number+1,start=rows[number]['stops'][0],end=rows[number]['stops'][-1],
                    feasible_september=sum(x is not None for x in days[:30]),feasible_october=sum(x is not None for x in days[30:]),
                    first_failure_counts=dict(reasons)))
            for start in range(30):
                completed=0;travel=[];wait=0;finish=None
                for day in range(start,61):
                    opportunity=schedules[completed][day]
                    if opportunity:
                        travel.append(dict(stage=completed+1,**opportunity));completed+=1
                        if completed==len(rows):finish=opportunity['arrival'];break
                    else:wait+=1
                all_runs.append(dict(year=year,variant=name,start_date=f'{year}-09-{start+1:02d}',completed=finish is not None,
                    finish=finish,completed_in_september=bool(finish and datetime.fromisoformat(finish).month==9),
                    riding_days=completed,waiting_days=wait,completed_km=sum(x['km'] for x in rows[:completed]),
                    next_stage=None if finish else completed+1,travel=travel))
            print(year,name,'runs computed',flush=True)
    result=dict(config=cfg,runs=all_runs,stage_feasibility=feasibility,local_wind_availability=availability)
    (DATA/'simulation-results.json').write_text(json.dumps(result,indent=2)+'\n')
    for name in variants:
        runs=[r for r in all_runs if r['variant']==name]
        print(name,'completed',sum(r['completed'] for r in runs),'/',len(runs),'max stages',max(r['riding_days'] for r in runs))


if __name__=='__main__':main()
