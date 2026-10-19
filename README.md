# Sardinien mit dem Wingfoil umrunden

Stand: 18.10.2026. Sprache: Deutsch. Reisezeit: September; Reisejahr noch offen.

Der erste recherchierte Routenentwurf liegt vor: **rund 891 km, 58 Landeplatzkandidaten und eine Hotelkette rund um Sardinien**, mit Start/Ziel Cagliari/Poetto und Aussenumrundung von Sant’Antioco. Beides ist als Arbeitsumfang bestätigt.

Die Route ist in **16 flexible Module** aufgeteilt und alternativ zu **neun Fahrtagen** gebündelt, jeweils mit 2–3 Pausen und in beiden Fahrtrichtungen. Alle Tage bleiben bei konstant 25 km/h unter fünf rechnerischen Fahrstunden. Ein erster historischer Windvergleich mit Wartetagen ist jetzt dokumentiert; die Fahrtgeschwindigkeit bleibt dabei konstant angesetzt. Die Dokumentation konzentriert sich auf Etappen, Pausen, Versorgung und strandnahe Hotels.

Zum Einstieg: [Routen und Etappen](docs/06-routenvarianten.md) · [Landeplätze](docs/05-landeplaetze-index.md).

![Routenübersicht](data/phase1/route-overview.png)

## Historischer Windvergleich

[API und Datenabruf](docs/11-wind-api-und-daten.md): September/Oktober 2022–2025, 91 Abfragepunkte, 63 Modellzellen, 532’896 Punktstunden ohne fehlende Werte.

[Erster Vergleich beider Richtungen](docs/12-historischer-windvergleich.md): Unter euren Grenzen von 15–25 kn und seitlichem/rückwärtigem Wind findet sich für die festen Startetappen kein vollständiges Windfenster. Die Modellannahmen und alle 480 Reiseverläufe sind dokumentiert.

## Ziel und Phasen

1. **Phase 1:** Landeplätze recherchieren, nachvollziehbar bewerten und daraus eine zusammenhängende Umrundung mit Übernachtungszielen, 2–3 Pausen pro Tag und Alternativen entwerfen. Ausgangswert: ca. 25 km/h und bis ca. 5 Stunden täglich auf dem Wingfoil.
2. **Phase 2:** Die Varianten mit historischen September-Winddaten und ergänzenden Seegangs-/Strömungsdaten simulieren. Fahrbarkeit und Reisedauer ergeben sich erst unter den gewählten Bedingungen.

Hotelöffnungszeiten werden auf ausdrücklichen Wunsch nicht geprüft. Für Hotels werden Lage und Fussweg vom Landepunkt erfasst. Zugang und Regeln, Materiallogistik im Hotel sowie eine gesonderte Bewertung der Belegqualität sind nicht Teil der Planung. Quellenlinks bleiben Bestandteil der Dokumentation.

## Dokumente

| Datei | Inhalt |
|---|---|
| [Planungsrahmen](docs/01-planungsrahmen.md) | Vorgaben, Annahmen, Reichweite und Detailgrad |
| [Bewertung der Landeplätze](docs/02-bewertung-landeplaetze.md) | Versorgungskategorien, Pflichtfelder und technische Eignung |
| [Datenquellen und APIs](docs/03-datenquellen.md) | Quellen, Zugangswege, Grenzen und tatsächlich geprüfte Abrufe |
| [Prompt für Phase 1](docs/04-prompt-phase-1.md) | Kopierbarer Arbeitsauftrag für die anschliessende Routenplanung |
| [Landeplätze-Index](docs/05-landeplaetze-index.md) | 58 Steckbriefe mit Quellen, Bewertung und Versorgung |
| [Routenvarianten](docs/06-routenvarianten.md) | 16 Module / 9 Fahrtage, CCW und CW, 50 Etappenblätter |
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
| [Annahmen fürs Aufkreuzen](docs/21-annahmen-aufkreuzen.md) | Vorschlag: alle Windrichtungen, kursabhängige Geschwindigkeit und Manöververluste |
| [Umrundung mit Aufkreuzen](docs/22-umrundung-mit-aufkreuzen.md) | Basis und vorsichtiges Modell, beide Richtungen, fünf Stunden Wasserzeit |
| [Engpässe und Startorte](docs/23-engpaesse-und-startorte.md) | Konkrete blockierende Passagen und Vergleich aller 21 Hotelstartorte |
| [Aktuell: Erweitertes Hotelnetz](docs/24-erweitertes-hotelnetz-simulation.md) | 33 Hotelziele, beide Richtungen und alle Startorte neu simuliert |
| [Beispielreisen](docs/25-reiseverlaeufe-erweitertes-hotelnetz.md) | Tagesetappen, Hotelziele, Wasserzeit und Wartepausen im erweiterten Netz |
| [Quellenregister](docs/10-quellenregister.md) | Quellen je Landeplatz |
| [Vorlage Landeplatz](templates/landeplatz.md) | Steckbrief mit Quellen je Aussage |
| [Vorlage Etappe](templates/etappe.md) | Teilstrecken, Pausen, Hotels, Alternativen und Nachweise |

## Daten und Nachvollziehbarkeit

Unter [data/phase1](data/phase1/) liegen archivierte API-Daten, Rechercheinput und GeoJSON für Küste, Route und Landeplätze. [Methodik und Befehle](docs/09-methodik-und-daten.md) erklären den Wiederaufbau. Konsistenzprüfung offline: `python3 scripts/validate_plan.py`.

Die fachlichen Ergebnisse werden in Markdown dokumentiert. Maschinenlesbare Rohdaten dürfen ergänzend als JSON/XML und später GeoJSON/GPX abgelegt werden; sie ersetzen die Markdown-Dokumentation nicht.

[scripts/check_sources.py](scripts/check_sources.py) prüft drei öffentliche Geo-Dienste mit kleinen Leseabfragen. Ausführen mit `python3 scripts/check_sources.py`. Jeder Lauf erhält ein eigenes Verzeichnis unter `data/source-checks/` mit Abfrageparametern, UTC-Abrufzeit, HTTP-Ergebnis, Prüfsumme und gegebenenfalls Rohantwort. Es werden keine Konten oder API-Schlüssel benötigt.

OSM-Daten: © OpenStreetMap contributors, [ODbL und Quellenangabe](https://www.openstreetmap.org/copyright). Andere Quellen werden getrennt mit ihren jeweiligen Nutzungsbedingungen geführt.
