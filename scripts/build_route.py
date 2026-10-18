"""Build a geometric planning route, not a navigational or weather routing track.

Dependencies: shapely>=2, pyproj. Input coordinates remain preliminary.
Run from any directory. Raw WFS responses may be JSON or gzip-compressed JSON.
"""
import gzip
import json
import math
from pathlib import Path

import shapely
from shapely.geometry import shape, mapping, Point, LineString
from shapely.geometry.polygon import orient
from shapely.ops import transform, unary_union, polygonize, substring
from shapely.prepared import prep
from pyproj import Transformer, Geod

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/phase1'
FORWARD = Transformer.from_crs(4326, 32632, always_xy=True).transform
BACK = Transformer.from_crs(32632, 4326, always_xy=True).transform
GEOD = Geod(ellps='WGS84')


def read_raw(name):
    p = DATA / 'raw' / name
    if p.exists():
        return json.loads(p.read_text())
    with gzip.open(str(p) + '.gz', 'rt') as f:
        return json.load(f)


def build():
    config = json.loads((DATA / 'planning-input.json').read_text())
    features = read_raw('coastline.json')['features'] + read_raw('coastline-tail.json')['features']
    assert len(features) == 10969
    assert len({f['id'] for f in features}) == 10969
    lines = [transform(FORWARD, shape(f['geometry'])).simplify(1) for f in features if f['geometry']]
    # A 5 m precision grid closes source linework gaps; retain islands >= 0.01 km².
    polygons = sorted([p for p in polygonize(unary_union(shapely.set_precision(lines, 5)))
                       if p.area > 10000], key=lambda p: -p.area)
    assert 23000 < polygons[0].area / 1e6 < 25000
    land = unary_union(polygons)
    barrier = prep(land.buffer(25))
    buffered = unary_union([p.buffer(100) for p in polygons])
    main = max(buffered.geoms, key=lambda p: p.area)
    ring = LineString(orient(main, sign=1).exterior.coords)
    coastline = land.boundary
    points = {}
    for ident, spot in config['spots'].items():
        ref = Point(FORWARD(spot['reference_lon'], spot['reference_lat']))
        shore = coastline.interpolate(coastline.project(ref))
        route = ring.interpolate(ring.project(ref))
        spot.update(landing_coordinate=list(BACK(shore.x, shore.y)),
                    route_coordinate=list(BACK(route.x, route.y)),
                    reference_to_shore_m=round(ref.distance(shore)),
                    shore_to_route_m=round(shore.distance(route)))
        points[ident] = (ring.project(route), route)

    def water_route(a, b):
        da, pa = points[a]
        db, pb = points[b]
        if db < da:
            parts = [substring(ring, da, ring.length), substring(ring, 0, db)]
            chain = LineString(list(parts[0].coords) + list(parts[1].coords)[1:])
        else:
            chain = substring(ring, da, db)
        # Greedy visibility shortcut along the CCW shore chain. This is not a
        # shortest-path proof; all accepted chords avoid the buffered land mask.
        samples = [chain.interpolate(d) for d in range(0, int(chain.length), 50)] + [pb]
        result = [pa]
        i = 0
        while i < len(samples) - 1:
            for j in range(len(samples) - 1, i, -1):
                chord = LineString([result[-1], samples[j]])
                if not barrier.intersects(chord):
                    result.append(samples[j])
                    i = j
                    break
            else:
                raise ValueError(f'No water-only chord: {a} -> {b}, sample {i}')
        line = LineString(result)
        assert not barrier.intersects(line), (a, b)
        geo = transform(BACK, line)
        # Separate allowance for slow approach/landing: geometrical connectors
        # are NOT asserted to have adequate depth or a clear passage.
        approach_m = config['spots'][a]['shore_to_route_m'] + config['spots'][b]['shore_to_route_m']
        distance = GEOD.geometry_length(geo) / 1000 + approach_m / 1000
        distances = [line.interpolate(d).distance(land) for d in range(0, int(line.length) + 1, 100)]
        return geo, distance, max(distances, default=0) / 1000, approach_m

    legs, route_features, stages = [], [], []
    for num, ids in enumerate(config['stages'], 1):
        stage_legs = []
        for a, b in zip(ids, ids[1:]):
            geo, km, offshore, approach = water_route(a, b)
            record = dict(start=a, end=b, km=round(km, 4), max_offshore_km=round(offshore, 3),
                          approach_allowance_m=approach, stage_ccw=num)
            legs.append(record)
            stage_legs.append(record)
            route_features.append(dict(type='Feature', properties=record, geometry=mapping(geo)))
        km = sum(x['km'] for x in stage_legs)
        assert len(ids) - 2 in (2, 3)
        assert ids[-1] in config['spots'] and config['spots'][ids[-1]].get('hotel')
        assert km / config['speed_kmh'] <= config['max_riding_hours'], (num, km)
        stages.append(dict(number=num, stops=ids, km=round(km, 3), hours=km / 25,
                           longest_leg_km=max(x['km'] for x in stage_legs)))
        print(num, ids[0], '->', ids[-1], round(km, 1), 'km', round(km/25, 2), 'h', flush=True)
    assert config['stages'][0][0] == config['stages'][-1][-1] == 'poetto'
    for left, right in zip(stages, stages[1:]):
        assert left['stops'][-1] == right['stops'][0]
    result = dict(config, stages_calculated=stages, legs=legs,
                  total_km=sum(x['km'] for x in stages), source_feature_count=len(features),
                  land_polygons=len(polygons), precision_grid_m=5,
                  geometric_buffer_m=100, chord_land_clearance_m=25)
    (DATA / 'route-plan.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    (DATA / 'route.geojson').write_text(json.dumps(dict(type='FeatureCollection', features=route_features))+'\n')
    (DATA / 'land.geojson').write_text(json.dumps(dict(type='FeatureCollection', features=[
        dict(type='Feature', properties={'area_km2':round(p.area/1e6,3)},
             geometry=mapping(transform(BACK,p.simplify(30)))) for p in polygons]))+'\n')
    (DATA / 'landing-candidates.geojson').write_text(json.dumps(dict(type='FeatureCollection', features=[
        dict(type='Feature', properties={'id':k, 'name':s['name'], 'hotel':s.get('hotel',{}).get('name'),
                                        'status':'preliminary'},
             geometry={'type':'Point','coordinates':s['landing_coordinate']}) for k,s in config['spots'].items()
    ]), ensure_ascii=False)+'\n')
    print('TOTAL', round(result['total_km'],1), 'km; all legs clear of buffered model land.')


if __name__ == '__main__':
    build()
