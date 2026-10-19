"""Validate the rotated circuits against Poetto reference and replay best trips."""
from datetime import datetime,date
from zoneinfo import ZoneInfo
import json
from simulate_tacking import Engine,DATA
from analyze_start_locations import OUT


def main():
    count=0;replayed=0;best_count=0;zone=ZoneInfo('Europe/Rome')
    for year in range(2022,2026):
        reference=json.loads((DATA/f'tacking-{year}.json').read_text())['runs']
        for model in ['base','cautious']:
            engine=Engine(model,year);cache={}
            ccw=[l['start'] for l in engine.plan['legs']]
            for direction in ['ccw','cw']:
                data=json.loads((OUT/f'{year}-{model}-{direction}.json').read_text())
                assert len(data['runs'])==21*61 and len(data['gaps'])==21
                keys={(r['start_hotel'],r['start']) for r in data['runs']};assert len(keys)==21*61
                old={r['start']:r for r in reference if r['scenario']==model and r['direction']==direction}
                ring=ccw if direction=='ccw' else ['poetto']+ccw[:0:-1]
                for r in data['runs']:
                    assert 0<=r['completed_km']<=890.775
                    assert r['riding_days']+r['waiting_days']==(date.fromisoformat(r['finish'])-date.fromisoformat(r['start'])).days+1
                    if r['completed']:assert abs(r['completed_km']-engine.plan['total_km'])<.01 and r['last_hotel']==r['start_hotel']
                    if r['start_hotel']=='poetto':
                        for field in ['completed','completed_km','last_hotel']:
                            assert r[field]==old[r['start']][field],(year,model,direction,r['start'],field)
                    count+=1
                for site,best in data['best_trips'].items():
                    r=best['summary'];progress=0;index=ring.index(site);km=0;current=site;previous_date=None
                    for day in best['travel']:
                        assert previous_date is None or previous_date<day['date']
                        water=0;prev=None
                        for leg in day['legs']:
                            assert leg['start']==current
                            assert leg['end']==ring[(index+progress+1)%len(ring)]
                            progress+=1;current=leg['end'];assert progress<=len(ring)
                            key=leg['start'],leg['end'],leg['departure']
                            if key not in cache:
                                closing=datetime.fromtimestamp(leg['departure'],zone).replace(hour=17,minute=0,second=0).timestamp()
                                actual,why=engine.voyage(*key,closing)
                                assert why=='ok';cache[key]=actual;replayed+=1
                            assert abs(cache[key]['arrival']-leg['arrival'])<1e-5
                            if prev is not None:assert leg['departure']-prev>=1500-1e-6
                            prev=leg['arrival'];water+=leg['water_seconds']
                        assert water<=18000+1e-6
                        assert abs(water/3600-day['water_hours'])<1e-5
                        km+=day['route_km'];previous_date=day['date']
                    assert abs(km-r['completed_km'])<.001 and current==r['last_hotel']
                    assert r['completed']==(progress==len(ring));best_count+=1
            print('verified',year,model,flush=True)
    assert count==20496
    summary=dict(runs=count,best_routes_verified=best_count,unique_selected_passages_replayed=replayed,
                 checks=['All 976 Poetto references matched','No skipped gap or overshoot in rotated circuits','Representative full route reconstruction','Wind, coast and five-hour water budget replay'])
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)

if __name__=='__main__':main()
