"""Time-dependent wingfoil polar, local water-only tacks and hotel-state planning.

Historical hindsight, approximate Euler integration. Not a navigation track.
"""
import argparse
from collections import Counter,defaultdict
from datetime import datetime,timedelta
import json
import math
from zoneinfo import ZoneInfo
from shapely.geometry import shape,LineString
from shapely.ops import transform,unary_union
from shapely.prepared import prep
from pyproj import Transformer
from simulate_wind import ROOT,DATA,load_weather

FORWARD=Transformer.from_crs(4326,32632,always_xy=True).transform
BACK=Transformer.from_crs(32632,4326,always_xy=True).transform
SETTINGS=dict(wind_min_kn=12,wind_max_kn=25,water_hours=5,land_pause_minutes=25,
    departure_grid_minutes=5,integration_seconds=120,max_progress_step_m=500,min_coastal_step_m=25,
    land_buffer_m=25,day_local='09:00–17:00',start_dates='08-01 through 09-30',last_day='10-31',
    model_note='Local triangular tacks, both orders tested; shorten up to 25 m progress near land. Wind frozen for geometry over <=120 s; range checked along actual strokes. No global offshore rerouting.')


def angle_delta(a,b):return (a-b+180)%360-180


def polar(wind,angle,scenario):
    """Return progress speed, physical-distance factor, manoeuvre factor, turn angle/mode."""
    band=0 if wind<15 else 1 if wind<20 else 2
    cautious=scenario=='cautious';scale=.85 if cautious else 1
    theta=([60,55,55][band]+(5 if cautious else 0))
    a=abs(angle)
    if a<theta-1e-9:
        factor=math.cos(math.radians(a))/math.cos(math.radians(theta))
        efficiency=.80 if cautious else .85
        speed=[16,20,18][band]*scale
        return speed*efficiency/factor,factor,efficiency,theta,'upwind'
    if a>145+1e-9:
        factor=math.cos(math.radians(180-a))/math.cos(math.radians(35))
        speed=[18,22,20][band]*scale
        return speed*.90/factor,factor,.90,35,'downwind'
    anchors=[(theta,[16,20,18][band]),(70,[16,20,18][band]),(90,[20,25,23][band]),
             (120,[22,26,24][band]),(145,[18,22,20][band])]
    for (x,v),(y,w) in zip(anchors,anchors[1:]):
        if a<=y+1e-9:
            speed=(v+(w-v)*(a-x)/(y-x))*scale
            return speed,1,1,0,'direct'
    raise AssertionError(a)


def tack_paths(start,end,wind_relative,theta,mode):
    """Two possible orders of the symmetric strokes, in projected metres."""
    if mode=='direct':return [[start,end]]
    dx,dy=end[0]-start[0],end[1]-start[1];distance=math.hypot(dx,dy)
    if distance==0:return [[start,end]]
    ex,ey=dx/distance,dy/distance
    centre=wind_relative+(180 if mode=='downwind' else 0)
    r1,r2=map(math.radians,[centre+theta,centre-theta])
    c1,s1,c2,s2=math.cos(r1),math.sin(r1),math.cos(r2),math.sin(r2)
    determinant=c1*s2-c2*s1
    l1=distance*s2/determinant;l2=-distance*s1/determinant
    assert l1>=-1e-5 and l2>=-1e-5
    corners=[(start[0]+l1*(ex*c1+ey*s1),start[1]+l1*(ey*c1-ex*s1)),
             (start[0]+l2*(ex*c2+ey*s2),start[1]+l2*(ey*c2-ex*s2))]
    return [[start,c,end] for c in corners]


