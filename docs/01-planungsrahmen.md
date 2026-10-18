# Planungsrahmen und noch offene Entscheidungen

Stand: 18.10.2026. Die folgenden Zahlen sind Vorgaben, Rechenergebnisse oder ausdrücklich bezeichnete Vorschläge; keine bereits validierten Etappen.

## Bereits vorgegeben

| Thema | Vorgabe |
|---|---|
| Vorhaben | Sardinien komplett und unabhängig mit dem Wingfoil umrunden |
| Tagesumfang | Bis ca. 5 Stunden auf dem Wingfoil |
| Pausen | 2–3 pro Fahrtag |
| Geschwindigkeit | Ca. 25 km/h |
| Nachtziel | Landepunkt mit Strandhotel in der Nähe |
| Versorgungskategorien | Nur Rast; Getränkekauf; Übernachtung |
| Reisezeit | Voraussichtlich September; Jahr nicht genannt |
| Hotelöffnung | Nicht untersuchen; für die Planung als geöffnet annehmen |
| Ergebnis | Markdown-Dateien mit Quellen; APIs bevorzugen |
| Phase 2 | Simulation auf Basis historischer Winddaten |

## Vorschläge für den ersten Entwurf

Diese Annahmen können für einen Entwurf verwendet werden, gelten aber noch nicht als Entscheidungen der Reisenden.

| Parameter | Vorschlag | Grund |
|---|---|---|
| Bedeutung der 5 Stunden | Reine Fortbewegungszeit auf dem Wasser, einschliesslich langsamer Phasen | Pausen und Materialhandling separat bilanzieren |
| 25 km/h | Nominalwert für die Rechnung bei geeigneten Bedingungen | Noch keine belastbare Geschwindigkeit bei Gegenwind, Welle oder Gepäck |
| Zieldistanz | Zunächst 80–100 km pro Fahrtag | Bei 25 km/h verbleiben 1–1,8 Stunden bis zum 5-Stunden-Budget |
| Pausendauer | 20–30 Minuten je Pause | Landen, Material ablegen, Einkauf und Wiederstart zusätzlich erfassen, soweit nicht enthalten |
| Hotelentfernung | Bevorzugt bis 500 m, höchstens 1 km tatsächlicher Fussweg | Luftlinie bildet Tragestrecke und Umwege nicht ab |
| Getränkekauf | Bevorzugt bis 300 m, höchstens 500 m tatsächlicher Fussweg | Mit einer kurzen Pause vereinbar; Wasserreserve bleibt separat zu planen |
| Übernachtung | Hotels bevorzugen; B&B nur als ausdrücklich bezeichnete Alternative | Entspricht dem gewünschten Strandhotel-Konzept |
| Unabhängigkeit | Kein Begleitboot, kein Begleitfahrzeug, kein Gepäcktransfer; Material selbst mitführen | Muss zur tatsächlichen Ausrüstung und Gruppenorganisation passen |
| Umfang der Runde | Hauptinsel als Arbeitsumfang, vorgelagerte Inseln als separate Varianten | Inseln, verbundene Inseln und Buchtquerungen ausdrücklich festlegen |
| Richtung | Beide Richtungen als Varianten erhalten | Eine Windoptimierung erfolgt erst in Phase 2 |
| Tageslicht | Ankunftsreserve vor Sonnenuntergang vorsehen | Konkrete Reserve und Datum sind noch festzulegen |

Die Entfernungsgrenzen sind Präferenzen, keine recherchierten Eigenschaften von Orten. Werden sie überschritten, wird eine Lücke oder Ausnahme ausgewiesen und kein passender Fussweg erfunden.

## Zeit und Entfernung

Nominal gilt: `Fahrzeit in Stunden = tatsächlich geplanter Wasserweg in km / 25`.

| Wasserweg | Nominale Fahrzeit | Verbleibend bis 5 h |
|---|---:|---:|
| 80 km | 3 h 12 min | 1 h 48 min |
| 100 km | 4 h | 1 h |
| 125 km | 5 h | 0 |

125 km sind damit eine rechnerische Obergrenze bei konstantem Tempo, kein tägliches Soll. Die Reserve ist lediglich eine Budgetreserve; sie belegt keine Fahrbarkeit.

Zwei Pausen teilen einen Tag in drei Fahrabschnitte; drei Pausen in vier. Bei 100 km sind das im Mittel etwa 33 bzw. 25 km pro Abschnitt. Die realen Haltepunkte müssen sich nach geeigneten Küstenabschnitten richten. Zusätzliche Ausweichlandeplätze werden unabhängig von diesen Pausen gesucht.

Bei fünf reinen Fahrstunden plus 2–3 Pausen von je 20–30 Minuten entstehen **5 h 40 min bis 6 h 30 min**, zuzüglich noch nicht enthaltener Rüst- und Tragzeiten. Falls fünf Stunden dagegen das gesamte Tagesfenster meinen, bleiben mit denselben Pausen nominal nur **87,5–108,3 km**, noch vor zusätzlichen Rüstzeiten und Reserven.

