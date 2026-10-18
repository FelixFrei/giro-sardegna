# Übergabe an Phase 2: historische September-Simulation

Stand: 18.10.2026. In Phase 1 wurde noch keine Windstatistik berechnet und keine Fahrtrichtung meteorologisch bevorzugt.

## Vorhandene Eingaben

- [route-plan.json](../data/phase1/route-plan.json): Landeplatz-IDs, Quellen, Hotelkandidaten, Exposition, Referenz-/Küstenpunkte und berechnete Teilstrecken.
- [route.geojson](../data/phase1/route.geojson): Wasserweg je Nachbarstopp, Richtung CCW, Länge und maximaler modellierter Landabstand. Richtung CW durch Umkehr der Koordinaten und Reihenfolge.
- [variants.json](../data/phase1/variants.json): 16 flexible Module und neun kompakte Fahrtage, jeweils beide Richtungen; ausdrücklich markierte Pausen und geometrische Zwischenpunkte.
- [landing-candidates.geojson](../data/phase1/landing-candidates.geojson): vorläufige Küstenpunkte. Keine bestätigten Foil-Startpunkte.
- [Offene Prüfungen](07-offene-pruefungen.md): noch benötigte Grenzen und Ortsprüfungen.

## Vorgeschlagener Simulationsablauf

1. Mehrere vollständige historische September mit stündlichen Windvektoren untersuchen, nicht nur Monatsmittel. Starttage variieren; Datum und Zeitzone explizit führen.
2. Wind entlang der gesamten Passage und zur tatsächlichen Uhrzeit abfragen. Windrichtung ist Wind-von; den Kurs aus den Liniensegmenten separat berechnen. Windwinkel und fahrbare Geschwindigkeit aus den noch zu liefernden persönlichen Grenzen ableiten.
3. Böen, Wellenhöhe/-periode/-richtung und gegebenenfalls Strömung ergänzen. Grobe Gitter bilden lokale Abschattung und Beschleunigung an Kaps nicht zuverlässig ab; die Landepunktprüfung bleibt separat.
4. Landen, Pause und Wiederstart zeitlich modellieren. Ein fahrbarer Wasserabschnitt darf nicht automatisch als nutzbarer Pausenstrand oder erfolgreicher Wiederstart gelten.
5. Nach jeder Passage Fahrzeit aufsummieren. Bei fünf Fahrstunden spätestens stoppen; die Pause zählt zur Tagesdauer, nicht zur Fahrzeit. Hotelziele und mögliche kürzere Module berücksichtigen.
6. Bei ungeeigneten Bedingungen einen Wartetag am vorherigen nutzbaren Hotelziel einfügen. Nicht rechnerisch mitten auf einer Passage „übernachten“ und nicht automatisch zur nächsten Küste abtreiben lassen.
7. CCW und CW mit denselben Starttagen, Daten und Leistungsgrenzen vergleichen. Ungeklärte Landepunkte separat ausweisen; sie dürfen nicht stillschweigend als erfolgreich behandelt werden.

## Gewünschte Ergebnisse

| Kennzahl | Bedeutung |
|---|---|
| Erfolgreiche Umrundungen je historischem Starttag | Anteil innerhalb des vorgegebenen Kalenderfensters |
| Fahrtage und Wartetage | Getrennte Verteilungen, Median und Streuung |
| Tagesfahrzeiten und Pausenabstände | Einhaltung der persönlichen Grenzen |
| Richtung und problematische Passagen | Häufige Gegenwind-, Wellen- oder Wiederstartprobleme |
| Hotelkette nach Verkürzungen | Tatsächliche Nachtziele pro Simulation |
| Unsicherheitsfälle | Fehlende Daten, ungelöste Landepunkte und grobe lokale Windauflösung |

Als API-Kandidat ist die [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) im bisherigen [Quellenkonzept](03-datenquellen.md) vorgesehen; ERA5/Copernicus sind Alternativen. Verfügbarkeit, Variablen, Lizenz und Auflösung bei Beginn von Phase 2 erneut prüfen. Ein Wettermodell ist keine lokale Tiefenkarte. Es wurden noch keine historischen Daten heruntergeladen.
