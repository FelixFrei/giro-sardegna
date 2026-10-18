# Kürzere Tagesetappen mit Wartepausen

Stand: 18.10.2026. Historische Wetterjahre 2022–2025, jeweils 1. September bis 31. Oktober. Start ab jedem Septembertag in Poetto; beide Richtungen, Sant’Antioco aussen. Die vorhandene Route umfasst rund 890,8 km.

**Ergebnis:** Gegen den Uhrzeigersinn gelingt in allen 120 Startfällen die erste Hotel-Etappe nach Geremeas (18,9 km), gegebenenfalls erst im Oktober. Danach endet der Fortschritt. Im Uhrzeigersinn gelingt keine erste Hotel-Etappe. Keine vollständige Umrundung in diesem Modell.

## Regeln und Berechnung

- Unverändert: 15–25 kn Wind, Wind-von-Winkel 90–180° relativ zum jeweiligen Fahrkurs, kein Kreuzen; 25 km/h und höchstens fünf Fahrstunden täglich. Keine zusätzliche Böengrenze.
- Variable Hotelziele statt der festen Tagesmodule. Verglichen werden Tagesobergrenzen von 50 km (2 h Fahrt), 75 km (3 h) und 125 km (5 h). Das sind Obergrenzen, keine Mindestdistanzen.
- Wie bisher Modell-Tagesfenster 09:00–17:00 Uhr Ortszeit. Neu sind Abfahrten an jedem Landeplatz im Fünfminutenraster bis zur spätestmöglichen Ankunft um 17:00 Uhr erlaubt. Es gibt keine zusätzliche 15-Uhr-Abfahrtsgrenze.
- Jede Teilstrecke zwischen zwei benachbarten Landeplätzen muss während ihrer gesamten Passage fahrbar sein. Windprüfung mindestens alle fünf Minuten sowie an den Segmentgrenzen; zeitliche Interpolation der Windvektoren aus Stundenwerten.
- An jedem durchfahrenen Zwischenlandeplatz mindestens 25 Minuten Landpause, danach bei Bedarf längeres Warten. Auf kurzen Tagen können deshalb weniger als zwei, auf langen mehr als drei Pausen entstehen. Die ursprüngliche feste Pausenzahl wird für dieses Experiment durch diese Regel ersetzt. Keine Windprüfung während Landpausen; kein Warten auf dem Wasser.
- Übernachtungen nur an den 21 Orten der Hotelkette. Ohne erreichbares Hotel am Abend bleibt man am bisherigen Hotel. Ganze Wartetage sind erlaubt. Hotels gelten unabhängig von Öffnungszeiten und Belegung als verfügbar.
- Alle erreichbaren Hotelpositionen werden über die Tage weitergeführt. Die Rechnung wählt mit Kenntnis des historischen Wetters den frühesten Abschluss oder andernfalls den weitesten Fortschritt bis 31. Oktober. Bei Gleichstand werden weniger Fahrtage bevorzugt. Sie fährt nicht blind zum jeweils entferntesten Hotel.

## Vergleich

| Tageslimit | Richtung | Startfälle | Mindestens eine Hotel-Etappe | Vollständige Umrundungen | Erreichte Distanz |
|---|---|---:|---:|---:|---:|
| 50 km | Gegen Uhrzeigersinn | 120 | 120 | 0 | 18.9 km |
| 50 km | Im Uhrzeigersinn | 120 | 0 | 0 | 0.0 km |
| 75 km | Gegen Uhrzeigersinn | 120 | 120 | 0 | 18.9 km |
| 75 km | Im Uhrzeigersinn | 120 | 0 | 0 | 0.0 km |
| 125 km | Gegen Uhrzeigersinn | 120 | 120 | 0 | 18.9 km |
| 125 km | Im Uhrzeigersinn | 120 | 0 | 0 | 0.0 km |

720 Modellläufe insgesamt: 4 Jahre × 30 Starttage × 2 Richtungen × 3 Tageslimits. Die überlappenden Starttermine und Varianten sind keine unabhängigen Wetterereignisse. Die drei Limits liefern hier dieselben Resultate, weil bereits die nächste Einzelstrecke blockiert ist.

## Erste Fahrt gegen den Uhrzeigersinn

| Jahr | Starts mit Abfahrt noch im September | Wartezeit vor erster Fahrt (Minimum / Median / Maximum) | Erste mögliche Fahrt ab 1. September |
|---|---:|---:|---|
| 2022 | 27/30 | 0 / 5.5 / 16 Tage | 17.09. 09:00–17.09. 09:45 |
| 2023 | 24/30 | 0 / 13.5 / 29 Tage | 23.09. 13:05–23.09. 13:50 |
| 2024 | 28/30 | 0 / 3.5 / 12 Tage | 09.09. 09:00–09.09. 09:45 |
| 2025 | 0/30 | 5 / 19.5 / 34 Tage | 05.10. 10:40–05.10. 11:25 |

