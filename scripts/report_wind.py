"""Render the wind collection and first simulation results in Markdown."""
from collections import Counter
from datetime import date
import json
from pathlib import Path
import statistics

ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/phase2'


def main():
    data=json.loads((DATA/'simulation-results.json').read_text());coverage=json.loads((DATA/'coverage.json').read_text())
    plan=json.loads((ROOT/'data/phase1/route-plan.json').read_text());names={k:v['name'] for k,v in plan['spots'].items()}
    runs=data['runs'];labels={'flex-ccw':'16 Etappen · gegen Uhrzeigersinn','flex-cw':'16 Etappen · im Uhrzeigersinn','kompakt-ccw':'9 Etappen · gegen Uhrzeigersinn','kompakt-cw':'9 Etappen · im Uhrzeigersinn'}
    finished=sum(x['completed'] for x in runs)
    out=['# Historischer Windvergleich – erster Simulationslauf','','Stand: 18.10.2026. September-Starts 2022–2025, Fortsetzung jeweils bis 31. Oktober. **15–25 kn, Wind seitlich oder von hinten, ohne Kreuzen.**', '',
         f"**Ergebnis: {finished} von {len(runs)} simulierten Reiseverläufen schliessen die Runde bis Ende Oktober ab.**", '',
         ('Alle Verläufe bleiben bereits vor der ersten Tagesetappe am Start: Für diese findet sich kein vollständiges passendes Fenster. ' if all(r['riding_days']==0 for r in runs) else '') + 'Es werden die festen Hotelketten und Pausen aus Phase 1 gefahren. Jeder Septembertag bildet einen eigenen Startversuch. Die Rechnung prüft die ganze Tagesetappe mit den Windwerten zur jeweiligen Passagezeit. Sie verändert weder die Route noch die Hotelziele automatisch. Die 480 Startversuche überlappen zeitlich und sind keine 480 unabhängigen Wetterereignisse.', '',
         '## Datengrundlage', '',
         f"{coverage['request_points']} Abfragepunkte, {coverage['unique_returned_cells']} unterschiedliche zurückgegebene Gitterkoordinaten, {coverage['point_hours']:,} Punktstunden und {coverage['total_nulls']} fehlende Werte. Grösster Abstand zwischen Anfragepunkt und Modellzellenzentrum: {coverage['max_grid_offset_km']:.1f} km. Mehrere Abfragepunkte können dieselbe Modellzelle verwenden.", '',
         '[API-Auswahl, Abfragen, Quellen und Reproduktion](11-wind-api-und-daten.md) · [Abdeckungsbericht](../data/phase2/coverage.json)', '',
         '## Vollständige Reisen nach Variante', '',
         '| Variante | Starts | Bis 30. September fertig | Bis 31. Oktober fertig | Grösster Fortschritt |', '|---|---:|---:|---:|---:|']
    for key,label in labels.items():
        r=[x for x in runs if x['variant']==key]
        out.append(f"| {label} | {len(r)} | {sum(x['completed_in_september'] for x in r)} | {sum(x['completed'] for x in r)} | {max(x['riding_days'] for x in r)} Etappen / {max(x['completed_km'] for x in r):.1f} km |")
    out += ['', '## Vergleich je Jahr', '', '| Jahr | Variante | Abschlüsse September / bis Oktober | Maximale Zahl gefahrener Etappen |', '|---|---|---:|---:|']
    for year in data['config']['years']:
        for key,label in labels.items():
            r=[x for x in runs if x['variant']==key and x['year']==year]
            out.append(f"| {year} | {label} | {sum(x['completed_in_september'] for x in r)} / {sum(x['completed'] for x in r)} von 30 | {max(x['riding_days'] for x in r)} |")
    if not finished:
        out += ['', '**Damit ergibt sich unter diesen Annahmen keine erfolgreiche Vorzugsrichtung.** Das Ergebnis gilt für diese festen Etappen und Zeitfenster; es ist kein Beweis, dass eine windabhängig angepasste Umrundung unmöglich wäre. Eine zusätzliche Monatsreserve allein löst die Engpässe in diesem Lauf nicht.']
    out += ['', '## Wo die Reiseverläufe stehen bleiben', '', '| Variante | Nächste nicht absolvierte Etappe | Ziel | Anzahl Startversuche |', '|---|---:|---|---:|']
    variants=json.loads((ROOT/'data/phase1/variants.json').read_text())
    for key,label in labels.items():
        for stage,count in Counter(x['next_stage'] for x in runs if x['variant']==key and not x['completed']).most_common():
            out.append(f"| {label} | {stage} | {names[variants[key][stage-1]['stops'][-1]]} | {count} |")
    out += ['', '## Erster Ausschlussgrund auf den Startetappen', '',
            'Hier werden die ausprobierten Abfahrtszeiten für die flexiblen Startetappen gezählt. Pro Versuch zählt nur die zuerst verletzte Bedingung; weitere Gründe im späteren Verlauf werden nicht geprüft. Die häufigste erste Ursache ist in diesem Lauf Wind unter 15 kn im Modell.', '',
            '| Richtung | Unter 15 kn | Über 25 kn | Wind von vorne |', '|---|---:|---:|---:|']
    for key in ['flex-ccw','flex-cw']:
        counts=Counter()
        for row in data['stage_feasibility']:
            if row['variant']==key and row['stage']==1:counts.update(row['first_failure_counts'])
        out.append(f"| {labels[key]} | {counts['too_light']} | {counts['too_strong']} | {counts['headwind']} |")
    out += ['', '## Passende lokale Windstunden', '',
            'Die folgende Kennzahl ist der längengewichtete Anteil der Routenstücke mit passendem Wind während 09–17 Uhr Ortszeit. Sie prüft Abschnitte unabhängig voneinander. **Sie ist keine Wahrscheinlichkeit einer erfolgreichen Reise:** passende Stunden können an verschiedenen Orten und Tagen liegen.', '',
            '| Jahr | Monat | Gegen Uhrzeigersinn | Im Uhrzeigersinn |', '|---|---|---:|---:|']
    for row in data['local_wind_availability']:out.append(f"| {row['year']} | {'September' if row['month']==9 else 'Oktober'} | {row['ccw_percent']:.1f} % | {row['cw_percent']:.1f} % |")
    out += ['', '## Etappenfenster', '',
            'Gezählt werden Kalendertage mit mindestens einer passenden Abfahrt für die komplette Etappe. Diese Tage sind unabhängig davon gezählt, ob die Gruppe an diesem Tag bereits am jeweiligen Startort angekommen wäre. Details aller 200 Etappen/Jahr-Kombinationen stehen in den [Rohresultaten](../data/phase2/simulation-results.json).', '',
            '| Flexible Etappe CCW | Ziel | Passende Septembertage / 120 | Zusätzliche Oktobertage / 124 |', '|---|---|---:|---:|']
    for stage in range(1,17):
        rows=[x for x in data['stage_feasibility'] if x['variant']=='flex-ccw' and x['stage']==stage]
        out.append(f"| {stage} | {names[rows[0]['end']]} | {sum(x['feasible_september'] for x in rows)} | {sum(x['feasible_october'] for x in rows)} |")
    out += ['', '## Annahmen für die Einordnung', '',
            '- 25 km/h, maximal fünf Fahrstunden, 25 Minuten pro Pause; Abfahrtssuche alle 30 Minuten zwischen 09 und 15 Uhr, Ankunft bis 17 Uhr.',
            '- Wind-von-Winkel 90–180° relativ zum momentanen Fahrkurs. Auch Richtungswechsel an Kaps und in Buchten zählen. Keine Kreuzschläge oder alternativen Linien.',
            '- Gleiche Route, Wetterdaten und Regeln für beide Richtungen. Nur die Reihenfolge und Fahrkurse werden umgekehrt.',
            '- Unterwegs keine zusätzliche Wartezeit auf Windwechsel; bei fehlendem vollständigem Tagesfenster wird am Hotel gewartet. Frühere Hotelziele werden nur über den separaten flexiblen Etappenplan abgebildet.',
            '- Rückblick mit bekanntem Wetterverlauf, keine Vorhersagesimulation. Wellen, Strömung und Böengrenzen sind nicht Teil dieses Windfilters.', '',
            'Die gewählten Tagesfenster und die feste Hotelkette sind Modellannahmen. Die von euch genannten Windgrenzen bleiben unverändert. Eine weitere Rechnung kann die Hotelziele und Abfahrten dynamischer wählen, ohne daraus neue Detailprüfungen an Land abzuleiten.', '',
            '## Dateien und Prüfungen', '',
            '- [Konfiguration](../data/phase2/simulation-config.json), [alle Reiseverläufe](../data/phase2/simulation-results.json), [Simulationsskript](../scripts/simulate_wind.py).',
            '- [Tests](../scripts/test_wind.py): Wind-von-Konvention, umgekehrte Kurse, Grenzwerte, 359°/1°-Interpolation, Windwechsel unterwegs, fehlende Werte, Pausenzeit, Zeitumstellung und Streckensummen.',
            '- [Datenprüfung](../scripts/validate_wind_data.py): SHA-256, vollständige Stundenfolgen, Einheiten und Zuordnung zur Route.', '',
            'Winddaten: ECMWF / Open-Meteo. Methodik und Quellen im [API-Dokument](11-wind-api-und-daten.md). Alle Prozentwerte und Reiseergebnisse sind eigene Berechnungen.', '']
    out.insert(1, '\nWeiterführung: [Kürzere Tagesetappen mit Wartepausen](13-variable-etappen-wartepausen.md) vergleicht flexible Hotelziele bei unveränderten Windgrenzen.')
    (ROOT/'docs/12-historischer-windvergleich.md').write_text('\n'.join(out))
    print('Wrote docs/12-historischer-windvergleich.md')


if __name__=='__main__':main()
