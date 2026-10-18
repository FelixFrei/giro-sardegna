"""Render the researched input and geometric results into German Markdown.

Standard library only. Does not fetch data or infer missing facilities.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/phase1'


def hm(hours):
    minutes = round(hours * 60)
    return f'{minutes // 60}:{minutes % 60:02d}'


def main():
    p = json.loads((DATA / 'route-plan.json').read_text())
    s = p['spots']
    legs = {(x['start'], x['end']): x for x in p['legs']}
    def link(k):
        return f"[{s[k]['name']}](../landeplaetze/{k}.md)"
    def category(spot):
        return 'Rast' + (' + Getränke' if spot.get('food') else '') + (' + Hotel' if spot.get('hotel') else '')
    def concise(value):
        parts = re.split(r'(?<=[.;])\s+', value)
        return ' '.join(x for x in parts if not re.search(r'offen|unbekannt|prüf|bestätig|verifizier|zu verfeinern|noch genauer|noch nicht|entscheidende Lücken', x, re.I)).strip()
    sequence = [k for stage in p['stages'] for k in stage[:-1]]
    for k, spot in s.items():
        lon, lat = spot['landing_coordinate']
        hotel, food = spot.get('hotel'), spot.get('food')
        sources = '\n'.join(f'- [Quelle {i}]({url})' for i,url in enumerate(spot['sources'], 1))
        neighbor = 'Zusatzkandidat südlich von Bosa; kein regulärer Pausenpunkt dieser Route. Zusatzstrecke noch nicht berechnet.'
        if k in sequence:
            i = sequence.index(k)
            previous, following = sequence[i-1], sequence[(i+1) % len(sequence)]
            before, after = legs[(previous,k)], legs[(k,following)]
            neighbor = f"Gegen den Uhrzeigersinn: vorher {link(previous)} ({before['km']:.1f} km), danach {link(following)} ({after['km']:.1f} km). Im Uhrzeigersinn vertauscht. Wasserweg einschliesslich geometrischem Anlandezuschlag; keine Luftlinie."
        htext = f"[{hotel['name']}]({hotel['url']}). {concise(hotel['walk'])}" if hotel else 'Kein Hotel in dieser Recherche erfasst.'
        ftext = f"[{food['name']}]({food['url']}) – Getränke und Verpflegung." if food else 'Keine Verkaufsstelle in dieser Recherche erfasst.'
        text = f"""# {spot['name']}

Stand: 18.10.2026 · ID: `{k}` · Gemeinde: {spot['municipality']}

**{category(spot)}** · Planungsentwurf

## Lage und Strand

