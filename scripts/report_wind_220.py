"""Report August starts with 12–25 kn and a 220-degree directional window."""
import json
from statistics import median
from simulate_wind import ROOT,DATA


def main():
    data=json.loads((DATA/'adaptive-results-august-220-12-25kn.json').read_text());runs=data['runs']
    old=json.loads((DATA/'adaptive-results-august-180-12-20kn.json').read_text())['runs']
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    labels={'ccw':'Gegen Uhrzeigersinn','cw':'Im Uhrzeigersinn'}
    lines=['# Ab August: 12–25 kn und 220°-Windfenster','','Stand: 19.10.2026. Windbereich auf Wunsch **12–25 kn**, bisheriges 180°-Windfenster um **je 20° auf beiden Seiten** erweitert. Starttermine vom 1. August bis 30. September 2022–2025, jeweils bis spätestens 31. Oktober.','','## Bedeutung des Windfensters','','Der erlaubte Halbkreis für Seiten-/Rückenwind wird zu einem 220°-Sektor. Der kleinste Winkel zwischen Kurs und Wind-von-Richtung darf jetzt **70–180°** betragen. Bei Nordkurs sind damit Wind-von-Richtungen von 70° bis 290° zulässig; der 140° breite Gegenwindsektor bleibt ausgeschlossen. Der Filter dreht sich mit jedem Teilstück des Kurses. Keine Kreuzschläge oder zusätzlichen Kurse werden berechnet.','','## Ergebnisse','','| Startmonat | Tageslimit | Richtung | Starts mit Fahrt | Vollständige Runden | Fortschritt min. / Median / max. |','|---|---|---|---:|---:|---:|']
    for month,name in [('08','August'),('09','September')]:
        for cap in [50,75,125]:
            for direction,label in labels.items():
                rows=[r for r in runs if r['start'][5:7]==month and r['daily_cap_km']==cap and r['direction']==direction];km=[r['completed_km'] for r in rows]
                lines.append(f"| {name} | {cap} km | {label} | {sum(r['riding_days']>0 for r in rows)}/{len(rows)} | {sum(r['completed'] for r in rows)}/{len(rows)} | {min(km):.1f} / {median(km):.1f} / {max(km):.1f} km |")
    lines+=['',f"**{sum(r['completed'] for r in runs)} vollständige Runden in {len(runs)} Läufen.** Vier Jahre × 61 Starttermine × zwei Richtungen × drei Tageslimits. Pro Richtung und Tageslimit 124 Auguststarts und 120 Septemberstarts. Überlappende Starttermine sind keine unabhängigen Wetterereignisse. Distanzen sind der gesamte erreichte Fortschritt bis zum Ende des Betrachtungszeitraums, keine Tagesdurchschnitte.",'','## Vergleich mit dem vorherigen Augustszenario','','Beide Änderungen – Obergrenze 20 → 25 kn und Windsektor 180 → 220° – wirken gemeinsam. Der Vergleich isoliert ihre Einzeleffekte nicht. Die folgende Tabelle bezieht sich ausschliesslich auf Auguststarts.','','| Tageslimit | Richtung | Maximaler Fortschritt bisher → neu |','|---|---|---:|']
    for cap in [50,75,125]:
        for direction,label in labels.items():
            select=lambda seq:[r['completed_km'] for r in seq if r['start'][5:7]=='08' and r['daily_cap_km']==cap and r['direction']==direction]
            lines.append(f'| {cap} km | {label} | {max(select(old)):.1f} → {max(select(runs)):.1f} km |')
    lines+=['','## Auguststarts nach Wetterjahr, maximal fünf Fahrstunden','','| Jahr | Richtung | Starts mit Fahrt | Distanz min. / Median / max. | Weitester Hotelort |','|---|---|---:|---:|---|']
    for year in [2022,2023,2024,2025]:
        for direction,label in labels.items():
            rows=[r for r in runs if r['year']==year and r['start'][5:7]=='08' and r['daily_cap_km']==125 and r['direction']==direction];km=[r['completed_km'] for r in rows];best=max(rows,key=lambda r:r['completed_km'])
            lines.append(f"| {year} | {label} | {sum(r['riding_days']>0 for r in rows)}/31 | {min(km):.1f} / {median(km):.1f} / {max(km):.1f} km | {plan['spots'][best['last_hotel']]['name']} |")
    lines+=['','## Weiteste Augustverläufe','','Je Richtung der weiteste Verlauf mit höchstens fünf Fahrstunden täglich. Bei gleichem Fortschritt wird der erste Starttermin in der Ergebnisliste gezeigt. Zwischen Fahrtagen bleibt die Gruppe am zuletzt erreichten Hotel.']
    for direction,label in labels.items():
        best=max((r for r in runs if r['start'][5:7]=='08' and r['daily_cap_km']==125 and r['direction']==direction),key=lambda r:r['completed_km'])
        lines+=['',f"### {label}, Start {best['start']}",'',f"{best['completed_km']:.1f} km in {best['riding_days']} Fahrtagen; {best['waiting_days']} ganze Wartetage bis Ende Oktober, einschliesslich der Tage ohne Weiterfahrt nach dem letzten Hotel.",'','| Datum | Von | Nach (Hotelort) | Distanz | Zusätzliche Wartezeit unterwegs¹ |','|---|---|---|---:|---:|']
        for t in best['travel']:
            lines.append(f"| {t['date']} | {plan['spots'][t['from']]['name']} | {plan['spots'][t['to']]['name']} | {t['km']:.1f} km | {sum(l['land_minutes'] for l in t['legs'][1:]):.0f} min |")
    lines+=['','¹ Zusätzlich zu mindestens 25 Minuten Pause pro Zwischenlandeplatz, ohne Warten vor der ersten Tagesabfahrt.','','## Einordnung und Annahmen','','Die zusätzlichen 20° auf beiden Seiten erlauben etwas Wind von vorne. Trotzdem muss jedes geprüfte Teilstück der vorhandenen Route den Richtungsfilter und die Windgrenzen während der Passage erfüllen. Ein kurzer unpassender Abschnitt kann eine ganze Fahrt zum nächsten Landeplatz verhindern. Das Ergebnis ist deshalb an die gewählte Routengeometrie und das bestehende Landeplatznetz gebunden; kein Nachweis der Unmöglichkeit einer realen Umrundung.','','Unverändert: konstante 25 km/h, Tageslimits 50/75/125 km (= zwei/drei/fünf Fahrstunden), 09–17 Uhr Ortszeit, mindestens 25 Minuten an Zwischenlandeplätzen, zusätzliche Land-Wartepausen und ganze Wartetage. Alle Tagesziele gehören zum recherchierten Netz von 21 Hotelorten. Hotelöffnungen und Belegung werden nicht berücksichtigt. Das 50-km-Limit kann grössere Lücken im Hotelnetz unabhängig vom Wetter nicht überbrücken.','','Die Geschwindigkeit wird auch bei 12 kn und bei den neu erlaubten Kursen mit Gegenwindkomponente konstant angenommen. Es gibt keine separate Böengrenze, kein Kreuzen und keine Suche nach alternativen Kurslinien oder neuen Zwischenlandungen. Der Planer kennt den historischen Wetterverlauf im Voraus und berücksichtigt alle erreichbaren Hotelalternativen. Abfahrtsraster fünf Minuten, Prüfung des Windes während der gesamten Teilstrecke.','','## Quellen und Reproduktion','','Dieselben archivierten August–Oktober-Daten von ECMWF IFS über die [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api); keine neuen API-Abrufe. Nominell rund 9 km Raster. [Augustdaten und Quellen](17-ab-august-180-grad.md), [Winddaten-Grundlage](11-wind-api-und-daten.md), [Hotelnetz und Quellen](13-variable-etappen-wartepausen.md).','','```sh','python3 scripts/simulate_adaptive.py --august --wide-window','python3 scripts/report_wind_220.py','python3 scripts/validate_adaptive_results.py adaptive-results-august-220-12-25kn.json',"python3 -m unittest discover -s scripts -p 'test_*.py'",'```','','- [Konfiguration](../data/phase2/simulation-config-august-220-12-25kn.json)', '- [Alle Ergebnisse und Teilfahrten](../data/phase2/adaptive-results-august-220-12-25kn.json)','','Vorherige Szenarien bleiben unverändert reproduzierbar.']
    (ROOT/'docs/18-ab-august-220-grad.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
