# Arbeitsauftrag für Phase 1

Der folgende Prompt ist zur anschliessenden vollständigen Recherche gedacht. Er wurde hier noch nicht als Routenauftrag ausgeführt. Angaben in eckigen Klammern sind offene Entscheidungen; die genannten Entwurfsannahmen sind Vorschläge.

---

Plane eine vollständige, zusammenhängende Umrundung Sardiniens mit dem Wingfoil. Bearbeite jetzt Phase 1: Landeplätze systematisch recherchieren und bewerten, Tagesetappen mit Übernachtung und 2–3 Pausen pro Fahrtag planen. Phase 2 wird später historische Winddaten und ergänzende Wellen-/Strömungsdaten zur Simulation nutzen. Bereite die dafür notwendigen Orts- und Routendaten bereits vor, ohne jetzt eine Windstatistik oder wetteroptimierte Fahrbarkeit zu behaupten.

## Vorgaben und offene Parameter

- Wir reisen unabhängig. Arbeitsannahme: kein Begleitboot, kein Begleitfahrzeug, kein Gepäcktransfer; alle Ausrüstung wird mitgeführt.
- Geschwindigkeit: nominell 25 km/h bei geeigneten Bedingungen. Unterscheide Fahrtgeschwindigkeit und tatsächlichen Fortschritt entlang der Route, besonders beim Kreuzen.
- Tagesbudget: bis ca. 5 Stunden auf dem Wasser. Bis zur Präzisierung als reine Fortbewegungszeit einschliesslich langsamer Phasen behandeln. Pausen, Tragestrecken, Einkauf und Rüstzeiten separat ausweisen.
- Plane zunächst bevorzugt 80–100 km pro Tag. 125 km sind nur die rechnerische Obergrenze bei 25 km/h über fünf Stunden; keine Pflichtdistanz. Kürzere Etappen sind bei begründeter Ortslage erwünscht.
- Pro Fahrtag 2–3 geplante Pausen, als vorläufige Annahme je 20–30 Minuten. Erfasse zusätzliche Ausweichlandeplätze unabhängig von der Anzahl der Pausen.
- Jedes Nachtziel braucht ein namentlich belegtes, vom konkreten Landepunkt erreichbares Strandhotel. Vorläufig bevorzugt bis 500 m und höchstens 1 km tatsächlicher Fussweg. Luftlinie reicht nicht. B&B und andere Unterkünfte nur als ausgewiesene Alternativen führen.
- Suche Getränkekauf bevorzugt innerhalb von 300 m, höchstens 500 m tatsächlichem Fussweg vom Landepunkt. Diese Radien sind Entwurfsannahmen.
- Startzeitraum: September [Jahr und Startfenster offen]. Hotel-Saisonöffnung und Zimmerverfügbarkeit nicht prüfen; Hotels als geöffnet annehmen.
- Start-/Endort: [offen; bei fehlender Festlegung geeignete Startorte anhand Erreichbarkeit, Hotels und Routenanschluss vergleichen].
- Geografischer Umfang: [Hauptinsel; Umgang mit vorgelagerten und verbundenen Inseln sowie Buchtquerungen offen]. Eine geschlossene Runde zum Ausgangspunkt ausweisen; zusätzliche Inselvarianten separat führen.
- Fahrtrichtung: beide Richtungen als Varianten erhalten. In Phase 1 nach Infrastruktur und Wasserweg beurteilen, noch keine windoptimale Richtung bestimmen.
- Reisedauer, Wartetage, Hotelbudget, Zimmerzahl, maximale Tragestrecke: [offen].
- Personen, Erfahrung, Boardvolumen, Mastlänge, Winggrössen, Gepäckgewicht und Wiederstartfähigkeit: [offen].
- Persönliche Grenzen für Wind/Böen, Welle/Shorebreak, Küstenabstand, offene Querungen und längste Abschnitte ohne Ausstieg bzw. Versorgung: [offen]. Erfinde dafür keine vermeintlich sicheren Standardwerte.

