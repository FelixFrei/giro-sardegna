"""Compare the 12-knot scenario with the archived 15-knot scenario."""
import json
from statistics import median
from datetime import date
from simulate_wind import ROOT,DATA


def main():
    result=json.loads((DATA/'adaptive-results-360-12kn.json').read_text());runs=result['runs']
    old=json.loads((DATA/'adaptive-results-360.json').read_text())['runs']
    labels={'ccw':'Gegen Uhrzeigersinn','cw':'Im Uhrzeigersinn'}
    lines=['# 12–25 kn, Wind aus allen Richtungen','','Mindestwind auf Wunsch von 15 auf **12 kn** gesenkt. Obergrenze **25 kn**, **360°**-Windfenster und alle übrigen Regeln bleiben gleich. 720 Läufe für Starttermine vom 1.–30. September 2022–2025; gerechnet jeweils bis 31. Oktober.','','## Vergleich mit 15 kn Mindestwind','','| Tageslimit | Richtung | Runden bei 15 kn | Runden bei 12 kn | Maximaler Fortschritt 15 → 12 kn |','|---|---|---:|---:|---:|']
    for cap in [50,75,125]:
        for direction,label in labels.items():
            rows=[r for r in runs if r['daily_cap_km']==cap and r['direction']==direction]
            baseline=[r for r in old if r['daily_cap_km']==cap and r['direction']==direction]
            lines.append(f"| {cap} km | {label} | {sum(r['completed'] for r in baseline)}/120 | {sum(r['completed'] for r in rows)}/120 | {max(r['completed_km'] for r in baseline):.1f} → {max(r['completed_km'] for r in rows):.1f} km |")
    lines+=['','Bei 12 kn Mindestwind gelingt in allen 120 Startfällen je Richtung und Tageslimit mindestens eine Hotel-Etappe. Vollständige Runden gelingen ausschliesslich gegen den Uhrzeigersinn mit dem Tageslimit von 125 km (= maximal fünf Fahrstunden). Bei 75 km sind maximal drei, bei 50 km maximal zwei Fahrstunden möglich.','','## Erfolgreiche Starttermine','','| Wetterjahr | September-Starttermine mit vollständiger Runde | Ankunft Poetto | Fahrtage | Ganze Wartetage | Gesamtdauer inkl. Start- und Ankunftstag |','|---|---|---|---:|---:|---:|']
    for year in [2022,2023,2024,2025]:
        rows=[r for r in runs if r['year']==year and r['completed']]
        if not rows:
            lines.append(f'| {year} | Keine | – | – | – | – |');continue
        days=[int(r['start'][-2:]) for r in rows]
        durations=[r['riding_days']+r['waiting_days'] for r in rows]
        waits=[r['waiting_days'] for r in rows]
        lines.append(f"| {year} | {min(days)}.–{max(days)}. September | {rows[0]['travel'][-1]['date']} | {rows[0]['riding_days']} | {min(waits)}–{max(waits)} | {min(durations)}–{max(durations)} Tage |")
    lines+=['','Keine Runde endet bereits im September. Die zwölf erfolgreichen Starttermine verteilen sich auf nur zwei Wetterjahre und überlappen stark. 12/120 sind deshalb keine belastbare Erfolgswahrscheinlichkeit für eine künftige Reise.','','## Fortschritt pro Jahr bei höchstens fünf Fahrstunden','','| Jahr | Richtung | Vollständige Runden | Distanz min. / Median / max. |','|---|---|---:|---:|']
    for year in [2022,2023,2024,2025]:
        for direction,label in labels.items():
            rows=[r for r in runs if r['year']==year and r['direction']==direction and r['daily_cap_km']==125];km=[r['completed_km'] for r in rows]
            lines.append(f"| {year} | {label} | {sum(r['completed'] for r in rows)}/30 | {min(km):.1f} / {median(km):.1f} / {max(km):.1f} km |")
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    lines+=['','## Erfolgreiche Beispielreise','','Gegen den Uhrzeigersinn, Starttermin 1. September 2023. Die erste tatsächliche Fahrt findet nach Warten am Starthotel statt. Nach jedem Fahrtag Übernachtung am genannten Hotelort.','','| Fahrtag | Von | Nach (Hotelort) | Distanz | Fahrzeit | Zusätzliche Wartezeit unterwegs¹ |','|---|---|---|---:|---:|---:|']
    example=next(r for r in runs if r['completed'] and r['start']=='2023-09-01')
    for t in example['travel']:
        lines.append(f"| {t['date']} | {plan['spots'][t['from']]['name']} | {plan['spots'][t['to']]['name']} | {t['km']:.1f} km | {t['km']/25:.2f} h | {sum(l['land_minutes'] for l in t['legs'][1:]):.0f} min |")
    lines+=['','¹ Zusätzlich zur Mindestpause von 25 Minuten je Zwischenlandeplatz, ohne Warten vor der ersten Tagesabfahrt. Ganze Tage zwischen den Fahrtagen werden am letzten Hotel verbracht.','','## Was das Ergebnis bedeutet','','Die niedrigere Windgrenze macht einen grossen Unterschied. Für dieses Hotelnetz und diese Wetterjahre schneidet die Richtung gegen den Uhrzeigersinn besser ab. Dennoch benötigen selbst die erfolgreichen Runden 48–56 Kalendertage und viele Wartetage. Das Ergebnis stützt eine lange Wetterreserve, keine planbare Umrundung in wenigen Wochen.','','Das 50-km-Limit hat zusätzlich einen geometrischen Engpass: Die nächste Hotelstrecke ab Torre Salinas gegen den Uhrzeigersinn ist rund 54 km lang; ab Spiaggia Grande im Uhrzeigersinn sind es rund 60,7 km bis Piscinas. Solche Lücken im recherchierten Hotelnetz sind mit einem strikten 50-km-Tageslimit unabhängig vom Wind nicht überbrückbar. Die Unterschiede zwischen den Tageslimits sind daher nicht ausschliesslich wetterbedingt.','','## Annahmen, Daten und Reproduktion','','Unverändert: rund 890,8 km bestehende Route ab Poetto, Sant’Antioco aussen, 21 Hotelorte, 09–17 Uhr Ortszeit, Landpausen und ganze Wartetage, Fünfminuten-Abfahrtsraster, Windprüfung entlang der ganzen jeweiligen Teilstrecke. Keine Böengrenze. Hotelöffnungen und Verfügbarkeit werden nicht berücksichtigt. Der Planer behält alle erreichbaren Hotelalternativen bei und kennt den historischen Wetterverlauf im Voraus.','','**Vereinfachung:** weiterhin 25 km/h, auch bei 12 kn und Gegenwind. Zusätzliche Kreuzstrecke oder eine geringere Geschwindigkeit bei schwächerem Wind werden nicht eingerechnet. Die 360°-Freigabe ist ein Modell ohne Richtungsbeschränkung, keine Zusicherung der realen Fahrbarkeit jedes Kurses.','','Windquelle: archivierte ECMWF-IFS-Stundenwerte der [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), nominell rund 9 km Raster. Keine neuen API-Abrufe. [Datendokumentation](11-wind-api-und-daten.md), [Hotelquellen und Pausenmodell](13-variable-etappen-wartepausen.md), [Vergleichslauf mit 15–25 kn und 360°](14-windfenster-360-grad.md).','','```sh','python3 scripts/simulate_adaptive.py --all-directions --min-wind 12','python3 scripts/report_wind_12kn.py',"python3 -m unittest discover -s scripts -p 'test_*.py'",'```','','- [Konfiguration](../data/phase2/simulation-config-360-12kn.json)', '- [Alle Ergebnisse und Teilfahrten](../data/phase2/adaptive-results-360-12kn.json)','','Die vorherigen Szenarien bleiben unverändert erhalten.']
    (ROOT/'docs/15-windfenster-12-knoten.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