class Engine:
    def __init__(self,scenario,year,step_seconds=120):
        self.scenario=scenario;self.base,self.weather=load_weather(year,august=True)
        self.step_seconds=step_seconds;self.failures=Counter()
        self.plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
        self.sampling=json.loads((DATA/'sampling.json').read_text())
        land=json.loads((ROOT/'data/phase1/land.geojson').read_text())
        self.barrier=prep(unary_union([transform(FORWARD,shape(f['geometry'])) for f in land['features']]).buffer(25))
        self.points=[(p['id'],FORWARD(p['longitude'],p['latitude'])) for p in self.sampling['points']]
        self.nearest_cache={}
        self.pieces=defaultdict(list)
        for p in self.sampling['segments']:
            a,b=[FORWARD(*xy[:2]) for xy in p['coordinates']]
            self.pieces[(p['start'],p['end'])].append(dict(a=a,b=b,bearing=p['bearing_ccw'],weather_id=p['weather_id']))
        self.distances={(l['start'],l['end']):l['km'] for l in self.plan['legs']}
        self.route_cache={}

    def wind(self,ident,t):
        index=(t-self.base)/3600;i=int(math.floor(index));f=index-i
        values=self.weather[ident]
        if i<0 or i+1>=len(values) or values[i] is None or values[i+1] is None:return None
        u=values[i][0]*(1-f)+values[i+1][0]*f;v=values[i][1]*(1-f)+values[i+1][1]*f
        speed=math.hypot(u,v)
        if speed<12-1e-9 or speed>25+1e-9:return None
        return speed,math.degrees(math.atan2(-u,-v))%360

    def nearest(self,xy):
        key=(round(xy[0]/1000),round(xy[1]/1000))
        if key not in self.nearest_cache:
            x,y=key[0]*1000,key[1]*1000
            self.nearest_cache[key]=min(self.points,key=lambda p:(p[1][0]-x)**2+(p[1][1]-y)**2)[0]
        return self.nearest_cache[key]

    def route(self,a,b):
        if (a,b) in self.route_cache:return self.route_cache[a,b]
        rev=(a,b) not in self.pieces;key=(b,a) if rev else (a,b)
        pieces=self.pieces[key]
        if rev:pieces=[dict(a=p['b'],b=p['a'],bearing=(p['bearing']+180)%360,weather_id=p['weather_id']) for p in pieces[::-1]]
        geom=sum(math.dist(p['a'],p['b']) for p in pieces)
        ratio=self.distances[key]*1000/geom
        self.route_cache[a,b]=(pieces,ratio,self.distances[key])
        return self.route_cache[a,b]

    def voyage(self,a,b,departure,closing,trace=False):
        pieces,ratio,route_km=self.route(a,b);now=departure;physical=0;upwind=0;downwind=0;loss=0;tracks=[]
        for p in pieces:
            length=math.dist(p['a'],p['b']);done=0
            while done<length-1e-6:
                start=tuple(p['a'][k]+(p['b'][k]-p['a'][k])*done/length for k in [0,1])
                wind=self.wind(self.nearest(start),now)
                if wind is None:return None,'wind'
                relative=angle_delta(wind[1],p['bearing'])
                speed,factor,efficiency,theta,mode=polar(wind[0],relative,self.scenario)
                progress=min(length-done,500,speed/3.6*self.step_seconds/ratio)
                # The planned connector allowance scales both distance and time.
                while True:
                    end=tuple(p['a'][k]+(p['b'][k]-p['a'][k])*(done+progress)/length for k in [0,1])
                    paths=tack_paths(start,end,relative,theta,mode)
                    path=next((v for v in paths if not self.barrier.intersects(LineString(v))),None)
                    if path is not None:break
                    if progress<=25+1e-9:return None,'coast'
                    progress=max(25,progress/2)
                duration=progress*ratio/(speed/3.6)
                if now+duration>closing+1e-6 or now+duration-departure>5*3600+1e-6:return None,'time'
                # Wind strength sampled at start, midpoint and end of each actual stroke.
                lengths=[math.dist(c,d) for c,d in zip(path,path[1:])];total=sum(lengths);elapsed=0
                for c,d,leg_m in zip(path,path[1:],lengths):
                    for fraction in [0,.5,1]:
                        xy=tuple(c[k]+(d[k]-c[k])*fraction for k in [0,1])
                        t=now+duration*(elapsed+leg_m*fraction)/total
                        if self.wind(self.nearest(xy),t) is None:return None,'wind'
                    elapsed+=leg_m
                if trace:tracks.append(dict(coordinates=[BACK(*xy) for xy in path],departure=now,arrival=now+duration,mode=mode))
                physical+=progress*ratio*factor/1000
                if mode=='upwind':upwind+=duration
                if mode=='downwind':downwind+=duration
                loss+=duration*(1-efficiency)
                now+=duration;done+=progress
        result=dict(departure=departure,arrival=now,water_seconds=now-departure,physical_km=physical,
                    route_km=route_km,upwind_seconds=upwind,downwind_seconds=downwind,manoeuvre_seconds=loss)
        if trace:result['tracks']=tracks
        return result,'ok'


def pareto(labels):
    best=float('inf');out=[]
    for row in sorted(labels,key=lambda x:(x['ready'],x['water'])):
        if row['water']<best-1e-6:out.append(row);best=row['water']
    return out


