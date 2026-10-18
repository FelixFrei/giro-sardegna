# Historische Winddaten und Simulation

Datenquelle: **ECMWF / Open-Meteo**, ECMWF-IFS-Modellarchiv, stündlich. Abruf am 18.10.2026. [API-Dokumentation](https://open-meteo.com/en/docs/historical-weather-api), [Attribution und CC BY 4.0](https://open-meteo.com/en/pricing).

Zeitraum: September und Oktober 2022–2025. 91 angefragte Punkte entlang der Route, 63 zurückgegebene Modellzellen, insgesamt 532’896 Punktstunden ohne fehlende Werte. Doppelt zugeordnete Zellen sind keine unabhängigen Beobachtungen.

| Datei | Inhalt |
|---|---|
| [sampling.json](sampling.json) | 332 Routenstücke, Kurswinkel und Wetterpunkte |
| [coverage.json](coverage.json) | Angefragte und zurückgegebene Koordinaten, Stundenumfang und Nullwerte |
| [raw](raw/) | Unveränderte API-Antworten als gzip, Requests und Prüfsummen; zusätzlich ein kleiner Testabruf |
| [simulation-config.json](simulation-config.json) | 15–25 kn, 90–180° Wind-von-Winkel zum Fahrkurs, Zeitannahmen |
| [simulation-results.json](simulation-results.json) | 480 Reiseverläufe, Etappenfenster und lokale Windstatistik |

Eigene Verarbeitung: Punktbildung und Zuordnung zur Route, Vektorinterpolation zwischen Stundenwerten, Simulation der Fahrt und Pausen. Die Rohantworten bleiben unverändert erhalten; nur die Speicherung ist komprimiert.

[Methodik und Wiederholung](../../docs/11-wind-api-und-daten.md) · [Ergebnisse](../../docs/12-historischer-windvergleich.md)