- Küstenreferenz WGS84: **{lat:.5f}, {lon:.5f}** (Breite, Länge). [Kartenansicht](https://www.openstreetmap.org/?mlat={lat:.5f}&mlon={lon:.5f}#map=16/{lat:.5f}/{lon:.5f}).
- {concise(spot['note']) or 'Strand als Pausenpunkt im Routenentwurf.'}
- Seeseite ungefähr **{spot['sea']}** (geografische Einordnung).

## Getränke und Verpflegung

{ftext}

## Übernachtung

{htext}

Entfernungsangaben stammen, soweit vorhanden, vom Anbieter.

## Nachbarstopps

{neighbor}

## Quellen

{sources}
- [Küstengeometrie, Berechnung und API-Abrufe](../docs/09-methodik-und-daten.md)
"""
        (ROOT / 'landeplaetze' / f'{k}.md').write_text(text)
    index = ['# Landeplätze – Übersicht', '', 'Stand: 18.10.2026. **58 Kandidaten**, davon 57 entlang der Runde und Porto Alabe als zusätzliche Alternative. Planungsentwurf.', '',
             'Die Kategorien zeigen die recherchierten Angebote: Rast, Getränkekauf und Hotel. Nicht aufgeführte Angebote wurden nicht erfasst; daraus folgt nicht, dass sie vor Ort fehlen.', '',
             '| Landeplatz | Versorgung | Hotel |', '|---|---|---|']
    for k,spot in s.items():
        index.append(f"| {link(k)} | {category(spot)} | {spot.get('hotel',{}).get('name','—')} |")
    index += ['', 'Die Steckbriefe enthalten Lage, Strandmerkmale, Versorgung, Hotels, Nachbarstopps und Quellen. [Routenübersicht](06-routenvarianten.md).', '']
    (ROOT/'docs/05-landeplaetze-index.md').write_text('\n'.join(index))

    # Keep the full geometry when combining modules. Bypassed stops become transit
    # points; existing approach allowances remain as conservative distance budget.
    compact_specs = [([1],None),([2],None),([3,4],['cala-luna','marina-di-orosei','la-caletta']),
                     ([5,6],['porto-istana','baja-sardinia','porto-pollo']),
                     ([7,8],['vignola-mare-aglientu','li-junchi','platamona']),
                     ([9,10],['argentiera','porto-conte','lido-di-san-giovanni']),
                     ([11,12],['putzu-idu','torregrande','torre-dei-corsari']),
                     ([13,14],['funtanamare','spiaggia-grande','coaquaddus']),
                     ([15,16],['porto-tramatzu','su-giudeu','nora'])]
    base=[]; compact=[]
    for i, ids in enumerate(p['stages'],1):base.append(dict(modules=[i],path=ids,stops=ids))
    for modules,pauses in compact_specs:
        path=[]
        for m in modules:path += p['stages'][m-1] if not path else p['stages'][m-1][1:]
        compact.append(dict(modules=modules,path=path,stops=[path[0]]+(pauses or path[1:-1])+[path[-1]]))
    all_variants={}
    overview=['# Routenvarianten – Sardinien mit Sant’Antioco', '',
              'Stand: 18.10.2026. Start und Ziel **Cagliari/Poetto**, Sant’Antioco aussen. Diese beiden Festlegungen sind vom Nutzer bestätigt. Asinara, San Pietro und La Maddalena werden nicht zusätzlich umrundet.', '',
              f"Die geometrische Runde umfasst **{p['total_km']:.1f} km**, entsprechend **{hm(p['total_km']/25)} Stunden** bei konstant 25 km/h. Das ergibt 16 flexible Module oder neun gebündelte Fahrtage. Wetterwartezeiten sind darin nicht enthalten. Die kürzeren Module sind wegen der Hotelstandorte bewusst kürzer als 80 km; die kompakte Variante nutzt den Fünfstundenrahmen stärker aus.", '',
              'Die Variante gegen den Uhrzeigersinn fährt zuerst die Ostküste hinauf. Die Gegenrichtung verwendet dieselben Wasserwege in umgekehrter Reihenfolge. Gleiche geometrische Länge bedeutet keine gleiche Fahrbarkeit; eine Vorzugsrichtung ergibt erst Phase 2.', '',
              '![Übersicht der 16 Module](../data/phase1/route-overview.png)', '',
              '**Status:** Recherchierter Planungsentwurf mit namentlich belegten Hotels. Die Wind-Simulation folgt in Phase 2.', '',
              'Buchten werden teilweise direkt gequert. Grösste modellierte Entfernung zu Land: rund 8,3 km zwischen Nora und Poetto; weitere Querungen liegen bei etwa 4–6 km.', '']
    for kind, ccw in [('flex',base),('kompakt',compact)]:
        for direction in ['ccw','cw']:
            var=f'{kind}-{direction}'
            rows=ccw if direction=='ccw' else [dict(modules=x['modules'][::-1],path=x['path'][::-1],stops=x['stops'][::-1]) for x in ccw[::-1]]
            overview += [f"## {'16 Module' if kind=='flex' else '9 Fahrtage'} – {'gegen den' if direction=='ccw' else 'im'} Uhrzeigersinn", '', '| Tag | Start → Hotelziel | Pausen | km | Fahrt h:mm | längster Abschnitt ohne geplante Pause |', '|---|---|---|---:|---:|---:|']
            records=[]
            for n,row in enumerate(rows,1):
                path, stops=row['path'],row['stops']
                selected=[]
                for a,b in zip(path,path[1:]):selected.append(legs.get((a,b)) or legs[(b,a)])
                km=sum(x['km'] for x in selected)
                pause_legs=[]
                for a,b in zip(stops,stops[1:]):
                    left,right=path.index(a),path.index(b)
                    pause_legs.append((a,b,sum(x['km'] for x in selected[left:right])))
                longest=max(x[2] for x in pause_legs)
                assert 2<=len(stops)-2<=3 and km/25<=5
                assert all(k in path for k in stops)
                assert s[stops[-1]].get('hotel')
                filename=f'{var}-{n:02d}.md'
                overview.append(f"| [{n:02d}](../etappen/{filename}) | {s[stops[0]]['name']} → {s[stops[-1]]['name']} | {' · '.join(s[x]['name'] for x in stops[1:-1])} | {km:.1f} | {hm(km/25)} | {longest:.1f} km |")
                count=len(stops)-2; hotel=s[stops[-1]]['hotel']; off=max(x['max_offshore_km'] for x in selected)
                details=[f"# {var.upper()} {n:02d}: {s[stops[0]]['name']} → {s[stops[-1]]['name']}", '',
                         'Stand: 18.10.2026 · vorläufiger Routenentwurf', '',
                         f"**{km:.1f} km · {hm(km/25)} h reine Fahrt bei 25 km/h · {count} Pausen.** Mit je 20–30 Minuten Pause: ungefähr {hm(km/25+count/3)}–{hm(km/25+count/2)} h unterwegs, zusätzlich Zeit für Anlanden, Wiederstart und Hotelweg. Rechnerische Fahrzeitreserve bis 5 h: {hm(5-km/25)} h.", '',
                         '| Abschnitt | Wasserweg | Fahrt bei 25 km/h | Funktion am Ende |', '|---|---:|---:|---|']
                for i,(a,b,dist) in enumerate(pause_legs):details.append(f"| {link(a)} → {link(b)} | {dist:.1f} km | {hm(dist/25)} h | {'Hotelziel' if b==stops[-1] else 'Pause 20–30 min'}; {category(s[b])} |")
                details += ['', '## Übernachtung und Versorgung', '',
                            f"Hotelkandidat: [{hotel['name']}]({hotel['url']}); weitere Angaben stehen im [Landeplatzblatt](../landeplaetze/{stops[-1]}.md). Alle Pausen sind unabhängig von einem Getränkekauf geplant. Angebote stehen in den verlinkten Steckbriefen.", '',
                            '## Passage und Alternativen', '',
                            f"Grösster Abstand von modelliertem Land: etwa **{off:.1f} km** (Stichprobe alle 100 m). Längster Abschnitt ohne geplante Pause: **{longest:.1f} km**, rechnerisch {hm(longest/25)} h. Der Abstand zu einem tatsächlich nutzbaren Ausstieg kann grösser sein als der Abstand zur Küste.", '',
                            f"Geometrische Reihenfolge: {' → '.join(link(k) for k in path)}.", '',
                            'Nicht als Pause markierte Orte in dieser Reihenfolge bleiben mögliche frühere Stopps.', '']
                alternatives=[k for k in path[1:-1] if s[k].get('hotel')]
                if alternatives:details.append('Frühere Hotelkandidaten auf dieser Passage: '+', '.join(link(k) for k in alternatives)+'. Eine vorgezogene Übernachtung erfordert eine neue Aufteilung der Folgetage.')
                else:details.append('Zwischen Start und Ziel wurde auf dieser Passage kein zusätzlicher Hotelkandidat mit ausreichend konkreter Strandnähe zugeordnet. Die Pausenstrände sind deshalb keine zugesicherten Nachtziele.')
                if any(k in path for k in ['cala-mariolu','cala-luna']):details += ['', 'Orosei-Abschnitt: Felsküste zwischen den Buchten, wenige Hotelziele unmittelbar am Wasser. Cala Mariolu hat Kies/Felsen; Cala Luna liegt zwischen Felswänden.']
                if 'cala-lunga-santantioco' in path:details += ['', 'Sant’Antioco wird über West- und Südküste umrundet. Die Verbindung über den Damm ist nicht Bestandteil der Route. Cala Lunga ist eine schmale Bucht mit felsigem Grund.']
                if 'porto-tramatzu' in path:details += ['', 'Die Geometrie führt um Capo Teulada.']
                details += ['', '## Grundlage', '',
                            'Eigene geodätische Berechnung aus dem [amtlichen Küstendatensatz und dokumentierten Modell](../docs/09-methodik-und-daten.md). Quellen für Strände, Gastronomie und Hotels stehen in den oben verlinkten Einzelblättern. Keine historische Windprüfung in Phase 1.', '',
                            '[Alle Varianten](../docs/06-routenvarianten.md)', '']
                (ROOT/'etappen'/filename).write_text('\n'.join(details))
                records.append(dict(number=n,stops=stops,path=path,km=km,hours=km/25,longest_nonstop_km=longest,modules=row['modules']))
            all_variants[var]=records
            overview += ['']
    overview += ['## Auswahl für Phase 2', '',
                 'Die 16 Module bilden die flexible Hotelkette. Die neun Fahrtage sind ein kompakter Vergleich, keine feststehende Reisedauer: Auf dem längsten Tag bleibt bei 25 km/h nur ungefähr eine Viertelstunde Reserve. Langsameres Vorankommen, Kreuzen oder aufwendige Wiederstarts können ihn über fünf Fahrstunden bringen. Deshalb die Module als mögliche Abbruch- und Übernachtungsziele in die Simulation übernehmen.', '',
                 'Die kompakte Variante behält die Geometrie aller Module einschliesslich der bisherigen Anlandezuschläge bei. Nicht genutzte Pausen werden zu Zwischenpunkten; ihre Zuschläge bleiben als kleiner konservativer Distanzpuffer bestehen. Es wurde keine zweite kürzeste Route berechnet.', '',
                 '[Landeplätze und Quellen](05-landeplaetze-index.md) · [Methodik](09-methodik-und-daten.md) · [Phase-2-Übergabe](08-phase-2-uebergabe.md)', '']
    (ROOT/'docs/06-routenvarianten.md').write_text('\n'.join(overview))
    (DATA/'variants.json').write_text(json.dumps(all_variants,ensure_ascii=False,indent=2)+'\n')
    source_lines=['# Quellenregister Phase 1','','Abruf-/Recherchetag: 18.10.2026. API-Abrufe mit UTC-Zeit in den Rohdatenmanifesten. Die Links in den Steckbriefen ordnen die Aussagen einem Ort zu. Keine gesonderte Belegbewertung.','','| URL | Verwendung |','|---|---|']
    urls={}
    for k,spot in s.items():
        for url in spot['sources']:urls.setdefault(url,[]).append(link(k))
    for url,used in sorted(urls.items()):source_lines.append(f"| [Quelle]({url}) | {', '.join(used)} |")
    source_lines += ['', '[API-Quellen und technische Grenzen](09-methodik-und-daten.md). Fehlgeschlagene regionale Seitenabrufe bleiben in `tourism-index.json` dokumentiert; sie sind kein Nachweis für nicht vorhandene Strände oder Einrichtungen.', '']
    (ROOT/'docs/10-quellenregister.md').write_text('\n'.join(source_lines))
    print(f'Rendered {len(s)} spot sheets and {sum(map(len,all_variants.values()))} stage sheets.')


if __name__ == '__main__':
    main()
