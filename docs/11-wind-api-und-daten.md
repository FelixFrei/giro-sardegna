# Phase 2 – API und historische Winddaten

Stand: 18.10.2026. Verwendet wird die **Open-Meteo Historical Weather API** mit fest gewähltem Modell **ECMWF IFS**. Der Testabruf für September 2022 war erfolgreich; Rohantwort und Anfrage stehen in [api-probe.json](../data/phase2/raw/api-probe.json).

## API-Auswahl

| Zugang | Eignung für dieses Projekt |
|---|---|
| Open-Meteo, ECMWF IFS | Gewählt: stündlicher Wind und Böen, etwa 9 km Raster, Archiv ab 2017 |
| Open-Meteo, ERA5 | Alternative mit konsistenter Reanalyse, etwa 25 km; Böen werden für ERA5 in dieser API nicht angeboten |
| Copernicus Climate Data Store, ERA5 | Direkter Datensatzbezug; Konto und API-Token erforderlich |
| Open-Meteo, CERRA | Hier ungeeignet: dokumentierte Abdeckung endet Juni 2021 |

Quelle für Modelle und Parameter: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api). Der direkte ERA5-Zugang ist in der [CDS-API-Anleitung](https://cds.climate.copernicus.eu/how-to-api) beschrieben. Für die erste Vergleichsrechnung bevorzuge ich die feinere IFS-Auflösung und die verfügbaren Böen. IFS ist ein Modellarchiv; Modellversionen können sich zwischen Jahren ändern. Die Daten sind keine lokalen Windmessungen.

Der öffentliche Open-Meteo-Zugang benötigt für nichtkommerzielle Nutzung keinen Schlüssel. Es gelten Abruflimits. Der Downloader arbeitet deshalb in kleinen Paketen mit Pausen und lokalem Cache. [Nutzung und Datenlizenz](https://open-meteo.com/en/pricing): Winddaten mit Attribution an **ECMWF und Open-Meteo**, CC BY 4.0. Eigene Änderungen: räumliche Zuordnung, zeitliche Vektorinterpolation und daraus abgeleitete Simulation.

## Zeitraum und Abdeckung

Vier vollständige September/Oktober-Paare: **2022, 2023, 2024 und 2025**, jeweils 1. September bis 31. Oktober. Oktober 2026 ist am Recherchetag noch nicht vollständig; deshalb wird 2026 nicht mit den vollständigen Jahren vermischt.

September ist der Startmonat. Oktober dient als Verlängerung derselben Reise, nicht als neuer Start. Wir laden beide Monate vorab, damit längere Wartezeiten ohne zusätzliche Abrufe simuliert werden können.

Die Routenlinie wird geodätisch in Stücke von höchstens fünf Kilometern aufgeteilt. Ihre Mittelpunkte werden in 0,1°-Gruppen zusammengefasst; je Gruppe dient ein Punkt auf der Route als Anfragekoordinate. Daraus entstehen **91 Abfragepunkte und 332 Routenstücke**. Beide Richtungen nutzen exakt denselben Wetterdatensatz.

Die API kann mehrere Abfragepunkte derselben Modellzelle zuordnen. Angefragte und tatsächlich zurückgegebene Koordinaten bleiben deshalb getrennt gespeichert. 91 Abfragepunkte bedeuten nicht 91 unabhängige Wetterstationen. Die abschliessenden Zahlen und Datenprüfungen stehen in [coverage.json](../data/phase2/coverage.json).

## Konkrete Abfrage

Endpunkt: `https://archive-api.open-meteo.com/v1/archive`

```text
latitude=<Breite oder Liste>
longitude=<Länge oder Liste>
start_date=2022-09-01
end_date=2022-10-31
hourly=wind_speed_10m,wind_direction_10m,wind_gusts_10m
models=ecmwf_ifs
cell_selection=sea
elevation=nan
wind_speed_unit=kn
timezone=GMT
timeformat=unixtime
```

Bei mehreren Koordinaten wird `elevation=nan` für jeden Punkt wiederholt. Das war die Ursache einer zunächst zurückgewiesenen Mehrpunktanfrage; die korrigierte Fassung wird im Skript verwendet. `cell_selection=sea` bevorzugt Meerzellen. Die ausgegebenen Zellkoordinaten und Höhen werden archiviert.

Zeitstempel sind UTC-Sekunden. Für Tagesfenster werden sie lokal mit `Europe/Rome` umgerechnet, einschliesslich der Zeitumstellung im Oktober. Windrichtung bezeichnet Wind-von; die Fahrtrichtung wird aus der Route berechnet. Wind und Böen werden in Knoten gespeichert.

## Dateien und Wiederholung

- [fetch_wind.py](../scripts/fetch_wind.py): Punktbildung, Mehrpunktabruf, Cache und Abdeckungsbericht.
- [sampling.json](../data/phase2/sampling.json): Abfragepunkte, Kurswinkel und Zuordnung aller Routenstücke.
- `data/phase2/raw/ifs-<Jahr>-<Paket>.json.gz`: komprimierte API-Antworten.
- Daneben `*.request.json`: exakte URL, Parameter, Punkt-IDs, UTC-Abrufzeit und SHA-256 der archivierten Antwort.
- [coverage.json](../data/phase2/coverage.json): Stundenumfang, fehlende Werte und tatsächlich verwendete Gitterzellen.
- [simulation-config.json](../data/phase2/simulation-config.json): eure Fahrgrenzen und die Zeitannahmen.

```sh
python3 scripts/fetch_wind.py --prepare-only
python3 scripts/fetch_wind.py --years 2022 2023 2024 2025
python3 scripts/validate_wind_data.py
python3 scripts/test_wind.py
python3 scripts/simulate_wind.py
python3 scripts/report_wind.py
```

Abhängigkeiten für den Abruf: `requests` und `pyproj`, bereits in [requirements.txt](../scripts/requirements.txt). Die Simulation benötigt nur die Python-Standardbibliothek. Vorhandene Pakete werden wiederverwendet. Ein HTTP-429-Limit stoppt den Lauf; er kann später mit demselben Befehl fortgesetzt werden.

## Simulationsregeln

**Von euch vorgegeben:** 15–25 kn Wind, von der Seite oder hinten. Interpretation für die Rechnung: 90–180° zur Wind-von-Richtung relativ zum jeweiligen Fahrkurs; kein Kreuzen. Keine zusätzliche Böengrenze angegeben, deshalb werden Böen archiviert, aber nicht als Filter verwendet.

**Rechenannahmen:** 25 km/h auf der Route; höchstens fünf Fahrstunden; 25 Minuten je geplanter Pause. Abfahrtsversuche zwischen 09:00 und 15:00 Ortszeit, alle 30 Minuten; Ankunft spätestens 17:00. Die beiden Pausen-/Hotelpläne aus Phase 1 werden jeweils in beiden Richtungen berechnet.

Windvektoren werden zwischen Stundenwerten linear interpoliert. Jedes Routenstück wird bei Einfahrt, Ausfahrt und mit höchstens fünf Minuten Abstand dazwischen geprüft. Eine Pause verschiebt die Uhrzeit des nächsten Abschnitts. Fehlende Werte gelten nicht als fahrbarer Wind.

Ein Tag zählt nur dann als Fahrtag, wenn die gesamte nächste Etappe unter diesen Annahmen passt. Andernfalls bleibt die Gruppe am aktuellen Hotelziel und wartet bis zum nächsten Tag. Es gibt keine Teilstreckenübernachtung und keine automatische Änderung der Pausen oder Hotelkette. Jeder Septembertag wird separat als möglicher Start gerechnet: 30 Starts × 4 Jahre × 4 Varianten = **480 Reiseverläufe**.

Die Rechnung kennt den historischen Tagesverlauf im Voraus und ist damit ein retrospektiver Vergleich. Sie ist auf Wind beschränkt; Wellen und Strömungen sind in diesem ersten Lauf nicht enthalten. Details zu Ausstiegen und Hotel-Fusswegen werden wie gewünscht nicht wieder eingeführt.
