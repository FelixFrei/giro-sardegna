# Sardinien mit dem Wingfoil umrunden

Stand: 19.10.2026 · Planung für einen Start im August · Reisejahr noch offen

**Mit 33 strandnahen Hotelzielen sind vollständige Umrundungen im Basismodell möglich – allerdings mit vielen Wartetagen.** Im vorsichtigen Leistungsmodell gelingt bisher keine ganze Runde. Gegen den Uhrzeigersinn gibt es vollständige Reisen in drei der vier untersuchten Wetterjahre, im Uhrzeigersinn in einem.

Die Route umfasst **rund 891 km**, umrundet Sant’Antioco aussen und führt zum jeweils gewählten Startort zurück. Alle **33 Hotelorte** wurden als Start und Ziel geprüft. Cagliari/Poetto bleibt der ursprüngliche Referenzstart; ab dort gelingt unter den aktuellen Annahmen noch keine vollständige Runde.

Zum Einstieg: **[Aktuelle Auswertung und Hotelquellen](docs/24-erweitertes-hotelnetz-simulation.md)** · [Tagesgenaue Beispielreisen](docs/25-reiseverlaeufe-erweitertes-hotelnetz.md) · [Landeplätze](docs/05-landeplaetze-index.md)

## Aktuelle Ergebnisse

Historische Winddaten **2022–2025**, tägliche Starttermine im August, Reiseende spätestens **31. Oktober**. Je Modell und Richtung wurden 4.092 Kombinationen aus 33 Startorten, 31 Starttagen und vier Wetterjahren gerechnet.

| Leistungsmodell | Richtung | Vollständige Läufe | Wetterjahre mit voller Runde | Schnellste volle Runde |
|---|---|---:|---|---:|
| Basis | Gegen Uhrzeigersinn | **605 / 4.092** | 2023, 2024, 2025 | **61 Tage** |
| Basis | Im Uhrzeigersinn | **171 / 4.092** | 2023 | **60 Tage** |
| Vorsichtig | Gegen Uhrzeigersinn | 0 / 4.092 | – | –; maximal 801 km |
| Vorsichtig | Im Uhrzeigersinn | 0 / 4.092 | – | –; maximal 809 km |

Die Läufe überlappen zeitlich und sind **keine unabhängigen Reisen oder Erfolgswahrscheinlichkeiten**. Der Planer kennt den historischen Wetterverlauf. Die Reisedauern enthalten Start- und Ankunftstag sowie alle Wartetage.

### Startorte und Wartezeiten

| Schnellste vollständige Beispielreise | Zeitraum | Fahrtage | Wartetage | Kalendertage |
|---|---|---:|---:|---:|
| Porto Istana → gegen Uhrzeigersinn → Porto Istana | 31.08.–30.10.2023 | 16 | 45 | 61 |
| Torregrande → im Uhrzeigersinn → Torregrande | 28.08.–26.10.2023 | 15 | 45 | 60 |

