"""Offline consistency checks on the published planning artifacts."""
import gzip
import hashlib
import json
import math
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/phase1'


def main():
    plan=json.loads((DATA/'route-plan.json').read_text())
    variants=json.loads((DATA/'variants.json').read_text())
    inputs=json.loads((DATA/'planning-input.json').read_text())
    assert len(plan['spots'])==58
    for ident, spot in inputs['spots'].items():
        for key,value in spot.items():assert plan['spots'][ident][key]==value, (ident,key,'stale build')
        assert spot['sources'] and all(u.startswith('https://') for u in spot['sources'])
        assert (ROOT/'landeplaetze'/f'{ident}.md').exists()
    for name,stages in variants.items():
        assert len(stages)==(16 if name.startswith('flex') else 9)
        assert stages[0]['stops'][0]==stages[-1]['stops'][-1]=='poetto'
        assert math.isclose(sum(x['km'] for x in stages),plan['total_km'],abs_tol=.02)
        for i,x in enumerate(stages):
            assert 2<=len(x['stops'])-2<=3
            assert x['hours']<=5 and math.isclose(x['km']/25,x['hours'])
            assert plan['spots'][x['stops'][-1]].get('hotel')
            indices=[x['path'].index(k) for k in x['stops']]
            assert indices==sorted(indices)
            if i:assert stages[i-1]['stops'][-1]==x['stops'][0]
            assert (ROOT/'etappen'/f'{name}-{i+1:02d}.md').exists()
    for kind in ['flex','kompakt']:
        for a,b in zip(variants[kind+'-ccw'],variants[kind+'-cw'][::-1]):
            assert a['path']==b['path'][::-1] and a['stops']==b['stops'][::-1]
    route=json.loads((DATA/'route.geojson').read_text())
    assert len(route['features'])==57
    for a,b in zip(route['features'],route['features'][1:]+route['features'][:1]):
        assert a['geometry']['coordinates'][-1]==b['geometry']['coordinates'][0]
    manifest=json.loads((DATA/'raw/manifest.json').read_text())
    for f in manifest['files']:
        raw=(DATA/'raw'/f['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==f['sha256']
        json.loads(gzip.decompress(raw))
    broken=[]
    paths=[ROOT/'README.md']+list((ROOT/'docs').glob('*.md'))+list((ROOT/'landeplaetze').glob('*.md'))+list((ROOT/'etappen').glob('*.md'))
    for p in paths:
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' in link or link.startswith('#'):continue
            target=link.split('#')[0]
            if target and not (p.parent/target).exists():broken.append((str(p.relative_to(ROOT)),target))
    assert not broken,broken
    print(f'PASS: {len(plan["spots"])} spots, {len(route["features"])} connected water legs, 4 variants / 50 stage sheets, hotel endpoints, pause/time limits, reverse symmetry, raw-data hashes and local links.')


if __name__=='__main__':
    main()
