"""Render the all-direction adaptive scenario from computed results."""
import json
from statistics import median
from simulate_wind import ROOT,DATA


def main():
    result=json.loads((DATA/'adaptive-results-360.json').read_text());runs=result['runs']
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    labels={'ccw':'Gegen Uhrzeigersinn','cw':'Im Uhrzeigersinn'}
    lines=['# Windfenster 360° – flexible Hotel-Etappen','','Stand: 18.10.2026. Aktualisiertes Szenario auf Wunsch: **alle Windrichtungen zugelassen**, weiterhin **15–25 kn**. September-Starttermine 2022–2025, Fortsetzung jeweils bis 31. Oktober.','','## Modelländerung','','Der Richtungsfilter entfällt. Der kleinste Winkel zwischen Wind-von-Richtung und Kurs liegt mathematisch zwischen 0° und 180°; das Intervall 0–180° lässt deshalb den gesamten 360°-Windkreis zu. Die bisherigen Seiten-/Rückenwind-Ergebnisse bleiben als Vergleich erhalten.','','Die Geschwindigkeit bleibt vereinfachend bei 25 km/h entlang der bestehenden Route, auch bei Gegenwind. Zusätzliche Kreuzstrecke oder geringere Geschwindigkeit gegen den Wind werden nicht simuliert. Dies ist ein optimistisches Szenario für den Einfluss der Windrichtung, keine Aussage zur direkt fahrbaren Geschwindigkeit bei jedem Windwinkel.','','Unverändert zum [vorherigen Versuch](13-variable-etappen-wartepausen.md): 21 Hotelorte, variable Tagesziele, 50/75/125 km Tagesobergrenzen, höchstens fünf Fahrstunden, Tagesfenster 09–17 Uhr Ortszeit, mindestens 25 Minuten an Zwischenlandeplätzen, zusätzliche Wartepausen an Land und ganze Wartetage. Übernachtungen ausschliesslich an Hotelorten. Abfahrten im Fünfminutenraster; Windstärke muss während der gesamten jeweiligen Teilstrecke passen. Keine zusätzliche Böengrenze.','','## Gesamtvergleich','','| Tageslimit | Richtung | Start möglich | Vollständige Runden | Fortschritt min. / Median / max. |','|---|---|---:|---:|---:|']
    for cap in [50,75,125]:
        for direction,label in labels.items():
            rows=[r for r in runs if r['daily_cap_km']==cap and r['direction']==direction]
            km=[r['completed_km'] for r in rows]
            lines.append(f"| {cap} km | {label} | {sum(r['riding_days']>0 for r in rows)}/{len(rows)} | {sum(r['completed'] for r in rows)}/{len(rows)} | {min(km):.1f} / {median(km):.1f} / {max(km):.1f} km |")
    lines+=['','720 Läufe: vier Jahre × 30 September-Starttermine × zwei Richtungen × drei Tageslimits. Überlappende Starttermine sind keine unabhängigen Wetterereignisse. Die Distanz ist der bis Ende Oktober erreichte Fortschritt entlang der Route, kein Tagesdurchschnitt.','','## Jahresvergleich bei maximal 75 km pro Tag','','| Jahr | Richtung | Start möglich | Erreichter Fortschritt min.–max. | Weitester Hotelort |','|---|---|---:|---:|---|']
    for year in [2022,2023,2024,2025]:
        for direction,label in labels.items():
            rows=[r for r in runs if r['year']==year and r['daily_cap_km']==75 and r['direction']==direction]
            best=max(rows,key=lambda r:r['completed_km'])
            lines.append(f"| {year} | {label} | {sum(r['riding_days']>0 for r in rows)}/30 | {min(r['completed_km'] for r in rows):.1f}–{best['completed_km']:.1f} km | {plan['spots'][best['last_hotel']]['name']} |")
    lines+=['','## Beispielverläufe mit grösstem Fortschritt','','Je Richtung der weiteste Verlauf bei 75 km Tageslimit; bei Gleichstand der früheste September-Start. Zwischen den Fahrtagen wird am zuletzt erreichten Hotel gewartet.']
    for direction,label in labels.items():
        rows=[r for r in runs if r['direction']==direction and r['daily_cap_km']==75]
        best=max(rows,key=lambda r:r['completed_km'])
        lines+=['',f"### {label}: Start {best['start']}",'',f"{best['completed_km']:.1f} km in {best['riding_days']} Fahrtagen; {best['waiting_days']} ganze Wartetage bis 31. Oktober, einschliesslich der Tage ohne Weiterfahrt nach dem letzten erreichten Hotel.",'','| Datum | Von | Nach (Hotelort) | Tagesdistanz | Zusätzliche Wartezeit unterwegs¹ |','|---|---|---|---:|---:|']
        for t in best['travel']:
            lines.append(f"| {t['date']} | {plan['spots'][t['from']]['name']} | {plan['spots'][t['to']]['name']} | {t['km']:.1f} km | {sum(l['land_minutes'] for l in t['legs'][1:]):.0f} min |")
    lines+=['','¹ Zusätzlich zu 25 Minuten Mindestpause an jedem Zwischenlandeplatz; ohne Warten vor der ersten Tagesabfahrt.','','## Einordnung','','Der gelockerte Richtungsfilter erhöht den erreichbaren Fortschritt gegenüber dem bisherigen Maximum von 18,9 km. Gegen den Uhrzeigersinn gelingen mehr Starts und der grösste Fortschritt. Dennoch erreicht keiner der simulierten Verläufe die rund 890,8 km lange Runde bis Ende Oktober. Auch mit allen Windrichtungen bleibt die Bedingung streng: Die Windstärke muss auf jeder Einzelstrecke durchgehend zwischen 15 und 25 kn liegen.','','Die Aussage gilt für das bestehende Landeplatznetz, dessen feste Routenlinien und das Tageszeitfenster. Zusätzliche Zwischenlandungen innerhalb einer Einzelstrecke werden nicht gesucht. Der Planer kennt den historischen Wetterverlauf bereits vollständig und behält alle erreichbaren Hotelalternativen bei. Die Rechnung liefert daher weder eine Vorhersage noch einen Nachweis, dass die Reise in der Realität unmöglich ist.','','## Quellen und Reproduktion','','Dieselben archivierten ECMWF-IFS-Daten der [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) wie zuvor, keine neuen Wetterabrufe. Auflösung nominell rund 9 km; lokale Strandwinde sind damit nur eingeschränkt abgebildet. API, Datenumfang und Herkunft: [Winddaten-Dokumentation](11-wind-api-und-daten.md). Hotels und Quellen: [Hotelnetz des vorherigen Versuchs](13-variable-etappen-wartepausen.md#hotelnetz-und-quellen).','','```sh','python3 scripts/simulate_adaptive.py --all-directions','python3 scripts/report_wind_360.py',"python3 -m unittest discover -s scripts -p 'test_*.py'",'```','','- [Konfiguration 360°](../data/phase2/simulation-config-360.json)', '- [Alle 720 Ergebnisse und Teilfahrten](../data/phase2/adaptive-results-360.json)', '- [Vorheriges Szenario: Seiten-/Rückenwind](13-variable-etappen-wartepausen.md)','','Die ursprüngliche Konfiguration und deren Ergebnisdateien bleiben unverändert reproduzierbar. Das neue Szenario verwendet separate Dateien.']
    (ROOT/'docs/14-windfenster-360-grad.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
