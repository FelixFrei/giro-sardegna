# Bewertung der Landeplätze

Stand: 18.10.2026. Dieses Schema ist ein Planungsvorschlag, kein bereits angewendetes Prüfsiegel.

## Versorgung und Eignung getrennt erfassen

Die drei gewünschten Versorgungskategorien werden aus unabhängigen Feldern abgeleitet:

| Feld | Werte | Bedeutung |
|---|---|---|
| `rast_moeglich` | ja / nein / unbekannt | Aufenthalt mit abgelegtem Material möglich |
| `getraenke_kauf` | ja / nein / unbekannt | Konkrete erreichbare Verkaufsstelle vorhanden |
| `trinkwasser_nachfuellen` | ja / nein / unbekannt | Als Trinkwasser belegte Nachfüllmöglichkeit; nicht aus einer Dusche ableiten |
| `hotel_erreichbar` | ja / nein / unbekannt | Namentlich belegtes Hotel innerhalb der gewählten Fussweggrenze |
| `essen_kauf` | ja / nein / unbekannt | Konkrete Möglichkeit für Mahlzeit oder Vorräte |

- **R – nur Rast:** Rast möglich, Getränkekauf und Hotel nach Recherche nicht vorhanden bzw. ausserhalb des definierten Radius.
- **G – Getränkekauf:** Verkaufsstelle belegt; Hotelstatus separat anzeigen.
- **Ü – Übernachtung:** Hotel und tatsächliche Erreichbarkeit belegt; Getränkekauf nicht automatisch unterstellen.
- **Offen:** Ungeklärte Versorgung bleibt sichtbar, z. B. `Rast ja; G unbekannt; Ü unbekannt`. Ein fehlender OSM-Eintrag belegt kein Nein.

Bei mehreren belegten Funktionen werden sie zusammen angezeigt, etwa `R + G + Ü`. Ein Hotel-POI allein liefert zunächst nur einen Unterkunftskandidaten. Ein solcher Kandidat ist noch kein bestätigtes Nachtziel und sagt nichts über die Wingfoil-Eignung des Strandes aus.

## Welche Angaben pro Ort festhalten?

| Bereich | Pflichtangaben | Nutzen |
|---|---|---|
| Identität | Stabile ID, Name/Alias, Gemeinde, Küstenabschnitt, WGS84-Koordinaten | Wiederfinden und eindeutige Quellenzuordnung |
| Geometrie | Konkreter Landepunkt, möglicher Startpunkt, nutzbarer Strandabschnitt | Strandmittelpunkt ist kein belegter Ausstieg |
| Untergrund | Sand/Kies/Fels, Hindernisse am Ufer und im Wasser, Gefälle, nutzbare Breite | Material ablegen und Ein-/Ausstieg beurteilen |
| Foil-Tauglichkeit | Bekannte Untiefen/Felsen, ausreichende Wassertiefe für konkreten Mast, Weg bis zum Startbereich | Mastlänge und Gepäck berücksichtigen; Tiefe mit Quelle oder unbekannt |
| Landen und Wiederstart | Getrennte Beurteilung; nötiges Tragen, Aufbauen, Raum für den Wing | Ein Ausstieg kann möglich sein, obwohl kein Wiederstart möglich ist |
| Wind | Ausrichtung der Bucht, offene Seeseite, geeignete/ungeeignete Wind-von-Sektoren, Abschattungshinweise | Spätere Verknüpfung mit der Simulation |
| Wellen | Exposition, belegte Brandung/Shorebreak, Dünungsrichtung, bekannte Strömungen | Bedingungen an der Anlandung gesondert erfassen |
| Getränke und Essen | Name, Art, Position, belegtes Angebot, tatsächlicher Fussweg und Wegqualität | Nutzbare Versorgung statt blosser Nähe |
| Hotel | Name, Website, Lage, tatsächlicher Fussweg, Stufen/Umwege, Strandlage | Tragestrecke zum Etappenziel beurteilen |
| Rastkomfort | Schatten, WC, Dusche, geschützter Ablageplatz | Ergänzende Komfortmerkmale |
| Rückzug | Ausstieg bei Flaute, alternative Landeplätze, Kommunikations-/Hilfsmöglichkeiten | Optionen bei einer verkürzten Etappe erfassen |
| Nachbarorte | Vorheriger/nächster geeigneter Stopp, Entfernung auf Wasserweg, alternative Anlandung | Lücken zwischen Landemöglichkeiten erkennen |