25 km/h Fahrgeschwindigkeit sind bei Kreuzen nicht automatisch 25 km/h Fortschritt zum Ziel. In Phase 1 werden Küstenumwege, Kaps und Anlandungen über eine Wasserweg-Geometrie erfasst. In Phase 2 kommen Windwinkel, mögliche Kreuzschläge, Strömung, Starten und langsame Phasen hinzu. Ein Luftlinienabstand oder die veröffentlichte Küstenlänge ersetzt diese Rechnung nicht.

## In den Prompt aufzunehmende Entscheidungen

| Entscheidung | Präzisierung |
|---|---|
| Start und Ende | Fester Ort oder Auswahl aus mehreren Startorten? Muss der Endpunkt exakt identisch sein? |
| Reisedatum | September welchen Jahres; grobes Startfenster; wie viele Kalendertage und Reservetage stehen zur Verfügung? |
| Zeitbudget | Fünf Stunden reine Fahrzeit oder inklusive Pausen, Tragen und Auf-/Abbau? |
| Umrundungsdefinition | Hauptinsel; Umgang mit vorgelagerten/verbundenen Inseln; Buchten ausfahren oder queren; maximale offene Querung |
| Küstenabstand | Persönliche maximale Entfernung zum erreichbaren Land |
| Unterbrechungen | Sind Landtransfers ausschliesslich zum Abbruch erlaubt? Unterbrochene Wasserabschnitte nicht als absolviert zählen |
| Team und Material | Personenanzahl, Können, Boardvolumen, Mastlänge, Wings, Gepäckgewicht, Tragbarkeit, Verhalten bei Flaute |
| Betriebsgrenzen | Persönlicher Windbereich, Böengrenze, Wellen-/Shorebreakgrenze, mögliche Kurse zum Wind, Wiederstartfähigkeit mit Gepäck |
| Versorgung | Maximale Distanz/Zeit zwischen erreichbaren Ausstiegen und zwischen Wasser-/Essensnachschub; mitgeführte Vorräte |
| Übernachtung | Maximale Tragestrecke, Hotelbudget, Zimmerzahl, akzeptierte Unterkunftsarten |
| Alternativen | Kürzere Etappen, Wartetage, Rückzug zum letzten geeigneten Ort; Transport zum Abbruch separat ausweisen |

Für fehlende Komfortpräferenzen dürfen gekennzeichnete Annahmen verwendet werden. Fehlende persönliche Wind-, Wellen-, Querungs- und Autonomiegrenzen bleiben offene Parameter. Sie dürfen nicht durch vermeintlich allgemeingültige Sicherheitswerte ersetzt werden.

## Vorgehen in Phase 1

1. Küste in lückenlos anschliessende Rechercheabschnitte gliedern; Abschnittsgrenzen und Abdeckung dokumentieren.
2. Strände und andere potenzielle Ausstiege über APIs sammeln; Namen und Geometrien abgleichen, Dubletten zusammenführen.
3. Jeden Kandidaten auf Landen, Aufenthalt, erneutes Starten und Versorgung untersuchen; Quellen verlinken.
4. Erst ein Netz geeigneter Nachtziele mit Hotels bilden; danach 2–3 Pausen und zusätzliche Ausweichlandeplätze zwischen den Nachtzielen einfügen.
5. Wasserwege zwischen den Punkten zeichnen, gegen die Küstengeometrie prüfen und ihre Länge berechnen. Keine automatischen Geraden durch Land oder Strassenrouten verwenden.
6. Für beide Fahrtrichtungen eine vollständige Kette zurück zum Ausgangspunkt aufstellen. Fehlende Hotelabdeckung oder zu lange Abschnitte sichtbar lassen und mit kürzeren Varianten bearbeiten.
7. Jede Etappe mit Distanz, Zeitrechnung, Versorgung, längstem Abschnitt ohne geeigneten Ausstieg und verkürzbarer Alternative dokumentieren.

Phase 1 ist inhaltlich abgeschlossen, wenn die gesamte definierte Runde abgedeckt ist, jeder geplante Stopp einen Steckbrief hat, jedes Nachtziel ein namentlich belegtes erreichbares Hotel besitzt und offene Prüfungen transparent ausgewiesen sind. Ein recherchierter Entwurf mit offenen Fahrbarkeitsfragen ist als solcher zu kennzeichnen.

## Übergabe an Phase 2

Stabile IDs für Orte und Wasserabschnitte, Koordinaten, Segmentrichtungen, Land-/Wasserlage der Wetterpunkte und Bedingungen für Start und Landung bereits jetzt erfassen. Historische Wetterdaten als zusammenhängende Stundenfolgen mehrerer September auswerten; Wartetage und wechselnde Etappenlängen berücksichtigen. Startjahr und Umfang der historischen Stichprobe gesondert festlegen.

Das spätere Geschwindigkeitsmodell muss Fahrgeschwindigkeit und Fortschritt entlang der Route unterscheiden. Wellen und Strömung beeinflussen die Bewertung zusätzlich. Modelle können lokale Abschattung, Kap-Effekte und Brandung nur begrenzt abbilden; hierfür sind separate Ortsbelege erforderlich. Quellen und konkrete Datensatzgrenzen stehen im [Quellenverzeichnis](03-datenquellen.md).
