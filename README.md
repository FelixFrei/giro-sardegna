# Sardinien mit dem Wingfoil umrunden

Stand: 18.10.2026. Sprache: Deutsch. Reisezeit: September; Reisejahr noch offen.

Dieses Projekt enthält zunächst die Planungsgrundlage, das Bewertungsschema und einen ausführbaren Rechercheauftrag. **Eine vollständige Route und bewertete Landeplätze liegen noch nicht vor.** Die kleine API-Stichprobe dient nur der Prüfung von Datenquellen.

## Ziel und Phasen

1. **Phase 1:** Landeplätze recherchieren, nachvollziehbar bewerten und daraus eine zusammenhängende Umrundung mit Übernachtungszielen, 2–3 Pausen pro Tag und Alternativen entwerfen. Ausgangswert: ca. 25 km/h und bis ca. 5 Stunden täglich auf dem Wingfoil.
2. **Phase 2:** Die Varianten mit historischen September-Winddaten und ergänzenden Seegangs-/Strömungsdaten simulieren. Fahrbarkeit und Reisedauer ergeben sich erst unter den gewählten Bedingungen.

Hotelöffnungszeiten werden auf ausdrücklichen Wunsch nicht geprüft. Für Hotels werden Lage und Fussweg vom Landepunkt erfasst. Zugang und Regeln, Materiallogistik im Hotel sowie eine gesonderte Bewertung der Belegqualität sind nicht Teil der Planung. Quellenlinks bleiben Bestandteil der Dokumentation.

## Dokumente

| Datei | Inhalt |
|---|---|
| [Planungsrahmen](docs/01-planungsrahmen.md) | Vorgaben, vorgeschlagene Annahmen, Reichweite und offene Entscheidungen |
| [Bewertung der Landeplätze](docs/02-bewertung-landeplaetze.md) | Versorgungskategorien, Pflichtfelder und technische Eignung |
| [Datenquellen und APIs](docs/03-datenquellen.md) | Quellen, Zugangswege, Grenzen und tatsächlich geprüfte Abrufe |
| [Prompt für Phase 1](docs/04-prompt-phase-1.md) | Kopierbarer Arbeitsauftrag für die anschliessende Routenplanung |
| [Vorlage Landeplatz](templates/landeplatz.md) | Steckbrief mit Quellen je Aussage |
| [Vorlage Etappe](templates/etappe.md) | Teilstrecken, Pausen, Hotels, Alternativen und Nachweise |

## Daten und Nachvollziehbarkeit

Die fachlichen Ergebnisse werden in Markdown dokumentiert. Maschinenlesbare Rohdaten dürfen ergänzend als JSON/XML und später GeoJSON/GPX abgelegt werden; sie ersetzen die Markdown-Dokumentation nicht.

[scripts/check_sources.py](scripts/check_sources.py) prüft drei öffentliche Geo-Dienste mit kleinen Leseabfragen. Ausführen mit `python3 scripts/check_sources.py`. Jeder Lauf erhält ein eigenes Verzeichnis unter `data/source-checks/` mit Abfrageparametern, UTC-Abrufzeit, HTTP-Ergebnis, Prüfsumme und gegebenenfalls Rohantwort. Es werden keine Konten oder API-Schlüssel benötigt.

OSM-Daten: © OpenStreetMap contributors, [ODbL und Quellenangabe](https://www.openstreetmap.org/copyright). Andere Quellen werden getrennt mit ihren jeweiligen Nutzungsbedingungen geführt.
