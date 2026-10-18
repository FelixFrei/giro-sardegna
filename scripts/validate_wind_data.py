"""Validate archived requests, complete UTC timelines and sampling coverage offline."""
import gzip
import hashlib
import json
from pathlib import Path
from fetch_wind import validate_row

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data/phase2'


def main():
    cfg=json.loads((DATA/'simulation-config.json').read_text())
    sampling=json.loads((DATA/'sampling.json').read_text())
    assert hashlib.sha256((ROOT/'data/phase1/route.geojson').read_bytes()).hexdigest()==sampling['source_sha256']
    ids={x['id'] for x in sampling['points']};seen=set();hours=0;nulls=0
    for path in sorted((DATA/'raw').glob('ifs-*.request.json')):
        m=json.loads(path.read_text());raw=(path.parent/path.name.replace('.request.json','.json.gz')).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==m['sha256']
        year=int(m['params']['start_date'][:4]); rows=json.loads(gzip.decompress(raw)); rows=rows if isinstance(rows,list) else [rows]
        assert len(rows)==len(m['point_ids'])
        for ident,row in zip(m['point_ids'],rows):
            assert ident in ids and (year,ident) not in seen
            seen.add((year,ident));validate_row(row,year);hours+=len(row['hourly']['time'])
            nulls+=sum(values.count(None) for key,values in row['hourly'].items() if key!='time')
    assert seen=={(y,i) for y in cfg['years'] for i in ids}
    assert all(p['km']<=5.001 and p['weather_id'] in ids for p in sampling['segments'])
    coverage=json.loads((DATA/'coverage.json').read_text());assert coverage['point_hours']==hours
    assert nulls==coverage['total_nulls']
    print(f'PASS: {len(seen)} point/year series, {hours} point-hours, {nulls} nulls; hashes, hourly UTC continuity, units and complete route mapping.')


if __name__=='__main__':main()
