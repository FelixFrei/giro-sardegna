"""Download the two WFS pages used by this planning snapshot; archive with hashes."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'data/phase1/raw'
URL = 'https://webgis.regione.sardegna.it/geoserver/ows'


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for start, name in [(0, 'coastline'), (10000, 'coastline-tail')]:
        params = dict(service='WFS', version='1.1.0', request='GetFeature',
                      typeName='dbu:dbgt_10k_22_v05_04_linea_costa_marina',
                      outputFormat='application/json', srsName='EPSG:4326',
                      maxFeatures=10000, startIndex=start)
        response = requests.get(URL, params=params, timeout=(15, 180))
        response.raise_for_status()
        payload = response.json()
        assert payload['type'] == 'FeatureCollection'
        raw = response.content
        (DEST / f'{name}.json.gz').write_bytes(gzip.compress(raw, mtime=0))
        (DEST / f'{name}.request.json').write_text(json.dumps(dict(
            source=URL, params=params, url=response.url,
            retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
            http_status=response.status_code, bytes=len(raw),
            sha256_http_body=hashlib.sha256(raw).hexdigest(),
            count=len(payload['features'])), indent=2)+'\n')
    archive_manifest()


def archive_manifest():
    entries=[]
    for p in sorted(DEST.glob('*.json.gz')):
        b=p.read_bytes()
        entries.append(dict(file=p.name, bytes=len(b), sha256=hashlib.sha256(b).hexdigest()))
    (DEST/'manifest.json').write_text(json.dumps(dict(
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        checksum_scope='gzip archive bytes; retrieval times in corresponding request files',
        files=entries), indent=2)+'\n')


if __name__ == '__main__':
    main()
