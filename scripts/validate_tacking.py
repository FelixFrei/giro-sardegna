"""Replay all unique selected passages; validate calendar, hotel and water budgets."""
from datetime import datetime,date
import json
from zoneinfo import ZoneInfo
from simulate_tacking import Engine,DATA,ROOT


def load_results():
    results=[json.loads((DATA/f'tacking-{year}.json').read_text()) for year in [2022,2023,2024,2025]]
    assert all(len(r['runs'])==244 for r in results)
    return [run for result in results for run in result['runs']]


def main():
    runs=load_results();zone=ZoneInfo('Europe/Rome');keys=set();count=0;unique=0;trace_features=[]
    for year in [2022,2023,2024,2025]:
        for scenario in ['base','cautious']:
            engine=Engine(scenario,year);checked={}
            hotel_ids={k for k,s in engine.plan['spots'].items() if s.get('hotel')}|set(json.loads((DATA/'hotel-network.json').read_text())['additional_hotels'])
            for run in [r for r in runs if r['year']==year and r['scenario']==scenario]:
                key=(run['start'],scenario,run['direction']);assert key not in keys;keys.add(key)
                hotel='poetto';route_km=0;physical_km=0;water=0;previous_day=None
                for day in run['travel']:
                    assert day['start']==hotel and day['end'] in hotel_ids
                    assert run['start']<=day['date']<=f'{year}-10-31'
                    assert previous_day is None or previous_day<day['date']
                    seconds=0;previous_arrival=None;current=day['start'];rkm=0;pkm=0
                    for leg in day['legs']:
                        assert leg['start']==current
                        start=datetime.fromtimestamp(leg['departure'],zone);end=datetime.fromtimestamp(leg['arrival'],zone)
                        assert start.date().isoformat()==end.date().isoformat()==day['date']
                        assert start.hour>=9 and (end.hour,end.minute,end.second)<=(17,0,0)
                        if previous_arrival is not None:assert leg['departure']-previous_arrival>=1500-1e-6
                        ident=leg['start'],leg['end'],leg['departure']
                        if ident not in checked:
                            closing=start.replace(hour=17,minute=0,second=0).timestamp()
                            replay,why=engine.voyage(*ident,closing)
                            assert why=='ok',ident
                            checked[ident]=replay;unique+=1
                        replay=checked[ident]
                        for field in ['arrival','water_seconds','physical_km','route_km','manoeuvre_seconds']:
                            assert abs(replay[field]-leg[field])<1e-5,(ident,field)
                        assert leg['physical_km']>=leg['route_km']-1e-6
                        assert 0<=leg['manoeuvre_seconds']<=leg['water_seconds']
                        seconds+=leg['water_seconds'];rkm+=leg['route_km'];pkm+=leg['physical_km'];count+=1
                        previous_arrival=leg['arrival'];current=leg['end']
                    assert current==day['end'] and seconds<=18000+1e-6
                    assert abs(seconds/3600-day['water_hours'])<1e-6
                    assert abs(rkm-day['route_km'])<1e-5 and abs(pkm-day['physical_km'])<1e-5
                    hotel=current;route_km+=rkm;physical_km+=pkm;water+=seconds/3600;previous_day=day['date']
                assert hotel==run['last_hotel'] and abs(route_km-run['completed_km'])<.001
                assert abs(water-run['water_hours'])<1e-5 and abs(physical_km-run['physical_km'])<1e-5
                assert run['riding_days']==len(run['travel'])
                end_date=previous_day if run['completed'] else f'{year}-10-31'
                assert run['riding_days']+run['waiting_days']==(date.fromisoformat(end_date)-date.fromisoformat(run['start'])).days+1
                if run['completed']:assert hotel=='poetto' and abs(route_km-engine.plan['total_km'])<.01
            print('verified',year,scenario,flush=True)
    assert len(keys)==976
    summary=dict(runs=len(keys),recorded_passages=count,unique_passages_replayed=unique,
                 checks=['Wind and land geometry replay','hotel nights','five-hour water budget including manoeuvres','land pauses','daylight','physical and route distances','calendar'])
    (DATA/'tacking-validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(summary)

if __name__=='__main__':main()