Führe offene Entscheidungen zentral. Arbeite bei fehlenden Komfortangaben mit transparenten Entwurfsannahmen weiter. Wenn eine fehlende Information die eigentliche Machbarkeit bestimmt, formuliere die konkrete Rückfrage früh und recherchiere parallel unabhängig davon mögliche Orte und Quellen weiter. Unterstellte Werte dürfen nicht als Nutzerentscheidungen erscheinen.

Zugang und Regeln, Materiallogistik im Hotel sowie eine gesonderte Bewertung der Belegqualität sind auf Wunsch nicht Gegenstand der Recherche. Quellenlinks weiterhin dokumentieren.

## Landeplätze untersuchen

Nutze das vorhandene Bewertungsschema und die Steckbriefvorlage. Führe Rast, Getränkekauf, Trinkwassernachfüllung und Übernachtung als unabhängige Felder mit `ja/nein/unbekannt`. Leite daraus R, G und Ü ab. Übernachtung impliziert keinen Getränkekauf; ein fehlender Karteneintrag impliziert kein Nein.

Erfasse je Platz mindestens:

1. Stabile ID, Name, Gemeinde, Küstenabschnitt und WGS84-Koordinaten des konkreten Landepunkts; Wiederstartpunkt bei Abweichung separat.
2. Untergrund, Uferform, nutzbare Fläche, bekannte Felsen/Untiefen, Materialhandling und Foil-Tauglichkeit für die angegebene Mastlänge.
3. Landung und Wiederstart getrennt, jeweils mit passenden Bedingungen oder ungeklärten Punkten.
4. Bucht-/Strandausrichtung, offene Seeseite, Wind-von-Sektoren, Wellen-/Dünungsexposition, Shorebreak, Strömungen und Abschattungshinweise. Geometrische Ableitung von Ortsbeobachtung unterscheiden.
5. Namen und Quellen der Verkaufsstellen/Hotels; tatsächliche Fusswege inklusive Stufen und Umwegen.
6. Ausstieg/Rückzug bei Flaute, alternative Landeplätze und Distanz zum nächsten geeigneten Ort entlang der Wasserroute.
7. Direkte Quellenlinks für die recherchierten Angaben.

Bewerte technische Eignung unabhängig von Versorgung: A regulär unter genannten Bedingungen, B bedingt, C nur als belegte Ausstiegs-/Rückzugsoption unter genannten Bedingungen, X ausgeschlossen, ? noch nicht bewertbar. Keine Gesamtnote, die technische Hindernisse durch Hotelkomfort ausgleicht. Unbekannte Kernmerkmale verhindern eine belastbare A-Einstufung.

## Quellen und APIs

Beginne mit den dokumentierten Quellen in `docs/03-datenquellen.md`. Verwende nach Möglichkeit Overpass/OSM für Kandidaten und Infrastruktur sowie die regionalen Geodienste für Küstengeometrien. Prüfe Hotels mit geeigneten direkten Quellen. API-Daten sind Ausgangsmaterial, keine automatische Bestätigung der Eignung.

Beziehe Daten in angemessen grossen Gebietsabfragen, verwende einen Cache, vermeide doppelte Abfragen und behandle Rate-Limits und unvollständige Ergebnisse ausdrücklich. Speichere Abfrage, Abrufzeit, Datenstand, Rohantwort, Objekt-/Layer-ID und Lizenz. Nutze bei nicht verfügbaren APIs nachvollziehbar eine andere Quelle und dokumentiere die Lücke. Kein unbekannter Wert darf stillschweigend zu Null, Nein oder geeignet werden.

Bei Wind- und Wellendaten jetzt nur die spätere Schnittstelle vorbereiten. Keine historische Simulation ausführen. Beachte bereits bei der Datenauswahl, dass grobe Tiefen- und Wetterraster keine einzelnen Untiefen, lokalen Böen oder Strandbrandung zuverlässig beschreiben.

## Etappen bilden