def day_reachable(origin,nodes,hotels,opening,closing,engine,cache):
    labels=[dict(ready=opening,water=0,legs=[])];out={};route_km=0
    for edge in range(origin,len(nodes)-1):
        a,b=nodes[edge:edge+2];route_km+=engine.route(a,b)[2]
        if route_km>130+1e-6:break # fastest polar speed 26 km/h × 5 h
        next_labels=[]
        # For a fixed departure, the least-water eligible label dominates.
        ordered=sorted(labels,key=lambda x:x['ready']);idx=0;best=None
        for dep in range(int(opening),int(closing),300):
            while idx<len(ordered) and ordered[idx]['ready']<=dep+1e-6:
                if best is None or ordered[idx]['water']<best['water']:best=ordered[idx]
                idx+=1
            if best is None:continue
            key=a,b,dep
            if key not in cache:
                cache[key],why=engine.voyage(a,b,dep,closing)
                engine.failures[why]+=1
            trip=cache[key]
            if trip is None or best['water']+trip['water_seconds']>18000+1e-6:continue
            record=dict(**trip,start=a,end=b,land_wait_minutes=(dep-best['ready'])/60)
            next_labels.append(dict(ready=trip['arrival']+1500,water=best['water']+trip['water_seconds'],legs=best['legs']+[record]))
        labels=pareto(next_labels)
        if not labels:break
        if edge+1 in hotels:
            best=min(labels,key=lambda x:x['ready'])
            out[edge+1]=dict(route_km=route_km,water_hours=best['water']/3600,
                physical_km=sum(l['physical_km'] for l in best['legs']),legs=best['legs'])
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--years',nargs='+',type=int,default=[2022,2023,2024,2025]);args=parser.parse_args()
    all_runs=[];diagnostics=[];zone=ZoneInfo('Europe/Rome')
    for year in args.years:
        for scenario in ['base','cautious']:
            engine=Engine(scenario,year)
            ccw=[l['start'] for l in engine.plan['legs']]+['poetto']
            hotel_ids={k for k,s in engine.plan['spots'].items() if s.get('hotel')}|set(json.loads((DATA/'hotel-network.json').read_text())['additional_hotels'])
            for direction,nodes in [('ccw',ccw),('cw',ccw[::-1])]:
                first=datetime(year,8,1,tzinfo=zone);hotels={i for i,n in enumerate(nodes) if n in hotel_ids}
                states={};finished={};engine.failures.clear()
                for day in range(92):
                    if day<61:states[day]={0:[]}
                    date=first+timedelta(days=day);opening=date.replace(hour=9).timestamp();closing=date.replace(hour=17).timestamp()
                    origins={i for possibilities in states.values() for i in possibilities};cache={}
                    options={i:day_reachable(i,nodes,hotels,opening,closing,engine,cache) for i in sorted(origins)}
                    for start,possibilities in list(states.items()):
                        nxt=dict(possibilities)
                        for origin,history in possibilities.items():
                            for dest,trip in options[origin].items():
                                candidate=history+[dict(date=date.date().isoformat(),start=nodes[origin],end=nodes[dest],**trip)]
                                if dest not in nxt or len(candidate)<len(nxt[dest]):nxt[dest]=candidate
                        if len(nodes)-1 in nxt:
                            finished[start]=(len(nodes)-1,nxt[len(nodes)-1],day);del states[start]
                        else:states[start]=nxt
                    if day%15==0:print(year,scenario,direction,date.date(),'hotels',len(origins),flush=True)
                for start,possibilities in states.items():
                    dest=max(possibilities);finished[start]=(dest,possibilities[dest],91)
                for start,(dest,history,last) in sorted(finished.items()):
                    all_runs.append(dict(year=year,scenario=scenario,direction=direction,start=(first+timedelta(days=start)).date().isoformat(),
                        completed=dest==len(nodes)-1,last_hotel=nodes[dest],completed_km=round(sum(t['route_km'] for t in history),3),
                        riding_days=len(history),waiting_days=last-start+1-len(history),water_hours=sum(t['water_hours'] for t in history),
                        physical_km=sum(t['physical_km'] for t in history),travel=history))
                diagnostics.append(dict(year=year,scenario=scenario,direction=direction,attempts=dict(engine.failures)))
                print('DONE',year,scenario,direction,max(r['completed_km'] for r in all_runs if r['year']==year and r['scenario']==scenario and r['direction']==direction),flush=True)
            (DATA/f'tacking-{year}.json').write_text(json.dumps(dict(settings=SETTINGS,runs=[r for r in all_runs if r['year']==year],diagnostics=[d for d in diagnostics if d['year']==year]),ensure_ascii=False,indent=2)+'\n')
    (DATA/'tacking-model.json').write_text(json.dumps(dict(settings=SETTINGS,
        wind_bands_kn=['12 <= wind < 15','15 <= wind < 20','20 <= wind <= 25'],
        base=dict(upwind_angles_deg=[60,55,55],upwind_speeds_kmh=[16,20,18],
                  reaching_angles_deg=[70,90,120,145],reaching_speeds_kmh=[[16,20,18],[20,25,23],[22,26,24],[18,22,20]],
                  upwind_efficiency=.85,downwind_efficiency=.90,downwind_heading_deg=145),
        cautious=dict(upwind_angle_increment_deg=5,all_speeds_multiplier=.85,upwind_efficiency=.80,downwind_efficiency=.90),
        assumptions_document='docs/21-annahmen-aufkreuzen.md'),ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
