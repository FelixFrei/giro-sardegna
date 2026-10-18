"""Prepare route sampling and fetch archived hourly IFS wind, with resumable batches."""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import math
from pathlib import Path
import time

import requests
from pyproj import Geod

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/phase2'
URL='https://archive-api.open-meteo.com/v1/archive'
GEOD=Geod(ellps='WGS84')
VARIABLES=['wind_speed_10m','wind_direction_10m','wind_gusts_10m']


def prepare():
    source=ROOT/'data/phase1/route.geojson'
    route=json.loads(source.read_text())
    points=[]; bins={}; segments=[]
    for feature in route['features']:
        prop=feature['properties']; coords=feature['geometry']['coordinates']
        for a,b in zip(coords,coords[1:]):
            az,_,dist=GEOD.inv(*a[:2],*b[:2]); n=max(1,math.ceil(dist/5000))
            coords2=[a[:2]]+[list(x) for x in GEOD.npts(*a[:2],*b[:2],n-1)] if n>1 else [a[:2]]
            coords2+=[b[:2]]
            for c,d in zip(coords2,coords2[1:]):
                bearing,_,length=GEOD.inv(*c,*d)
                lon,lat,_=GEOD.fwd(*c,bearing,length/2)
                key=(round(lat,1),round(lon,1))
                if key not in bins:
                    bins[key]=len(points)
                    points.append(dict(id=f'W{len(points)+1:03d}',latitude=lat,longitude=lon))
                segments.append(dict(start=prop['start'],end=prop['end'],stage_ccw=prop['stage_ccw'],
                                     coordinates=[c,d],km=length/1000,bearing_ccw=bearing%360,
                                     weather_id=points[bins[key]]['id']))
    result=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                sampling='Geodesic pieces <=5 km; representative water point per rounded 0.1-degree midpoint bin.',
                points=points,segments=segments)
    DATA.mkdir(parents=True,exist_ok=True)
    (DATA/'sampling.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def validate_row(row,year):
    hours=row['hourly']; expected=int(datetime(year,9,1,tzinfo=timezone.utc).timestamp())
    assert row['utc_offset_seconds']==0
    assert hours['time']==list(range(expected,expected+61*86400,3600))
    for key in VARIABLES:
        assert len(hours[key])==1464
        assert all(v is None or isinstance(v,(int,float)) and math.isfinite(v) for v in hours[key])
    assert row['hourly_units']['wind_speed_10m']=='kn'
    assert row['hourly_units']['wind_gusts_10m']=='kn'
    assert row['hourly_units']['wind_direction_10m']=='°'
    assert all(v is None or 0<=v<=360 for v in hours['wind_direction_10m'])
    assert all(v is None or v>=0 for v in hours['wind_speed_10m'])


def fetch(years):
    sampling=prepare(); points=sampling['points']; raw=DATA/'raw';raw.mkdir(exist_ok=True)
    print(f'{len(points)} request points; {len(sampling["segments"])} route pieces',flush=True)
    for year in years:
        for i in range(0,len(points),5):
            batch=points[i:i+5]; name=f'ifs-{year}-{i//5:03d}'
            target=raw/(name+'.json.gz'); manifest=raw/(name+'.request.json')
            params=dict(latitude=','.join(str(round(p['latitude'],6)) for p in batch),
                        longitude=','.join(str(round(p['longitude'],6)) for p in batch),
                        start_date=f'{year}-09-01',end_date=f'{year}-10-31',
                        hourly=','.join(VARIABLES),models='ecmwf_ifs',cell_selection='sea',
                        elevation=','.join(['nan']*len(batch)),wind_speed_unit='kn',timezone='GMT',timeformat='unixtime')
            if target.exists() and manifest.exists():
                m=json.loads(manifest.read_text())
                assert m['params']==params, 'Cached request differs; preserve old dataset before changing sampling.'
                assert hashlib.sha256(target.read_bytes()).hexdigest()==m['sha256'], 'Cached response checksum mismatch'
                payload=json.loads(gzip.decompress(target.read_bytes()))
            else:
                response=requests.get(URL,params=params,timeout=(15,120))
                if response.status_code==429:
                    raise RuntimeError('API rate limit; stop and resume later, cached batches retained.')
                response.raise_for_status(); payload=response.json()
                rows=payload if isinstance(payload,list) else [payload]
                assert len(rows)==len(batch)
                for row in rows:validate_row(row,year)
                content=gzip.compress(response.content,mtime=0);target.write_bytes(content)
                manifest.write_text(json.dumps(dict(url=response.url,params=params,point_ids=[p['id'] for p in batch],
                    retrieved_at_utc=datetime.now(timezone.utc).isoformat(),http_status=response.status_code,
                    sha256=hashlib.sha256(content).hexdigest()),indent=2)+'\n')
                time.sleep(3)
            rows=payload if isinstance(payload,list) else [payload]
            for row in rows:validate_row(row,year)
            print(year,i+len(batch),'/',len(points),flush=True)
    summarize(years,sampling)


def summarize(years,sampling):
    records=[]
    for year in years:
        for i in range(0,len(sampling['points']),5):
            stem=DATA/'raw'/f'ifs-{year}-{i//5:03d}'
            rows=json.loads(gzip.decompress(Path(str(stem)+'.json.gz').read_bytes()))
            rows=rows if isinstance(rows,list) else [rows]
            for point,row in zip(sampling['points'][i:i+5],rows):
                records.append(dict(year=year,id=point['id'],requested_latitude=point['latitude'],requested_longitude=point['longitude'],
                    returned_latitude=row['latitude'],returned_longitude=row['longitude'],elevation=row['elevation'],
                    hours=len(row['hourly']['time']),null_counts={k:row['hourly'][k].count(None) for k in VARIABLES},
                    grid_offset_km=GEOD.inv(point['longitude'],point['latitude'],row['longitude'],row['latitude'])[2]/1000))
    report=dict(years=years,period='09-01 through 10-31 UTC',model='ecmwf_ifs',request_points=len(sampling['points']),
                route_segments=len(sampling['segments']),point_hours=sum(r['hours'] for r in records),
                unique_returned_cells=len({(r['returned_latitude'],r['returned_longitude']) for r in records}),
                total_nulls=sum(sum(r['null_counts'].values()) for r in records),
                max_grid_offset_km=max(r['grid_offset_km'] for r in records),records=records)
    (DATA/'coverage.json').write_text(json.dumps(report,indent=2)+'\n')
    print({k:v for k,v in report.items() if k!='records'},flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--years',nargs='+',type=int,default=[2022,2023,2024,2025]);parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    if args.prepare_only:
        s=prepare();print(len(s['points']),'weather points,',len(s['segments']),'route pieces')
    else:fetch(args.years)