Alle gezeigten ersten Fahrten führen Poetto → Geremeas und dauern rund 45 Minuten reine Fahrt. Danach bleibt die Gruppe im Modell am Hotel in Geremeas. Die lange Wartezeit bis Ende Oktober wird nicht als erfolgreiche Reise gewertet. Auf den tatsächlich erreichten Fahrtagen gibt es keine Zwischenlandung; die Fähigkeit zu Wartepausen unterwegs ist implementiert und separat getestet.

## Weshalb endet die Reise so früh?

Für Geremeas → Porto Giunco (gegen Uhrzeigersinn) und Poetto → Nora (im Uhrzeigersinn) gibt es in den 244 betrachteten Tagen **keine** zulässige Abfahrt im Fünfminutenraster, die die gesamte jeweilige Einzelstrecke unter allen Windbedingungen schafft. Damit hilft an diesen Engpässen weder ein höheres Tageslimit noch längeres Warten am bisherigen Landeplatz. Ein Hotel am Porto Giunco wurde ebenfalls aufgenommen; allein dessen Aufnahme ändert das Resultat nicht.

Das bedeutet **nicht**, dass es nie 15 kn Wind gibt. Gefordert sind gleichzeitig 15–25 kn und ein passender Windwinkel an jedem geprüften Stück des geometrischen Kurses zur jeweiligen Passagezeit. Auch ein vorübergehendes Unterschreiten oder ein kurzer Gegenwindabschnitt verwirft die Fahrt.

Die Aussage betrifft das vorhandene Netz von Landeplätzen, die feste Routengeometrie und die archivierten Rasterdaten. Zusätzliche Zwischenlandungen innerhalb einer heute unteilbaren Strecke oder eine andere Kurslinie werden nicht gesucht. Die Rechnung ist deshalb kein Nachweis, dass eine reale Umrundung unmöglich ist. Sie liefert unter diesen Regeln keine tragfähige Umrundungsplanung; gegen den Uhrzeigersinn ist lediglich der Start erfolgreicher.

## Hotelnetz und Quellen

Die 17 bisherigen Hotelorte stammen aus den [Phase-1-Steckbriefen](05-landeplaetze-index.md) und deren [Quellenregister](10-quellenregister.md). Vier bisherige Pausenorte werden ergänzend als mögliche Tagesziele verwendet:

| Ort | Hotel | Strandnähe laut Betreiber / Quelle |
|---|---|---|
| geremeas | Calaserena Resort | [Am Strand von Geremeas laut Betreiber](https://www.bluserena.it/en/hotels-and-resorts/calaserena-resort/) |
| nora | Hotel Baia di Nora | [Hotel am Meer mit eigenem Strand in Nora laut Betreiber](https://www.hotelbaiadinora.com/en/hotel/) |
| porto-giunco | Almar Timi Ama | [Privatstrand Porto Giunco laut Betreiber 500 m vom Hotel, zu Fuss erreichbar](https://www.almarresorts.com/en/almar-resorts/almar-timi-ama-villasimius-sardinia.html) |
| santa-maria-navarrese | Lanthia Resort | [Strandhotel mit eigenem Strand in Santa Maria Navarrese laut Betreiber](https://www.lanthiaresort.com/en/luxury-resort-in-santa-maria-navarrese-ogliastra-sardinia/) |

Hotelquellen gelesen am 18.10.2026. Das heutige Hotelnetz wird auf alle Wetterjahre angewandt; historische Hotelverfügbarkeit wird nicht behauptet.

Windquelle: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), Modell ECMWF IFS, 10-m-Wind, nominell rund 9 km Raster. Dieselben archivierten API-Antworten wie im [ersten Vergleich](12-historischer-windvergleich.md), keine neuen Wetterabrufe. Details zu 91 Abfragepunkten, 63 tatsächlich unterschiedlichen Rasterzellen und 532.896 vollständigen Punktstunden stehen in [Wind-API und Daten](11-wind-api-und-daten.md). Lokale Strandwinde und kleinräumige Effekte werden damit nicht zuverlässig aufgelöst. Wetterverläufe sind rückblickend bekannt; das Ergebnis ist keine Wettervorhersage.

## Reproduktion und Dateien

```sh
python3 scripts/simulate_adaptive.py
python3 scripts/report_adaptive.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

- [Hotel-Ergänzungen](../data/phase2/hotel-network.json): Namen, Lagebeschreibung und Quellen.
- [Alle Ergebnisse](../data/phase2/adaptive-results.json): 720 Läufe mit Datum, Hotelzielen, Teilfahrten, Zeitstempeln, Wartezeiten und verfügbaren Teilstreckenfenstern. `land_minutes` bezeichnet zusätzliches Warten nach der Mindestpause, am Start die Zeit ab 09:00 Uhr; Zeitstempel sind Unix-Sekunden.
- [Simulator](../scripts/simulate_adaptive.py) und [Berichtsgenerator](../scripts/report_adaptive.py).

Die technische Prüfung deckt unter anderem Windwinkel und Windgrenzen, zeitliche Änderungen, Hotelpflicht, Tageslicht, Distanzlimit, Warten unterwegs und die Beibehaltung kürzerer Hotelalternativen ab.
