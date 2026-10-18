"""Small, reproducible source checks; these are not evaluated landing sites.

Run from anywhere with Python 3.10+: python3 scripts/check_sources.py
Only the standard library is used. Each run gets a new directory.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
QUERY = """[out:json][timeout:25];
(
  nwr["natural"="beach"](39.20,9.14,39.25,9.21);
  nwr["tourism"="hotel"](39.20,9.14,39.25,9.21);
  nwr["amenity"~"^(bar|cafe|restaurant|drinking_water)$"](39.20,9.14,39.25,9.21);
  nwr["shop"~"^(supermarket|convenience)$"](39.20,9.14,39.25,9.21);
);
out center tags;
"""

SOURCES = [
    {
        "id": "overpass_sample",
        "url": "https://overpass-api.de/api/interpreter",
        "method": "POST",
        "query": QUERY,
        "format": "json",
        "purpose": "Small Cagliari/Poetto-area discovery sample, not a route recommendation",
    },
    {
        "id": "sardegna_wfs_capabilities",
        "url": "https://webgis.regione.sardegna.it/geoserver/ows?service=WFS&request=GetCapabilities&version=1.1.0",
        "method": "GET",
        "format": "xml",
        "purpose": "Discover advertised vector layers; no feature download",
    },
    {
        "id": "emodnet_wms_capabilities",
        "url": "https://ows.emodnet-bathymetry.eu/wms?service=WMS&version=1.3.0&request=GetCapabilities",
        "method": "GET",
        "format": "xml",
        "purpose": "Discover advertised map layers; no depth validation",
    },
]


def fetch(source, output):
    record = dict(source, requested_at_utc=datetime.now(timezone.utc).isoformat())
    data = None
    headers = {"User-Agent": "GiroSardegna-planning-source-check/0.1"}
    if source["method"] == "POST":
        data = urllib.parse.urlencode({"data": source["query"]}).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(source["url"], data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=40) as response:
            body = response.read()
            record.update(http_status=response.status, final_url=response.url,
                          content_type=response.headers.get("Content-Type"))
        path = output / (source["id"] + "." + source["format"])
        path.write_bytes(body)
        record.update(raw_file=str(path.relative_to(ROOT)), bytes=len(body),
                      sha256=hashlib.sha256(body).hexdigest())
        if source["format"] == "json":
            parsed = json.loads(body)
            if "remark" in parsed or "elements" not in parsed:
                raise ValueError("Overpass error or incomplete result: " + str(parsed.get("remark")))
            record["element_count"] = len(parsed["elements"])
            record["data_timestamp"] = parsed.get("osm3s", {}).get("timestamp_osm_base")
        else:
            tree = ET.fromstring(body)
            if tree.tag.split("}")[-1] not in {"WFS_Capabilities", "WMS_Capabilities", "WMT_MS_Capabilities"}:
                raise ValueError("Unexpected XML root: " + tree.tag)
            record["xml_root"] = tree.tag
        record["status"] = "ok"
    except Exception as exc:
        record.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=[source["id"] for source in SOURCES])
    args = parser.parse_args()
    selected = [source for source in SOURCES if not args.source or source["id"] == args.source]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = ROOT / "data" / "source-checks" / stamp
    output.mkdir(parents=True, exist_ok=False)
    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(lambda source: fetch(source, output), selected))
    manifest = output / "manifest.json"
    manifest.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    for record in records:
        print(record["id"], record["status"], record.get("element_count", ""), record.get("error", ""))
    print("Manifest:", manifest.relative_to(ROOT))
    return 0 if all(record["status"] == "ok" for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
