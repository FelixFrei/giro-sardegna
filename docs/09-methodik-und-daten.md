# Methodik, Daten und Reproduzierbarkeit

Stand: 18.10.2026. Die Strecken sind ein geometrisches Planungsmodell. Sie berücksichtigen Landflächen, aber weder Foiltiefe, Unterwasserriffe noch Wetter. Die Distanz ist keine Vorhersage der tatsächlich gefahrenen Strecke.

## Tatsächlich bezogene Daten

**Regione Autonoma della Sardegna, WFS:** `https://webgis.regione.sardegna.it/geoserver/ows`, Layer `dbu:dbgt_10k_22_v05_04_linea_costa_marina`. Abfrage mit WFS 1.1.0, `GetFeature`, GeoJSON, `srsName=EPSG:4326`, je 10.000 Objekte. Zwei Seiten mit `startIndex=0` und `startIndex=10000` ergeben **10.969 eindeutige Objekte**; zwei ohne Geometrie. [Beschreibung der regionalen Geodienste](https://www.sardegnageoportale.it/index.php?c=8835&s=29692&t=1&v=2&xsl=1598).

Die Rohantworten und Abrufparameter liegen unter [data/phase1/raw](../data/phase1/raw/). JSON wird verlustfrei gzip-komprimiert; SHA-256 in `manifest.json` bezieht sich auf die archivierten Dateien. Die Dateigrösse einer erneut serialisierten JSON-Datei kann von der ursprünglichen HTTP-Antwort abweichen. Die Rohgeometrie ist kein Nachweis für aktuelle Uferverhältnisse im Reisejahr.

**SardegnaTurismo:** Einzelne Ortsseiten, Referenzpunkte aus deren eingebetteten Leaflet-/Drupal-Daten. [tourism-index.json](../data/phase1/tourism-index.json) dokumentiert erfolgreiche und fehlgeschlagene Abrufe. Gerundete OpenGraph-Koordinaten werden nicht verwendet. Ortszentrum, Strandreferenz und genauer Ausstieg sind ausdrücklich nicht dasselbe. Widersprüchliche Punkte wurden korrigiert oder aus der Route ausgeschlossen.

**Hotels und Gastronomie:** Betreiberwebsites und örtliche Tourismusseiten, im [Quellenregister](10-quellenregister.md) und jedem Steckbrief verlinkt. Für diese Einzelangaben war keine geeignete öffentliche API verfügbar. HTML wird nur temporär zwischengespeichert; im Repository stehen kurze sachliche Zusammenfassungen und Links.

**OpenStreetMap/Overpass:** Die Testabrufe lieferten Fehler bzw. Zeitüberschreitungen. Daher wurden keine vollständigen POI- oder Fusswegdaten daraus behauptet. OSM-Kartenlinks in den Steckbriefen dienen nur zum Öffnen der Koordinaten. EMODnet wurde in der Vorprüfung auf Erreichbarkeit geprüft, aber nicht zur Bestätigung einzelner Foil-Tiefen verwendet.

## Wie die Strecke berechnet wird

1. Küstenlinien nach UTM 32N (EPSG:32632) projizieren; mit 1 m Toleranz vereinfachen und auf ein 5-m-Raster setzen. Dieses Raster schliesst kleine Lücken der Linien. Ohne Raster lässt sich die Hauptinsel aus diesen Linien nicht vollständig polygonisieren.
2. Geschlossene Landpolygone ab 0,01 km² behalten. Die Hauptinsel hat im Modell rund 23.819 km². Kleine Felsen und Inselchen unter der Filtergrenze sowie Unterwasserhindernisse sind **nicht vollständig erfasst**.
3. Landflächen um 100 m puffern. Der grösste zusammenhängende Umriss enthält wegen der Landverbindung auch Sant’Antioco. Den äusseren Ring gegen den Uhrzeigersinn verfolgen. Der Puffer ist ein technischer Konstruktionsparameter, keine empfohlene Distanz zum Ufer.
4. Strandreferenzen auf die Küstenlinie und auf den äusseren Routenring projizieren. Verschiebungen werden je Ort dokumentiert. Projektion allein bestätigt keine sandige Landestelle.
5. Zwischen aufeinanderfolgenden Stopps den Ring alle 50 m abtasten. Jeweils zum am weitesten voraus liegenden sichtbaren Punkt abkürzen, sofern die Gerade keine um 25 m gepufferte Modelllandfläche berührt. Dadurch werden Buchten gequert und Kaps umrundet. Das ist kein Beweis eines global kürzesten Weges.
6. Linien geodätisch auf WGS84 messen. Je Start/Ziel den geometrischen Abstand zwischen Routenring und Küstenpunkt als Anlandezuschlag addieren. Dieser Zuschlag ist keine geprüfte Anfahrt und keine Tiefenbestätigung; gerade in engen Buchten kann ein anderer Korridor nötig sein.
7. Den grössten Abstand zu Modellland entlang der Strecke in 100-m-Schritten schätzen. Die Werte sind Stichproben, keine exakten Extremwerte und kein Abstand zum nächsten nutzbaren Strand.
8. Fahrzeit = Strecke / 25 km/h. Pausen je 20–30 Minuten separat. Keine Geschwindigkeitsverluste durch Kreuzen, Böen, Wellen, Manöver oder Ermüdung modelliert. Keine zusätzliche prozentuale Wetterreserve versteckt.

Die neun kompakten Fahrtage bündeln Module auf unveränderter Geometrie. Nicht besuchte Strände bleiben Zwischenpunkte mit konservativ beibehaltenen Anlandezuschlägen. Gegenrichtung: dieselben Linien umgekehrt; Wetterwirkungen bleiben offen.

## Nachbauen

Python 3.12; `requests`, `beautifulsoup4`, `shapely>=2`, `pyproj`, für die Übersicht `matplotlib`. Die verwendeten Versionen stehen in [requirements.txt](../scripts/requirements.txt). Für einen isolierten Lauf beispielsweise:

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/fetch_coast.py
.venv/bin/python scripts/fetch_tourism.py
.venv/bin/python scripts/build_route.py
.venv/bin/python scripts/render_plan.py
.venv/bin/python scripts/plot_route.py
.venv/bin/python scripts/validate_plan.py
```

Die archivierten Rohdaten erlauben den geometrischen Wiederaufbau ohne Netzwerk; dafür die beiden `fetch`-Befehle auslassen. [planning-input.json](../data/phase1/planning-input.json) enthält die bewusst manuell recherchierte Auswahl. Neue Abrufe verändern die Quellen nicht automatisch in fachlich geprüfte Landeplätze.

## Prüfungen und Grenzen

Das Bauskript prüft eindeutige Quellobjekte, geschlossene Reihenfolge, vorhandene Hotelkandidaten an jedem Nachtziel, zwei bis drei Pausen und maximal fünf nominelle Fahrstunden pro Modul. Jede konstruierte Gerade wird gegen die gepufferte Landmaske geprüft. Der zusätzliche Validator prüft alle vier Varianten, Summen, Quellen und lokale Markdown-Verknüpfungen.

Die Kartenübersicht ist zur visuellen Plausibilitätskontrolle gedacht. GeoJSON ist für weitere Bearbeitung enthalten; ein als fertiger Navigationstrack missverständlicher GPX-Export wird in diesem Stand nicht ausgegeben. Hotel-Fusswege wurden nicht als zusammenhängendes Wegenetz berechnet.
