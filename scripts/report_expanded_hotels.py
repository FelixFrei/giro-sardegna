"""Report the expanded hotel network and historical start-location comparison."""
import json
from datetime import datetime
from statistics import median
from zoneinfo import ZoneInfo
from simulate_tacking import ROOT,DATA

OUT=DATA/'start-analysis-expanded'
MODELS={'base':'Basis','cautious':'Vorsichtig'}
DIRS={'ccw':'Gegen Uhrzeigersinn','cw':'Im Uhrzeigersinn'}

def main():
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text())
    network=json.loads((DATA/'hotel-network-expanded.json').read_text())
    previous=json.loads((DATA/'hotel-network.json').read_text())
    new={k:v for k,v in network['additional_hotels'].items() if k not in previous['additional_hotels']}
    name=lambda s:plan['spots'][s]['name']
    payloads=[json.loads((OUT/f'{y}-{m}-{d}.json').read_text()) for y in range(2022,2026) for m in MODELS for d in DIRS]
    rows=[dict(year=p['year'],model=p['model'],direction=p['direction'],**r) for p in payloads for r in p['runs']]
    august=[r for r in rows if r['start'][5:7]=='08']
    oldrows=[dict(year=y,model=m,direction=d,**r) for y in range(2022,2026) for m in MODELS for d in DIRS for r in json.loads((DATA/f'start-analysis/{y}-{m}-{d}.json').read_text())['runs']]
    lines=['# Erweiterte Hotelziele und erneuter Richtungs-/Startortvergleich','','Stand: 19.10.2026. **33 Hotelziele statt 21**, davon zwölf neu belegte Übernachtungsorte an bestehenden Landeplätzen. Unverändert: 12–25 kn, alle Windrichtungen mit Aufkreuzen, Basis- und vorsichtiges Leistungsmodell, maximal fünf Stunden Wasserzeit pro Tag, Fahrzeitfenster 09–17 Uhr und 25 Minuten Landpause zwischen Fahrstücken. Winddaten August–Oktober 2022–2025. Starttermine täglich im August; Septemberstarts sind ergänzend archiviert. Ende spätestens 31. Oktober.','','## Ergebnis für Auguststarts','',f"**{sum(r['completed'] for r in august)} vollständige Runden unter {len(august)} August-Kombinationen.** Diese Zählung ist keine Erfolgswahrscheinlichkeit: Starttage überlappen und der Planer kennt den historischen Wetterverlauf. Jede vollständige Runde führt rund {plan['total_km']:.1f} km zum gewählten Starthotel zurück.",'','| Modell | Richtung | Vollständig / Versuche | Jahre mit voller Runde | Schnellste volle Runde¹ | Max. Fortschritt vorher → jetzt |','|---|---|---:|---|---:|---:|']
    for m in MODELS:
        for d in DIRS:
            rr=[r for r in august if r['model']==m and r['direction']==d];ok=[r for r in rr if r['completed']]
            prior=[r for r in oldrows if r['model']==m and r['direction']==d and r['start'][5:7]=='08']
            dur=f"{min(r['riding_days']+r['waiting_days'] for r in ok)} Tage" if ok else '–'
            years=', '.join(str(y) for y in sorted({r['year'] for r in ok})) or '–'
            lines.append(f"| {MODELS[m]} | {DIRS[d]} | {len(ok)} / {len(rr)} | {years} | {dur} | {max(r['completed_km'] for r in prior):.1f} → {max(r['completed_km'] for r in rr):.1f} km |")
    po=[r for r in august if r['start_hotel']=='poetto']
    lines+=['',f"Ab dem ursprünglichen Start Poetto sind {sum(r['completed'] for r in po)} von {len(po)} Augustläufen vollständig. Die Startortwahl bleibt deshalb auch mit dichterem Hotelnetz relevant."]
    lines+=['','¹ Kalendertage inklusive Start- und Ankunftstag sowie Wartezeiten ab gewähltem Startdatum. Die Maxima vorher/jetzt dürfen aus unterschiedlichen Jahren stammen. Die zusätzlichen Startorte und die zusätzlichen Zwischenhotels werden gemeinsam verglichen.','','## Karte des erweiterten Hotelnetzes','','![Route und 33 Hotelorte](../data/phase2/hotel-network-overview.png)','','[SVG-Karte](../data/phase2/hotel-network-overview.svg) · [Zusammenfassung auf der Startseite](../README.md). Orange Rauten markieren die zwölf neuen Hotelorte. Nummern folgen der Route gegen den Uhrzeigersinn, keine festen Tagesetappen. Karte reproduzieren: `python3 scripts/plot_hotel_network.py`.','','## Neu belegte Hotelziele und Quellen','','Entfernungen beziehen sich auf den genannten Strand, nicht auf einen vermessenen Fussweg ab dem mathematischen Routenpunkt. Die Simulation arbeitet wie bisher auf Strandort-Ebene. Hotelöffnungen und Verfügbarkeit bleiben auf Wunsch unberücksichtigt; das heutige Unterkunftsnetz wird für alle vier Wetterjahre verwendet.','','| Landeplatz | Unterkunft | Strandnähe / Quelle |','|---|---|---|']
    for k,h in new.items():
        extra=f"; [Distanzquelle]({h['distance_source']})" if h.get('distance_source') else ''
        lines.append(f"| {name(k)} | [{h['name']}]({h['url']}) | {h['proximity']}{extra} |")
    lines+=['','Alle oben aufgeführten Quellen wurden am 19.10.2026 ausgewertet. Hotel-/Residence-Anlagen zählen nur mit Hotelangebot; reine Campingplätze wurden nicht als Hotelersatz aufgenommen.','','## Verkürzte Hotelabstände','','Die folgenden Strecken zeigen die Aufteilung in Gegen-Uhrzeigersinn-Reihenfolge. Alle Distanzen stammen unverändert aus dem vorhandenen Wasserwegmodell; in Gegenrichtung gelten dieselben Längen.','','| Bisherige Hotelstrecke | Vorher | Neue Zwischenziele | Neue Teilstrecken |','|---|---:|---|---|']
    old=json.loads((DATA/'start-analysis/2024-base-ccw.json').read_text())['gaps']
    gaps=next(p for p in payloads if p['year']==2024 and p['model']=='base' and p['direction']=='ccw')['gaps']
    lookup={g['start']:g for g in gaps}
    for g in old:
        chain=[];cur=g['start']
        while True:
            part=lookup[cur];chain.append(part);cur=part['end']
            if cur==g['end']:break
            assert len(chain)<34
        if len(chain)>1:
            lines.append(f"| {name(g['start'])} → {name(g['end'])} | {g['route_km']:.1f} km | "+' → '.join(name(c['end']) for c in chain[:-1])+' | '+' + '.join(f"{c['route_km']:.1f}" for c in chain)+' km |')
    lines+=['','## Vergleich je Wetterjahr – Auguststarts','','| Jahr | Modell | Richtung | Vollständig / Versuche | Max. Strecke ab beliebigem Hotel | Max. Strecke ab Poetto |','|---|---|---|---:|---:|---:|']
    for p in payloads:
        rr=[r for r in p['runs'] if r['start'][5:7]=='08'];po=[r for r in rr if r['start_hotel']=='poetto']
        lines.append(f"| {p['year']} | {MODELS[p['model']]} | {DIRS[p['direction']]} | {sum(r['completed'] for r in rr)} / {len(rr)} | {max(r['completed_km'] for r in rr):.1f} km | {max(r['completed_km'] for r in po):.1f} km |")
    lines+=['','## Startorte im Vergleich','','Rangfolge: zuerst Anzahl vollständiger Augustläufe, danach Median des erreichten Fortschritts, danach kürzeste vollständige Reisedauer. Jeder Ort hat 124 Augustläufe (31 Tage × vier Jahre). Das ist eine rückblickende Auswahl, keine Windprognose für eine zukünftige Reise.','','| Modell | Richtung | Startort | Vollständig / 124 | Median Strecke | Kürzeste volle Runde |','|---|---|---|---:|---:|---:|']
    for m in MODELS:
        for d in DIRS:
            rr=[r for r in august if r['model']==m and r['direction']==d];rank=[]
            for h in sorted({r['start_hotel'] for r in rr}):
                hr=[r for r in rr if r['start_hotel']==h];ok=[r for r in hr if r['completed']];dur=min((r['riding_days']+r['waiting_days'] for r in ok),default=999)
                rank.append((len(ok),median(r['completed_km'] for r in hr),-dur,h))
            for count,med,negdur,h in sorted(rank,reverse=True)[:5]:
                duration=f'{-negdur} Tage' if count else '–'
                lines.append(f'| {MODELS[m]} | {DIRS[d]} | {name(h)} | {count} | {med:.1f} km | {duration} |')
    lines+=['','## Beispielverläufe','','Je Modell/Richtung: schnellste vollständige Augustreise; falls keine vollständig ist, der weiteste Augustlauf. Datum und Dauer schliessen Wartezeiten ein. Die vollständigen Tageslisten stehen im [Reiseverlauf-Dokument](25-reiseverlaeufe-erweitertes-hotelnetz.md).','','| Modell | Richtung | Startort | Bereit ab | Erste Fahrt | Ende / Auswertung bis | Strecke | Fahrtage | Wartetage |','|---|---|---|---|---|---|---:|---:|---:|']
    travel_lines=['# Beispielreisen mit erweitertem Hotelnetz','','Zur [Auswertung und Methodik](24-erweitertes-hotelnetz-simulation.md). Wartezeiten zwischen Fahrtagen werden durch die Datumsabstände sichtbar; 25 Minuten Landpause zwischen Fahrstücken bleiben erhalten.']
    examples=[]
    for m in MODELS:
        for d in DIRS:
            rr=[r for r in august if r['model']==m and r['direction']==d];ok=[r for r in rr if r['completed']]
            best=min(ok,key=lambda r:(r['riding_days']+r['waiting_days'],r['riding_days'])) if ok else max(rr,key=lambda r:r['completed_km'])
            # Reconstruct the exact selected start, since stored representatives may use a September start.
            from analyze_start_locations import evaluate
            import gzip
            p=next(p for p in payloads if p['year']==best['year'] and p['model']==m and p['direction']==d)
            cal=json.loads(gzip.decompress((OUT/f"{best['year']}-{m}-{d}-calendar.json.gz").read_bytes()))
            nodes=cal['nodes'];days=[{int(k):{int(j):v for j,v in opts.items()} for k,opts in day.items()} for day in cal['days']]
            origin=nodes.index(best['start_hotel']);start=datetime.fromisoformat(best['start']).timetuple().tm_yday-datetime(best['year'],8,1).timetuple().tm_yday
            progress,history,last=evaluate(nodes,[],days,origin,start)
            examples.append(dict(summary=best,travel=history))
            assert abs(sum(t['route_km'] for t in history)-best['completed_km'])<.001
            lines.append(f"| {MODELS[m]} | {DIRS[d]} | {name(best['start_hotel'])} | {best['start']} | {best['first_ride']} | {best['finish']} | {best['completed_km']:.1f} km | {best['riding_days']} | {best['waiting_days']} |")
            travel_lines += ['',f"## {MODELS[m]} – {DIRS[d]} – {best['year']}",'',f"Start: {name(best['start_hotel'])}, bereit ab {best['start']}. Vollständig: {'ja' if best['completed'] else 'nein'}. {best['completed_km']:.1f} km, {best['riding_days']} Fahrtage, {best['waiting_days']} Wartetage bis {best['finish']}.",'','| Datum | Von → Hotelziel | Zwischenlandungen | Abfahrt–Ankunft | Routen-km | Wasserzeit | Tatsächlicher Modellweg inkl. Kreuzen |','|---|---|---|---|---:|---:|---:|']
            zone=ZoneInfo('Europe/Rome')
            for t in history:
                legs=t['legs'];dep=datetime.fromtimestamp(legs[0]['departure'],zone);arr=datetime.fromtimestamp(legs[-1]['arrival'],zone)
                stops=', '.join(name(l['end']) for l in legs[:-1]) or '–'
                travel_lines.append(f"| {dep:%Y-%m-%d} | {name(legs[0]['start'])} → {name(legs[-1]['end'])} | {stops} | {dep:%H:%M}–{arr:%H:%M} | {t['route_km']:.1f} | {t['water_hours']:.2f} h | {t['physical_km']:.1f} km |")
    lines+=['','## Verbleibende Engpässe','','Die folgende Tabelle zeigt die seltensten Hotelpassagen nach Anzahl fahrbarer Tage über alle vier Jahre (je Jahr 92 Tage). Eine neue Übernachtung verkürzt die Tagesstrecke, erzeugt aber keinen Wind. Vor allem unbesiedelte Küstenabschnitte können weiterhin längere Hotelabstände behalten.','','| Modell | Richtung | Hotelstrecke | km | 2022 | 2023 | 2024 | 2025 |','|---|---|---|---:|---:|---:|---:|---:|']
    for m in MODELS:
        for d in DIRS:
            pp=[p for p in payloads if p['model']==m and p['direction']==d];rank=[]
            for g in pp[0]['gaps']:
                gg=[next(x for x in p['gaps'] if x['start']==g['start']) for p in pp]
                rank.append((sum(len(x['feasible_dates']) for x in gg),g['start'],gg))
            for _,_,gg in sorted(rank)[:3]:
                g=gg[0];lines.append(f"| {MODELS[m]} | {DIRS[d]} | {name(g['start'])} → {name(g['end'])} | {g['route_km']:.1f} | "+' | '.join(str(len(x['feasible_dates'])) for x in gg)+' |')
    lines+=['','## Reproduktion und Grenzen','',f"Archiviert sind {len(rows)} Läufe: 33 Orte × 61 Starttermine im August/September × vier Jahre × zwei Richtungen × zwei Modelle. Insgesamt vollständig: {sum(r['completed'] for r in rows)}. Die Haupttabellen oben beziehen sich ausschliesslich auf August.",'','- [Erweitertes Hotelnetz](../data/phase2/hotel-network-expanded.json) mit Quellen; das bisherige 21-Orte-Netz bleibt als Referenz erhalten.','- [Resultate und Tageskalender](../data/phase2/start-analysis-expanded/) enthalten Hotelnetz-Prüfsummen zur Vermeidung veralteter Cache-Nutzung.','- [Validierung](../data/phase2/start-analysis-expanded/validation.json): alle bisherigen 20.496 Startversuche müssen mindestens denselben Fortschritt erlauben; repräsentative Reisen werden mit Wind, Küste, Hotelzielen und Fünf-Stunden-Grenze erneut geprüft.','- Die [archivierten Wind-API-Daten](11-wind-api-und-daten.md) samt [August-Erweiterung](17-ab-august-180-grad.md) werden wiederverwendet. Für Hotelnähe wurden Betreiberseiten und gekennzeichnete Distanzquellen genutzt; neue Wetter-API-Abrufe waren nicht nötig.','- Unverändert: hypothetische Leistungspolaren, grobes Windraster, lokale Kreuzschläge statt grossräumiger Offshore-Routen und historischer Vorausblick. Wellen und Strömungen werden in dieser Rechnung nicht neu modelliert.','- Ein weiter erreichter Hotelort wird bei unvollständigen Läufen bis 31. Oktober gehalten; das Feld Ende ist dann der Auswertungsstichtag, nicht zwingend der letzte Fahrtag.','','```sh','python3 scripts/analyze_start_locations.py --expanded','python3 scripts/report_expanded_hotels.py','python3 scripts/validate_start_locations.py --expanded',"python3 -m unittest discover -s scripts -p 'test_*.py'",'```']
    (ROOT/'docs/24-erweitertes-hotelnetz-simulation.md').write_text('\n'.join(lines)+'\n')
    (ROOT/'docs/25-reiseverlaeufe-erweitertes-hotelnetz.md').write_text('\n'.join(travel_lines)+'\n')
    (OUT/'examples.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