Erstelle zunächst ein möglichst vollständiges Netz von Landeplätzen entlang der gesamten definierten Runde. Wähle daraus Nachtziele und ergänze Pausen sowie kürzere Varianten und Ausweichlandeplätze. Eine zufällige Liste touristischer Strände reicht nicht.

Dokumentiere pro Etappe:

- Start, 2–3 Pausen, Nachtziel und zugehörige Landeplatz-IDs in Reihenfolge.
- Geografisch plausible Wasserweg-Polyline; Küstenumwege, Kaps, An-/Abfahrt und offene Querungen berücksichtigen. Keine Verbindungslinie durch Land. Kürzeste Luftlinie und tatsächlichen Wasserweg nicht vermischen.
- Distanz jeder Teilstrecke, Gesamtdistanz und nominale Fahrzeit `Distanz / 25`; Pausen-/Rüst-/Tragzeit zusätzlich. Rest des 5-Stunden-Budgets und Tageslichtreserve getrennt ausweisen.
- Geplante Versorgung und längste Abschnitte ohne bestätigte Nachfüll-/Kaufmöglichkeit bzw. ohne geeigneten Ausstieg. Persönliche Grenzwerte prüfen, sobald vorliegend.
- Konkretes Hotel am Nachtziel und möglichst eine belegte Alternative. Falls keine Alternative existiert, diese Abhängigkeit benennen.
- Kürzeres Ziel bzw. Abbruchoption vor schwierigen Abschnitten; zusätzliche Entfernung und deren Bedingungen ausweisen. Keine jederzeit sichere Notlandung behaupten.
- Offene technische Fragen sowie Wirkung auf die Etappe. Ein Landtransfer zum Abbruch schliesst keine Lücke einer vollständigen Wasserumrundung.

Kann ein Abschnitt die Bedingungen nicht erfüllen, markiere eine Machbarkeitslücke mit Ursache und Varianten. Erfinde keine Hotels, Fusswege oder Landemöglichkeiten, um eine geschlossene Route zu erhalten. Weise aus, ob eine Route ein vollständiger Entwurf oder eine unter den festgelegten Parametern plausibilisierte Variante ist.

## Ergebnisse und Abnahme

Dokumentiere alle fachlichen Ergebnisse auf Deutsch in Markdown mit direkten Quellenlinks:

- Aktualisierte Übersicht und Annahmen-/Entscheidungsliste.
- `docs/05-landeplaetze-index.md`: alle untersuchten Kandidaten, Versorgung, Eignung, Zuordnung zu Küstenabschnitten.
- `landeplaetze/<stabile-id>.md`: ein vollständiger Steckbrief pro Kandidat; Ausschlüsse mit Grund behalten.
- `docs/06-routenvarianten.md`: geschlossene Reihenfolge, Summen, Richtungsvarianten und räumliche Abdeckung einschliesslich Lücken.
- `etappen/<variante>-<nummer>.md`: ein Dokument je Etappe gemäss Vorlage.
- `docs/07-offene-pruefungen.md`: priorisierte technische und planerische Fragen sowie betroffene Orte/Etappen.
- `docs/08-phase-2-uebergabe.md`: Orts-/Segment-IDs, Geometrien, Bedingungen, Parameter und offene Anforderungen an die Simulation.
- Aktualisiertes Quellenverzeichnis. Rohdaten und maschinenlesbare Geometrien ergänzend speichern; eine Übersichtskarte mit Quellen/Legende ergänzen, wenn technisch möglich.

Prüfe abschliessend: lückenlose Verbindung zum Startpunkt, richtige Summen, 2–3 Pausen pro geplanten Fahrtag, Beachtung des Zeitbudgets, Hotelnachweise und Fusswege je Nachtziel sowie Bedingungen und Quellen aller geplanten Stopps. Überschreitungen und ungeklärte Punkte explizit ausweisen. Datenlücken dürfen im Abschlussbericht nicht als abgeschlossene Prüfung erscheinen.
