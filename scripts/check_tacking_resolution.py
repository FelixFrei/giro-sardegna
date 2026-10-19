"""Selected-passage sensitivity to 60 rather than 120 second integration."""
from datetime import datetime
from zoneinfo import ZoneInfo
from statistics import median
import json
from simulate_tacking import Engine,DATA
from validate_tacking import load_results


def main():
    runs=load_results();records=[];zone=ZoneInfo('Europe/Rome')
    for year in [2022,2023,2024,2025]:
        for scenario in ['base','cautious']:
            seen={}
            for r in runs:
                if r['year']==year and r['scenario']==scenario:
                    for day in r['travel']:
                        for leg in day['legs']:
                            if leg['upwind_seconds']>0:seen[(leg['start'],leg['end'],leg['departure'])]=leg
            # Stratified by year/scenario; deliberately select the longest upwind passages.
            samples=sorted(seen.values(),key=lambda l:l['upwind_seconds'],reverse=True)[:8]
            engine=Engine(scenario,year,step_seconds=60)
            for leg in samples:
                closing=datetime.fromtimestamp(leg['departure'],zone).replace(hour=17,minute=0,second=0).timestamp()
                alternative,reason=engine.voyage(leg['start'],leg['end'],leg['departure'],closing)
                records.append(dict(year=year,scenario=scenario,start=leg['start'],end=leg['end'],departure=leg['departure'],
                    valid_at_60s=alternative is not None,reason=reason,
                    duration_change_percent=(100*(alternative['water_seconds']/leg['water_seconds']-1) if alternative else None)))
    differences=[abs(r['duration_change_percent']) for r in records if r['valid_at_60s']]
    out=dict(sample='Eight longest distinct selected upwind passages per year/scenario; not a full rerun or independent sample.',
             passages=len(records),valid_at_60s=sum(r['valid_at_60s'] for r in records),
             median_absolute_duration_change_percent=median(differences) if differences else None,
             max_absolute_duration_change_percent=max(differences) if differences else None,records=records)
    (DATA/'tacking-resolution-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in out.items() if k!='records'})

if __name__=='__main__':main()