Hotelöffnungszeiten, Saisonöffnung und aktuelle Zimmerverfügbarkeit sind ausdrücklich nicht Teil dieser Recherche. Öffnungszeiten von Verkaufsstellen werden in diesem Strukturentwurf ebenfalls nicht als garantierte Versorgung zu einer konkreten Uhrzeit behandelt.

## Eignung mit Bedingungen statt einer Gesamtnote

| Klasse | Bedeutung im Entwurf |
|---|---|
| A | Als regulärer Stopp technisch geeignet innerhalb ausdrücklich beschriebener Bedingungen |
| B | Bedingt geeignet; konkrete Einschränkung und dafür notwendige Bedingung benennen |
| C | Als regulärer Stopp ungeeignet, aber ein belegter Ausstieg/Rückzug kann unter beschriebenen Bedingungen möglich sein; Wiederstart nicht voraussetzen |
| X | Für den betrachteten Zweck ausgeschlossen, mit konkretem Grund und Beleg |
| ? | Entscheidende Angaben fehlen oder widersprechen sich; noch nicht belastbar bewertbar |

Die Einstufung erfolgt für Landen und Wiederstart getrennt und, wo nötig, pro Fahrtrichtung/Wetterbedingung. Sie ist keine wetterunabhängige Eigenschaft eines Strandes. C bedeutet keine Garantie eines jederzeit nutzbaren Notausstiegs.

**Zuerst technische Eignung und offene Kernfragen prüfen, dann Komfort vergleichen.** Ein ungeeigneter Uferausstieg oder unvereinbare Wind-/Wellenbedingungen dürfen nicht durch Hotelnähe oder Gastronomie ausgeglichen werden. Bei unbekannten entscheidenden Hindernissen bleibt der Ort ein Kandidat der Klasse `?`, bis die Frage geklärt ist.

Unter geeigneten Kandidaten bevorzugen: einfacher Ein-/Ausstieg, funktionierender Wiederstart, kurze Tragestrecke, robuste Versorgung und mehrere Alternativen in erreichbarer Entfernung. Für den ersten Entwurf genügt diese begründete Reihenfolge; eine frei gewichtete 0–100-Gesamtnote würde Genauigkeit vortäuschen.

## Quellen

Die verwendeten Quellen werden direkt verlinkt. Fehlende Informationen bleiben als unbekannt gekennzeichnet. Allgemeine Tiefenraster liefern keine ausreichende Auflösung für einzelne Foil-Hindernisse; siehe [EMODnet im Quellenverzeichnis](03-datenquellen.md).

## Geodaten-Konventionen

- Koordinaten im Steckbrief als `latitude`, `longitude` in WGS84; GeoJSON verwendet dagegen `[longitude, latitude]`.
- Entfernungen mit Methode angeben: geodätische Länge einer Wasserweg-Polyline, tatsächlicher Fussweg oder ausdrücklich nur vorläufige Luftlinie.
- Windrichtung bezeichnet die Richtung, **aus der** der Wind kommt: 0° Nord, 90° Ost. Wasserweg-Kurs bezeichnet die Bewegungsrichtung. Nicht verwechseln.
- Die offene Seeseite einer Bucht kann als Richtung vom Strand hinaus aufs Meer angegeben werden. Geometrisch abgeleitete Exposition ist noch kein belegter nutzbarer Windsektor.
- Keine Nachkommastellen als Ersatz für Genauigkeit: Herkunft und Unsicherheit eines Landepunkts angeben.

Das [Steckbrief-Template](../templates/landeplatz.md) setzt dieses Schema um. Externe Datenquellen sind in [Datenquellen und APIs](03-datenquellen.md) belegt; die Kategorien und Planungsgrenzen sind eigene Vorschläge.
