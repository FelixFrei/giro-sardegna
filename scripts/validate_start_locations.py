"""Validate the rotated circuits against Poetto reference and replay best trips."""
from datetime import datetime,date,timedelta
from zoneinfo import ZoneInfo
import json,argparse,hashlib
from simulate_tacking import Engine,DATA
from analyze_start_locations import OUT


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expanded',action='store_true');args=parser.parse_args()
    out=DATA/('start-analysis-expanded' if args.expanded else 'start-analysis')
    network=DATA/('hotel-network-expanded.json' if args.expanded else 'hotel-network.json')
    extra=set(json.loads(network.read_text())['additional_hotels'])
    count=0;replayed=0;best_count=0;zone=ZoneInfo('Europe/Rome')
    for year in range(2022,2026):
        reference=json.loads((DATA/f'tacking-{year}.json').read_text())['runs']
        for model in ['base','cautious']:
            engine=Engine(model,year);cache={}
            ccw=[l['start'] for l in engine.plan['legs']]
            for direction in ['ccw','cw']:
                data=json.loads((out/f'{year}-{model}-{direction}.json').read_text())
                hotels={k for k,v in engine.plan['spots'].items() if v.get('hotel')}|extra
                size=len(hotels)
                if args.expanded:
                    assert data['network_sha256']==hashlib.sha256(network.read_bytes()).hexdigest()
                    baseline=json.loads((OUT/f'{year}-{model}-{direction}.json').read_text())
                    prior={(r['start_hotel'],r['start']):r for r in baseline['runs']}
                assert len(data['runs'])==size*61 and len(data['gaps'])==size
                keys={(r['start_hotel'],r['start']) for r in data['runs']};assert len(keys)==size*61
                assert keys=={(h,(date(year,8,1)+timedelta(days=i)).isoformat()) for h in hotels for i in range(61)}
                old={r['start']:r for r in reference if r['scenario']==model and r['direction']==direction}
                ring=ccw if direction=='ccw' else ['poetto']+ccw[:0:-1]
                for r in data['runs']:
                    assert 0<=r['completed_km']<=890.775
                    assert r['riding_days']+r['waiting_days']==(date.fromisoformat(r['finish'])-date.fromisoformat(r['start'])).days+1
                    if r['completed']:assert abs(r['completed_km']-engine.plan['total_km'])<.01 and r['last_hotel']==r['start_hotel']
                    if args.expanded and (r['start_hotel'],r['start']) in prior:
                        prev_run=prior[r['start_hotel'],r['start']]
                        assert r['completed_km']>=prev_run['completed_km']-.001
                        if prev_run['completed']:assert r['completed'] and r['finish']<=prev_run['finish']
                    if not args.expanded and r['start_hotel']=='poetto':
                        for field in ['completed','completed_km','last_hotel']:
                            assert r[field]==old[r['start']][field],(year,model,direction,r['start'],field)
                    count+=1
                selected=list(data['best_trips'].items())
                examples_path=out/'examples.json'
                if args.expanded and examples_path.exists():
                    for example in json.loads(examples_path.read_text()):
                        r=example['summary']
                        if (r['year'],r['model'],r['direction'])==(year,model,direction):
                            travel=[dict(t,date=datetime.fromtimestamp(t['legs'][0]['departure'],zone).date().isoformat()) for t in example['travel']]
                            selected.append((r['start_hotel'],dict(summary=r,travel=travel)))
                for site,best in selected:
                    r=best['summary'];progress=0;index=ring.index(site);km=0;current=site;previous_date=None
                    for day in best['travel']:
                        assert current in hotels
                        assert previous_date is None or previous_date<day['date']
                        water=0;prev=None
                        for leg in day['legs']:
                            depart=datetime.fromtimestamp(leg['departure'],zone);arrive=datetime.fromtimestamp(leg['arrival'],zone)
                            assert depart.date().isoformat()==day['date']==arrive.date().isoformat()
                            assert depart.hour>=9 and arrive<=arrive.replace(hour=17,minute=0,second=0)
                            assert leg['start']==current
                            assert leg['end']==ring[(index+progress+1)%len(ring)]
                            progress+=1;current=leg['end'];assert progress<=len(ring)
                            key=leg['start'],leg['end'],leg['departure']
                            if key not in cache:
                                closing=datetime.fromtimestamp(leg['departure'],zone).replace(hour=17,minute=0,second=0).timestamp()
                                actual,why=engine.voyage(*key,closing)
                                assert why=='ok';cache[key]=actual;replayed+=1
                            assert abs(cache[key]['arrival']-leg['arrival'])<1e-5
                            assert abs(cache[key]['water_seconds']-leg['water_seconds'])<1e-5
                            if prev is not None:assert leg['departure']-prev>=1500-1e-6
                            prev=leg['arrival'];water+=leg['water_seconds']
                        assert current in hotels
                        assert water<=18000+1e-6
                        assert abs(water/3600-day['water_hours'])<1e-5
                        km+=day['route_km'];previous_date=day['date']
                    assert abs(km-r['completed_km'])<.001 and current==r['last_hotel']
                    assert r['completed']==(progress==len(ring));best_count+=1
            print('verified',year,model,flush=True)
    assert count==size*61*16
    summary=dict(runs=count,best_routes_verified=best_count,unique_selected_passages_replayed=replayed,
                 checks=[('All 20496 baseline runs matched or improved' if args.expanded else 'All 976 Poetto references matched'),'No skipped gap or overshoot in rotated circuits','Representative full route reconstruction','Wind, coast and five-hour water budget replay'])
    (out/'validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)

if __name__=='__main__':main()
