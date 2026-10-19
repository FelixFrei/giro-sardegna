"""Replay recorded passages and check hotel, calendar, time and distance constraints."""
import argparse
from datetime import date,datetime
import json
from zoneinfo import ZoneInfo
from simulate_wind import ROOT,DATA,load_weather,route_actions,attempt


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('result',help='Result filename inside data/phase2')
    args=parser.parse_args()
    result=json.loads((DATA/args.result).read_text());cfg=result['config']
    august=cfg.get('weather_period','').startswith('08-01')
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    sampling=json.loads((DATA/'sampling.json').read_text())
    weather={year:load_weather(year,august=august) for year in cfg['years']}
    for base,series in weather.values():
        assert set(series)=={p['id'] for p in sampling['points']}
        assert all(len(values)==(92 if august else 61)*24 for values in series.values())
    hotels=set(result['assumptions']['overnight_hotel_ids']);zone=ZoneInfo(cfg['local_timezone'])
    passages=0;keys=set()
    for run in result['runs']:
        key=(run['start'],run['direction'],run['daily_cap_km']);assert key not in keys;keys.add(key)
        previous_hotel='poetto';km=0;previous_day=None
        for trip in run['travel']:
            assert trip['from']==previous_hotel and trip['to'] in hotels
            assert run['start']<=trip['date']<=f"{run['year']}-10-31"
            assert previous_day is None or previous_day<trip['date']
            assert trip['km']<=min(run['daily_cap_km'],cfg['max_riding_hours']*cfg['speed_kmh'])+1e-6
            previous_arrival=None;previous_place=trip['from'];ride_seconds=0
            for leg in trip['legs']:
                assert leg['from']==previous_place
                acts=route_actions({'path':[leg['from'],leg['to']],'stops':[leg['from'],leg['to']]},sampling,plan,cfg)
                base,w=weather[run['year']]
                arrival,_=attempt(acts,leg['departure'],base,w,cfg)
                assert arrival is not None and abs(arrival-leg['arrival'])<1e-6
                start=datetime.fromtimestamp(leg['departure'],zone);end=datetime.fromtimestamp(arrival,zone)
                assert start.date().isoformat()==end.date().isoformat()==trip['date']
                assert start.hour>=9 and (end.hour,end.minute,end.second)<=(17,0,0)
                if previous_arrival is not None:
                    assert leg['departure']-previous_arrival>=cfg['pause_minutes']*60-1e-6
                ride_seconds+=arrival-leg['departure']
                previous_arrival=arrival;previous_place=leg['to'];passages+=1
            assert previous_place==trip['to']
            assert abs(ride_seconds/3600*cfg['speed_kmh']-trip['km'])<1e-5
            previous_hotel=trip['to'];km+=trip['km'];previous_day=trip['date']
        assert abs(km-run['completed_km'])<0.001 and previous_hotel==run['last_hotel']
        assert run['riding_days']==len(run['travel'])
        last=previous_day if run['completed'] else f"{run['year']}-10-31"
        assert run['riding_days']+run['waiting_days']==(date.fromisoformat(last)-date.fromisoformat(run['start'])).days+1
        if run['completed']:assert previous_hotel=='poetto' and abs(km-plan['total_km'])<0.01
    assert len(keys)==len(cfg['years'])*(61 if august else 30)*2*3
    print(f'PASS: {len(keys)} runs, {passages} wind-checked passages; complete weather coverage, hotel nights, travel dates, daylight, pause and distance limits.')

if __name__=='__main__':main()
