"""Compare the 12–20 knot experiment against 12–25 knots."""
import json
from statistics import median
from simulate_wind import ROOT,DATA


def main():
    runs=json.loads((DATA/'adaptive-results-360-12-20kn.json').read_text())['runs']
    old=json.loads((DATA/'adaptive-results-360-12kn.json').read_text())['runs']
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    labels={'ccw':'Gegen Uhrzeigersinn','cw':'Im Uhrzeigersinn'}
    lines=['# Windfenster 12–20 kn, alle Windrichtungen','','Stand: 19.10.2026. Gegenüber dem [12–25-kn-Szenario](15-windfenster-12-knoten.md) wird ausschliesslich die Windobergrenze auf **20 kn** gesenkt. Mindestwind 12 kn und 360°-Richtungsfenster bleiben bestehen.','','**Ergebnis: keine vollständige Umrundung in den 720 Läufen.** Zuvor gelangen bei 12–25 kn zwölf vollständige Runden gegen den Uhrzeigersinn mit maximal fünf Fahrstunden täglich.','','## Direkter Vergleich','','| Tageslimit | Richtung | Vollständige Runden 12–25 → 12–20 kn | Maximaler Fortschritt 12–25 → 12–20 kn |','|---|---|---:|---:|']
    for cap in [50,75,125]:
        for direction,label in labels.items():
            rows=[r for r in runs if r['daily_cap_km']==cap and r['direction']==direction]
            before=[r for r in old if r['daily_cap_km']==cap and r['direction']==direction]
            lines.append(f"| {cap} km | {label} | {sum(r['completed'] for r in before)}/120 → {sum(r['completed'] for r in rows)}/120 | {max(r['completed_km'] for r in before):.1f} → {max(r['completed_km'] for r in rows):.1f} km |")
    lines+=['','Die Distanz bezeichnet den gesamten erreichten Fortschritt bis spätestens 31. Oktober, keinen Tagesdurchschnitt. Je Richtung und Tageslimit werden 120 September-Starttermine betrachtet: alle 30 Tage in vier Jahren (2022–2025). In diesem Szenario gelingt bei jedem Starttermin mindestens eine Hotel-Etappe. Überlappende Starttermine sind keine unabhängigen Wetterereignisse.','','## Vergleich bei höchstens fünf Fahrstunden täglich','','| Richtung | Fortschritt Minimum / Median / Maximum | Weitester Hotelort |','|---|---:|---|']
    for direction,label in labels.items():
        rows=[r for r in runs if r['daily_cap_km']==125 and r['direction']==direction];km=[r['completed_km'] for r in rows];best=max(rows,key=lambda r:r['completed_km'])
        lines.append(f"| {label} | {min(km):.1f} / {median(km):.1f} / {max(km):.1f} km | {plan['spots'][best['last_hotel']]['name']} |")
    lines+=['','Im Uhrzeigersinn gelingt der einzelne weiteste Verlauf, gegen den Uhrzeigersinn ist der Median höher. Daraus ergibt sich keine eindeutige Vorzugsrichtung für eine vollständige Umrundung.','','## Ergebnisse nach Wetterjahr, Tageslimit 125 km','','| Jahr | Richtung | Fortschritt Minimum / Median / Maximum |','|---|---|---:|']
    for year in [2022,2023,2024,2025]:
        for direction,label in labels.items():
            km=[r['completed_km'] for r in runs if r['year']==year and r['direction']==direction and r['daily_cap_km']==125]
            lines.append(f"| {year} | {label} | {min(km):.1f} / {median(km):.1f} / {max(km):.1f} km |")
    lines+=['','## Beispielverläufe mit grösstem Fortschritt','','Je Richtung der weiteste Lauf mit maximal 125 km täglich, bei gleichem Fortschritt der erste Starttermin in der Ergebnisliste. Zwischen Fahrtagen wird am zuletzt erreichten Hotel gewartet.']
    for direction,label in labels.items():
        best=max((r for r in runs if r['direction']==direction and r['daily_cap_km']==125),key=lambda r:r['completed_km'])
        lines+=['',f"### {label}, Start {best['start']}",'',f"{best['completed_km']:.1f} km, {best['riding_days']} Fahrtage und {best['waiting_days']} ganze Wartetage bis 31. Oktober; keine abgeschlossene Runde.",'','| Datum | Von | Nach (Hotelort) | Distanz | Zusätzliche Wartezeit unterwegs¹ |','|---|---|---|---:|---:|']
        for t in best['travel']:
            lines.append(f"| {t['date']} | {plan['spots'][t['from']]['name']} | {plan['spots'][t['to']]['name']} | {t['km']:.1f} km | {sum(l['land_minutes'] for l in t['legs'][1:]):.0f} min |")
    lines+=['','¹ Zusätzlich zu mindestens 25 Minuten Pause je Zwischenlandeplatz; ohne Warten vor der ersten Tagesabfahrt.','','## Einordnung und unveränderte Annahmen','','Die Obergrenze von 20 kn entfernt nutzbare Zeitfenster aus dem bisherigen Szenario. Schon ein geprüftes Teilstück über 20 kn verwirft die betreffende Passage; bis 25 kn wäre sie bezüglich dieser Obergrenze zulässig gewesen. Der engere Bereich kann deshalb bei identischem Modell keine zusätzlichen Fahrmöglichkeiten schaffen.','','Weiterhin gelten variable Tagesziele innerhalb der recherchierten 21 Hotelorte, Landpausen und ganze Wartetage, 09–17 Uhr Ortszeit sowie höchstens fünf Fahrstunden pro Tag. Die Tagesobergrenzen 50/75/125 km entsprechen zwei/drei/fünf Stunden bei 25 km/h. Das 50-km-Limit wird zusätzlich durch grössere Lücken zwischen Hotelorten eingeschränkt, siehe [vorheriger Bericht](15-windfenster-12-knoten.md).','','**Modellvereinfachung:** konstant 25 km/h auch bei 12 kn und Gegenwind; keine zusätzliche Kreuzstrecke. Windrichtung beliebig, keine separate Böengrenze. Die Windstärke muss auf der gesamten jeweiligen Teilstrecke passen. Abfahrten werden alle fünf Minuten geprüft, Übernachtungen nur an Hotelorten. Hotelöffnungen und Belegung bleiben unberücksichtigt. Der Planer kennt das historische Wetter vollständig und berücksichtigt alle erreichbaren Hotelalternativen.','','Keine vollständige Runde im Modell bedeutet nicht, dass eine reale Umrundung unmöglich ist. Andere Kurslinien, zusätzliche Zwischenlandeplätze und lokale Windunterschiede sind hier nicht abgebildet.','','## Quellen und Reproduktion','','Wetterquelle: dieselben archivierten ECMWF-IFS-Stundenwerte der [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), nominell rund 9 km Raster; keine neuen API-Abrufe. [API- und Datendokumentation](11-wind-api-und-daten.md), [Hotelnetz und Quellen](13-variable-etappen-wartepausen.md).','','```sh','python3 scripts/simulate_adaptive.py --all-directions --min-wind 12 --max-wind 20','python3 scripts/report_wind_12_20kn.py',"python3 -m unittest discover -s scripts -p 'test_*.py'",'```','','- [Konfiguration 12–20 kn](../data/phase2/simulation-config-360-12-20kn.json)', '- [Alle Ergebnisse und Teilfahrten](../data/phase2/adaptive-results-360-12-20kn.json)', '- [Vergleich 12–25 kn](15-windfenster-12-knoten.md)','','Die vorherigen Konfigurationen und Ergebnisdateien bleiben unverändert erhalten.']
    (ROOT/'docs/16-windfenster-12-bis-20-knoten.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
