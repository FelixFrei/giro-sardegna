"""Collect official SardegnaTurismo map points; keep HTML in a temporary cache.

Usage: python3 scripts/fetch_tourism.py [slug ...]
Dependencies: requests, beautifulsoup4. Points are reference locations, not
surveyed wingfoil launch sites. Never use rounded OpenGraph coordinates.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path(tempfile.gettempdir()) / "giro-tourism-cache"
DEST = ROOT / "data/phase1/tourism-index.json"
SLUGS = """poetto geremeas solanas porto-giunco cala-sinzias costa-rei
torre-salinas murtas porto-corallo torre-di-bari cea porto-frailis
santa-maria-navarrese cala-mariolu cala-sisine cala-luna cala-gonone
cala-cartoe marina-di-orosei berchida capo-comino la-caletta budoni
la-cinta porto-taverna porto-istana pittulongu spiaggia-bianca
marinella capriccioli liscia-ruja baja-sardinia cannigione porto-pollo
rena-bianca rena-majore vignola-mare costa-paradiso isola-rossa li-junchi
san-pietro-a-mare lu-bagnu platamona le-saline la-pelosa
cala-coscia-di-donna argentiera porto-ferro mugoni le-bombarde
lido-di-san-giovanni spiaggia-della-speranza porto-alabe bosa-marina
santa-caterina-di-pittinuri sarchittu is-arenas putzu-idu is-arutas
san-giovanni-di-sinis torregrande arborea marceddi torre-dei-corsari
marina-di-arbus piscinas scivu portixeddu buggerru cala-domestica
masua fontanamare portoscuso cala-lunga-santantioco spiaggia-grande
cala-sapone coaquaddus maladroxia porto-botte porto-pino porto-tramatzu
tuerredda su-giudeu chia santa-margherita-di-pula nora maddalena-spiaggia""".split()


def fetch(slug):
    url = "https://www.sardegnaturismo.it/it/esplora/" + slug
    record = {"slug": slug, "url": url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        path = CACHE / (slug + ".html")
        if path.exists():
            html = path.read_text()
            record["from_cache"] = True
        else:
            response = requests.get(url, timeout=(10, 25), headers={"User-Agent": "GiroSardegnaResearch/1.0"})
            record.update(http_status=response.status_code, url=response.url)
            response.raise_for_status()
            html = response.text
            path.write_text(html)
        soup = BeautifulSoup(html, "html.parser")
        heading = soup.find("h1")
        record["title"] = heading.get_text(" ", strip=True) if heading else soup.title.get_text()
        tag = soup.find("script", attrs={"data-drupal-selector": "drupal-settings-json"})
        settings = json.loads(tag.string) if tag else {}
        points = []
        for layer in settings.get("leaflet", {}).values():
            for feature in layer.get("features", []):
                if feature.get("type") == "point":
                    points.append({key: feature[key] for key in ("lat", "lon", "entity_id") if key in feature})
        record["reference_points"] = points
        record["status"] = "ok" if points else "no_point"
        print(slug, record["status"], points[:1], flush=True)
    except Exception as exc:
        record.update(status="failed", error=str(exc))
        print(slug, "failed", str(exc)[:100], flush=True)
    return record


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(DEST.read_text()) if DEST.exists() else []
    selected = sys.argv[1:] or SLUGS
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(fetch, selected))
    by_slug = {row["slug"]: row for row in existing}
    by_slug.update({row["slug"]: row for row in results})
    DEST.write_text(json.dumps(list(by_slug.values()), ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