Die meisten vollständigen Augustläufe gegen den Uhrzeigersinn liefern **Su Giudeu, Porto Pino und Porto Istana**. Im Uhrzeigersinn liegen **Alghero und Bosa Marina** nach Anzahl vollständiger Läufe vorn. Der schnellste Einzelverlauf und der über mehrere Starttermine günstigste Ort sind nicht zwingend identisch. [Vollständiger Startortvergleich](docs/24-erweitertes-hotelnetz-simulation.md#startorte-im-vergleich).

**Die zusätzlichen Hotels helfen wesentlich:** Cala Gonone–La Cinta wird von einer 67-km-Hotelstrecke in **12,6 + 32,2 + 22,2 km** aufgeteilt. Bosa–Torregrande lässt sich statt 67,5 km am Stück in **21,6 + 15,8 + 30,1 km** teilen. Seltene Windfenster und ihre zeitliche Reihenfolge bleiben die entscheidenden Engpässe.

## Karte: Route und 33 Hotelziele

![Sardinienkarte mit der rund 891 km langen Route und 33 nummerierten Hotelorten; zwölf ergänzte Hotelziele sind orange Rauten, die bisherigen 21 grüne Kreise.](data/phase2/hotel-network-overview.png)

[Vergrösserbare SVG-Karte](data/phase2/hotel-network-overview.svg) · [Hotelorte und Quellen](docs/24-erweitertes-hotelnetz-simulation.md#neu-belegte-hotelziele-und-quellen) · [Landeplatz-Steckbriefe](docs/05-landeplaetze-index.md)

Die Nummern folgen der Route gegen den Uhrzeigersinn. Die Karte zeigt die Hotelkette und die geometrische Route, keine festen Tagesetappen oder tatsächlich gefahrenen Kreuzschläge. Die zwölf neuen Ziele liegen an bereits erfassten Landeplätzen; die Route bleibt für den Vergleich unverändert.

## Aktuelle Modellannahmen

- **Wind:** 12–25 kn, alle Windrichtungen. Aufkreuzen und Kurse vor dem Wind erhalten angepasste Geschwindigkeiten und Manöververluste.
- **Leistung:** Basismodell und vorsichtiges Szenario. Bei direktem Gegenwind beträgt der Fortschritt im Basismodell je nach Windstärke rund 6,8–9,8 km/h. [Leistungsannahmen](docs/21-annahmen-aufkreuzen.md).
- **Tagesplanung:** maximal fünf Stunden Wasserzeit, Fahrzeitfenster 09–17 Uhr Ortszeit, 25 Minuten Landpause zwischen Fahrstücken und Wartezeiten an Land. Jede Übernachtung erfolgt an einem Hotelort.
- **Daten:** archivierte Open-Meteo/ECMWF-IFS-Winddaten August–Oktober 2022–2025. Auguststarts bilden den Hauptvergleich; Septemberstarts sind zusätzlich archiviert. [Wind-API](docs/11-wind-api-und-daten.md) · [August-Erweiterung](docs/17-ab-august-180-grad.md).
- **Hotels:** 33 strandnahe Ziele, davon zwölf neu recherchiert. Entfernungen beziehen sich auf den benannten Strand. Öffnungszeiten und Verfügbarkeit werden wie vereinbart nicht berücksichtigt.

Die Ergebnisse hängen von hypothetischen Leistungspolaren, einem groben Windraster und lokalen Kreuzschlägen ab. Seegang und Strömungen sind in dieser Rechnung nicht modelliert. Vollständige historische Läufe sind daher keine Zusage für eine zukünftige Reise.

## Projektstand und frühere Varianten

**Phase 1** dokumentiert 58 Landeplatzkandidaten, davon 57 entlang der Runde, sowie Versorgung und geometrische Etappen. Die damaligen 16 Module beziehungsweise neun Fahrtage beruhen auf konstant 25 km/h und sind ein früher Routenentwurf, keine aktuelle Reisedauer.

**Phase 2** ergänzt historische Winddaten, variable Hotelziele, Wartezeiten, beide Fahrtrichtungen und kursabhängige Leistung. Der aktuelle Stand ist die Simulation mit dem erweiterten Hotelnetz. Frühere Windgrenzen und Richtungsfenster bleiben unten als Vergleich dokumentiert; massgeblich sind die aktuellen Annahmen oben.

Die Dokumentation konzentriert sich auf Etappen, Pausen, Versorgung und strandnahe Hotels. Zugang und Regeln, Materiallogistik und eine gesonderte Bewertung der Belegqualität sind wie vereinbart nicht Bestandteil der Planung. Quellenlinks bleiben erhalten.

## Roadmap: So gehen wir weiter vor

Ziel ist eine vollständige Umrundung mit Hotelübernachtungen und einer realistisch planbaren Reisedauer. **12–25 kn, maximal fünf Stunden Wasserzeit und beide Leistungsmodelle bleiben die Vergleichsbasis.** Die folgenden Schritte sind geplant; sie sind noch nicht umgesetzt.

| Priorität | Nächster Schritt | Ergebnis / Entscheidung |
|---|---|---|
| 1 | **Weitere strandnahe Hotels an den Engpässen recherchieren.** Auch neue Landeplätze zwischen den bisherigen Punkten aufnehmen, sofern ein Hotel in Strandnähe belegt ist. | Kürzere Hotelabstände und mehr Möglichkeiten, ein kurzes Windfenster zu nutzen. Neue Orte mit Koordinaten und Quellen dokumentieren. |
| 2 | **Erweitertes Netz erneut simulieren.** Für neue Landeplätze die Wasserwege und Windzuordnung ergänzen; beide Richtungen und alle Startorte neu rechnen. | Vorher/nachher vergleichen: vollständige Runden, Reisedauer, Fahrtage, Wartetage und verbleibende Engpässe. Den Nutzen der Ergänzungen auch bei identischem Startort und Startdatum ausweisen. |
| 3 | **Leistungsannahmen mit eigenen Fahrdaten abgleichen.** GPS-Tracks und zugehörigen Wind aus Testfahrten auswerten: Geschwindigkeit je Windwinkel, Fortschritt beim Aufkreuzen und Manöververluste. | Basis- und vorsichtiges Modell durch nachvollziehbare Werte für unser Material und Können ersetzen beziehungsweise bestätigen. |
| 4 | **Wind- und Routenmodell verfeinern.** Kritische Passagen mit weiteren historischen Daten oder lokalen Messungen vergleichen; alternative Kreuzkurse sowie Seegang und Strömungen schrittweise ergänzen, soweit geeignete Daten verfügbar sind. | Prüfen, welche Engpässe bestehen bleiben und welche durch grobe Wetterdaten oder die bisher nur lokalen Kreuzschläge entstehen. APIs und archivierte Abrufe bevorzugen. |
| 5 | **Ein festes Reisezeitbudget vergleichen.** Gemeinsam die verfügbare Reisedauer festlegen; zunächst beispielsweise 30, 45 und 60 Kalendertage gegenüberstellen. Startort, Richtung und Startfenster über mehrere Wetterjahre vergleichen. | Eine Auswahl, die sich auf mehrere Wetterverläufe stützt. Zusätzlich eine Planung mit begrenztem Vorhersagehorizont testen, statt den gesamten historischen Wetterverlauf vorauszusetzen. |
| 6 | **Konkreten Reiseplan ableiten.** Für die bevorzugte Variante Hotelziele, Pausen, kürzere Tagesalternativen und Warteorte zusammenstellen. Kurz vor Abreise Startort und ersten Abschnitt anhand der aktuellen Vorhersage wählen. | Etappenplan mit Karte und Alternativen; keine starre Tagesfolge, die nur bei einem bestimmten historischen Wetterverlauf funktioniert. |

### Wo zusätzliche Hotelziele zuerst helfen könnten

Die Priorisierung folgt den [verbleibenden Engpässen der aktuellen Simulation](docs/24-erweitertes-hotelnetz-simulation.md#verbleibende-engpässe). Sie ist ein Rechercheauftrag, keine Aussage, dass dort bereits weitere Hotels gefunden wurden.

- **Torre Salinas ↔ Torre di Bari, rund 54 km:** lange Hotelstrecke mit wenigen vollständigen Windfenstern; im vorsichtigen Modell 2025 gegen den Uhrzeigersinn kein einziges.
- **Porto Istana ↔ Baja Sardinia, rund 52,5 km:** zusätzliche Übernachtungsorte entlang der Nordostküste könnten die verbleibende lange Tagesstrecke aufteilen.
- **La Pelosa ↔ Porto Conte, rund 65,2 km:** gezielt nach strandnahen Übernachtungsorten an der Nordwestküste suchen und bei Bedarf neue Landeplätze ergänzen.
- **Santa Maria Navarrese ↔ Cala Gonone, rund 37,4 km:** trotz kürzerer Distanz seltene Fahrfenster. Prüfen, ob überhaupt geeignete Zwischenhotels vorhanden sind; andernfalls die gesamte Passage als wetterabhängigen Schlüsselabschnitt planen.
- **Nora ↔ Poetto, rund 27,5 km:** ebenfalls wenige passende Fenster. Zusätzliche Hotelziele und die lokale Windzuordnung gemeinsam prüfen, statt allein die Entfernung zu betrachten.

Nach jedem Rechenlauf werden **Zusammenfassung, Karte, Quellen und Vergleichstabellen** aktualisiert. Hotelöffnungszeiten, Zugang und Regeln, Materiallogistik sowie eine gesonderte Bewertung der Belegqualität bleiben wie vereinbart ausserhalb des Arbeitsumfangs.

## Dokumente

| Datei | Inhalt |
|---|---|
| [Planungsrahmen](docs/01-planungsrahmen.md) | Vorgaben, Annahmen, Reichweite und Detailgrad |
| [Bewertung der Landeplätze](docs/02-bewertung-landeplaetze.md) | Versorgungskategorien, Pflichtfelder und technische Eignung |
| [Datenquellen und APIs](docs/03-datenquellen.md) | Quellen, Zugangswege, Grenzen und tatsächlich geprüfte Abrufe |
| [Prompt für Phase 1](docs/04-prompt-phase-1.md) | Kopierbarer Arbeitsauftrag für die anschliessende Routenplanung |
| [Landeplätze-Index](docs/05-landeplaetze-index.md) | 58 Steckbriefe mit Quellen, Bewertung und Versorgung |
| [Routenvarianten](docs/06-routenvarianten.md) | Früher geometrischer Entwurf bei konstant 25 km/h; 16 Module / 9 Fahrtage |
| [Phase-2-Übergabe](docs/08-phase-2-uebergabe.md) | Datenstruktur und Auftrag für die historische Simulation |
| [Methodik und Daten](docs/09-methodik-und-daten.md) | Wasserwegmodell, API-Abrufe, Reproduktion und Grenzen |
| [Wind-API und Daten](docs/11-wind-api-und-daten.md) | Historische Winddaten, Abrufe und Simulationsregeln |
| [Historischer Windvergleich](docs/12-historischer-windvergleich.md) | Beide Richtungen, September-Starts und Oktober-Verlängerung |
| [Variable Etappen und Wartepausen](docs/13-variable-etappen-wartepausen.md) | Kürzere Hotel-Etappen, Wartezeiten und beide Richtungen |
| [Windfenster 360°](docs/14-windfenster-360-grad.md) | Alle Windrichtungen bei 15–25 kn, neu berechneter Richtungsvergleich |
| [12–25 kn und 360°](docs/15-windfenster-12-knoten.md) | Vergleich mit 15 kn Mindestwind, erfolgreiche Runden und Wartezeiten |
| [12–20 kn und 360°](docs/16-windfenster-12-bis-20-knoten.md) | Engeres Windfenster im Vergleich mit 12–25 kn |
| [Ab August, 180°](docs/17-ab-august-180-grad.md) | August- und Septemberstarts bei 12–20 kn und Seiten-/Rückenwind |
| [Ab August, 220°](docs/18-ab-august-220-grad.md) | 12–25 kn, Windfenster auf beiden Seiten um 20° erweitert |
| [Ab August, 240°](docs/19-ab-august-240-grad.md) | Weitere 10° je Seite, Vergleich mit 220° bei 12–25 kn |
| [Ab August, 260°](docs/20-ab-august-260-grad.md) | Weitere 10° je Seite, Vergleich mit 240° bei 12–25 kn |
| [Annahmen fürs Aufkreuzen](docs/21-annahmen-aufkreuzen.md) | Verwendete Leistungspolaren, alle Windrichtungen und Manöververluste |
| [Umrundung mit Aufkreuzen](docs/22-umrundung-mit-aufkreuzen.md) | Basis und vorsichtiges Modell, beide Richtungen, fünf Stunden Wasserzeit |
| [Engpässe und Startorte](docs/23-engpaesse-und-startorte.md) | Konkrete blockierende Passagen und Vergleich aller 21 Hotelstartorte |
| [Aktuell: Erweitertes Hotelnetz](docs/24-erweitertes-hotelnetz-simulation.md) | 33 Hotelziele, beide Richtungen und alle Startorte neu simuliert |
| [Beispielreisen](docs/25-reiseverlaeufe-erweitertes-hotelnetz.md) | Tagesetappen, Hotelziele, Wasserzeit und Wartepausen im erweiterten Netz |
| [Quellenregister](docs/10-quellenregister.md) | Quellen je Landeplatz |
| [Vorlage Landeplatz](templates/landeplatz.md) | Steckbrief mit Quellen je Aussage |
| [Vorlage Etappe](templates/etappe.md) | Teilstrecken, Pausen, Hotels, Alternativen und Nachweise |

## Daten und Nachvollziehbarkeit

Unter [data/phase1](data/phase1/) liegen archivierte API-Daten, Rechercheinput und GeoJSON für Küste, Route und Landeplätze. [Methodik und Befehle](docs/09-methodik-und-daten.md) erklären den Wiederaufbau. Konsistenzprüfung offline: `python3 scripts/validate_plan.py`.

Die aktuelle Simulation und ihre Tageskalender liegen unter [data/phase2/start-analysis-expanded](data/phase2/start-analysis-expanded/). Geprüft wurden 32.208 August-/Septemberläufe, 532 repräsentative Reisen und 4.187 unterschiedliche Fahrstücke; alle 20.496 bisherigen Startvarianten erreichen mindestens den früheren Fortschritt. [Prüfbericht](data/phase2/start-analysis-expanded/validation.json).

Die aktuelle Karte lässt sich offline mit `python3 scripts/plot_hotel_network.py` aus den archivierten Daten neu erzeugen. Python-Abhängigkeiten: [scripts/requirements.txt](scripts/requirements.txt).

Die fachlichen Ergebnisse werden in Markdown dokumentiert. Maschinenlesbare Rohdaten dürfen ergänzend als JSON/XML und später GeoJSON/GPX abgelegt werden; sie ersetzen die Markdown-Dokumentation nicht.

[scripts/check_sources.py](scripts/check_sources.py) prüft drei öffentliche Geo-Dienste mit kleinen Leseabfragen. Ausführen mit `python3 scripts/check_sources.py`. Jeder Lauf erhält ein eigenes Verzeichnis unter `data/source-checks/` mit Abfrageparametern, UTC-Abrufzeit, HTTP-Ergebnis, Prüfsumme und gegebenenfalls Rohantwort. Es werden keine Konten oder API-Schlüssel benötigt.

OSM-Daten: © OpenStreetMap contributors, [ODbL und Quellenangabe](https://www.openstreetmap.org/copyright). Andere Quellen werden getrennt mit ihren jeweiligen Nutzungsbedingungen geführt.
