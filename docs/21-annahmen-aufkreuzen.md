# Annahmen für Aufkreuzen und Wind aus allen Richtungen

Stand: 19.10.2026. Grundlage für die [Umrundungssimulation mit Aufkreuzen](22-umrundung-mit-aufkreuzen.md). Weiterhin 12–25 kn, historische August–Oktober-Daten 2022–2025, beide Fahrtrichtungen, Hotelziele und Land-Wartepausen.

## Grundidee

Alle Windrichtungen können grundsätzlich genutzt werden. Direkt gegen den Wind wird weiterhin nicht gefahren: Die Gruppe kreuzt auf zwei fahrbaren Kursen. Die Zeit ergibt sich aus der tatsächlich gefahrenen Strecke, der Geschwindigkeit auf diesen Kursen und Manöververlusten. Entscheidend für das Etappenziel ist der Fortschritt entlang der geplanten Route, nicht die GPS-Geschwindigkeit auf dem einzelnen Schlag.

Diese Zahlen sind bewusst gewählte, plausible Arbeitsannahmen für erfahrene Freeride-Wingfoiler. Sie sind weder eine gemessene Leistungskurve der Gruppe noch wissenschaftlich belegte Durchschnittswerte. Material, Fahrergewicht, Können, Beladung und Seegang beeinflussen die Leistung. Die bisherige konstante Annahme von 25 km/h entfällt.

## Basisannahmen beim direkten Aufkreuzen

Windklassen: 12 bis unter 15 kn, 15 bis unter 20 kn, 20 bis einschliesslich 25 kn. Winkel immer relativ zur Wind-von-Richtung, 0° wäre direkt gegen den Wind.

| Wind | Amwindwinkel je Schlag | Fahrt auf dem Schlag | Faktor für Manöver und erneutes Anfahren | Effektiver Fortschritt direkt gegen den Wind |
|---|---:|---:|---:|---:|
| 12–<15 kn | 60° | 16 km/h | 0,85 | 6,8 km/h |
| 15–<20 kn | 55° | 20 km/h | 0,85 | 9,8 km/h |
| 20–25 kn | 55° | 18 km/h | 0,85 | 8,8 km/h |

Berechnung bei direkt gegen den Wind liegendem Ziel:

`Fortschritt = Geschwindigkeit auf dem Schlag × cos(Amwindwinkel) × 0,85`

Beispiel bei 18 kn Wind: `20 × cos(55°) × 0,85 = 9,75 km/h`. Ein 30 km entferntes Ziel direkt gegen den Wind benötigt damit rund **3,1 Stunden** und etwa **52,3 km tatsächlich gefahrenen Weg**. Bisher wären dafür nur 1,2 Stunden angesetzt worden.

Der Faktor 0,85 reduziert die effektive Geschwindigkeit um 15 %; die Fahrzeit steigt dadurch um rund 17,6 %. Er bildet Manöver und Wiederanfahren pauschal ab. Keine zusätzlichen pauschalen Wendeminuten darüberlegen, sonst würden Verluste doppelt gezählt. Die geringere Geschwindigkeit in der obersten Windklasse ist eine vorsichtige Modellentscheidung für längere Touren, keine aus Winddaten abgeleitete Wellenprognose.

## Andere Kurse und Wind von hinten

Als grobe Zielwerte für das Basisszenario:

| Kurs / Fortschritt Richtung Ziel | 12–<15 kn | 15–<20 kn | 20–25 kn |
|---|---:|---:|---:|
| Direkt gegen den Wind, mit Kreuzen | 6,8 km/h | 9,8 km/h | 8,8 km/h |
| Direkt fahrbar, schräg gegen den Wind bei 70° | 16 km/h | 20 km/h | 18 km/h |
| Halbwind, 90° | 20 km/h | 25 km/h | 23 km/h |
| Raumwind, 120° | 22 km/h | 26 km/h | 24 km/h |
| Direkt nach Lee, mit schrägen Kursen und Halsen | 13,3 km/h | 16,2 km/h | 14,7 km/h |

Für den letzten Eintrag werden zwei Kurse bei 145° zur Wind-von-Richtung angenommen: Fahrtgeschwindigkeit 18/22/20 km/h, Halsenfaktor 0,90. Fortschritt direkt nach Lee: `Fahrtgeschwindigkeit × cos(35°) × 0,90`. Damit wird auch achterlicher Wind nicht automatisch mit 25 km/h Richtung Ziel gerechnet. Die Werte gelten ohne zusätzlich angenommenen Schub durch Wellen.

Die Tabelle ist eine grobe Parametrisierung, keine fertige kontinuierliche Polare. Für die Umsetzung werden die Geschwindigkeiten zwischen fahrbaren Kursen interpoliert. Innerhalb des nicht direkt fahrbaren Amwindsektors werden die beiden Schläge kombiniert. Die Formel für ein exakt gegen den Wind liegendes Ziel darf nicht unverändert auf jeden schrägen Kurs übertragen werden.

Bei konstantem Wind, symmetrischen Schlägen und einem Zielwinkel α kleiner als dem Amwindwinkel θ gilt idealisiert:

`Gesamtstrecke = Zielentfernung × cos(α) / cos(θ)`

Die einzelnen Schlaglängen müssen zusammen die gewünschte Zielrichtung ergeben. Der Manöverfaktor fällt beim Kreuzen an; für einen direkt fahrbaren Kurs wird er nicht automatisch angesetzt. Nahe der Grenze sollte die Umsetzung direkte Fahrt und Kreuzen vergleichen, statt einen künstlichen Geschwindigkeitssprung zu erzwingen.

## Unsicherheit: drei ausdrücklich hypothetische Szenarien

| Szenario | Amwindwinkel gegenüber Basis | Geschwindigkeit auf den Schlägen | Manöverfaktor | Fortschritt direkt gegen den Wind bei 15–<20 kn |
|---|---|---|---:|---:|
| Vorsichtig | jeweils +5° | jeweils −15 % | 0,80 | 6,8 km/h |
| Basis | 60° bei wenig Wind, sonst 55° | 16/20/18 km/h | 0,85 | 9,8 km/h |
| Günstig | jeweils −5° | Basisgeschwindigkeit | 0,90 | 11,6 km/h |

Diese Spanne ersetzt eine vorgetäuschte Genauigkeit. Eigene GPS-Tracks mit Windrichtung und Windstärke können später die Winkel, Geschwindigkeiten und tatsächlichen Manöververluste ersetzen. Einzelne Spitzengeschwindigkeiten reichen dafür nicht; relevant ist der anhaltende Fortschritt inklusive Wenden und Wiederanfahren.

## Tagesplanung und technische Umsetzung

- Maximal fünf Stunden aktive Zeit auf dem Wasser, einschliesslich Wenden, Halsen, Anfahren und darin berücksichtigter Verluste. Landpausen und Warten an Land sind zusätzlich möglich, weiterhin innerhalb 09–17 Uhr.
- Bei fünf Stunden ausschliesslichem Aufkreuzen ergeben sich im Basisszenario rund 34–49 km Fortschritt. Gemischte Tage werden abschnittsweise gerechnet; daraus folgt kein allgemeines Tagesdistanzversprechen.
- Hotel am Tagesziel bleibt Voraussetzung. Die bisherigen 50/75/125-km-Limits können zusätzliche Vergleichsobergrenzen bleiben, ersetzen aber niemals die neu berechnete Zeitgrenze.
- Windstärke weiterhin 12–25 kn, keine zusätzliche Böengrenze. Wind muss während der längeren Passage passen; bisher erfolgreiche Fahrten können wegen der längeren Dauer nun scheitern.
- Bei wechselndem Wind werden Fortschritt und Uhrzeit in kurzen Zeitschritten gemeinsam aktualisiert. Eine nachträgliche Zeitmultiplikation alter Fahrten reicht nicht.
- Die tatsächlichen Kreuzschläge brauchen Platz auf dem Wasser. Ein rechnerischer VMG-Abschlag entlang der alten Linie allein ist noch keine geografisch fahrbare Route. Küstenquerungen durch gedachte Zickzacklinien dürfen nicht erlaubt werden; verfügbare Wasserfläche und Wind auf den Schlägen müssen berücksichtigt werden.

Das Modell sollte Ergebnisse zunächst als Bandbreite aus vorsichtigem und Basisszenario zeigen. Ohne persönliche Leistungsdaten ist eine einzelne Variante noch keine verlässlich realistische Vorhersage.

## Quellen und Abgrenzung

Quellen gelesen am 19.10.2026:

- [Foil Run: What is VMG?](https://foil.run/help/vmg): erläutert die Projektion `Geschwindigkeit × cos(Winkel)` und unterscheidet den Fortschritt auf geraden Schlägen vom Fortschritt inklusive Manövern. Die Beispiele der Seite sind keine Messwerte der hier geplanten Gruppe. **Die Formel und das Prinzip der Manöverberücksichtigung sind belegt; unsere Zahlen bleiben Annahmen.**
- [Wingfoil Playa Blanca: How to Ride Upwind](https://wingfoilplayablanca.com/guides/ride-upwind): Schulungsquelle zur Amwindtechnik; nennt als Orientierung engere fahrbare Winkel. Für diese Langstreckenplanung werden bewusst weniger ambitionierte Winkel von 55–60° gewählt. Daraus lässt sich keine garantierte Geschwindigkeit ableiten.
- [Duotone: Wings, Auswahl und Einflussfaktoren](https://www.duotonesports.com/en/uk/wing-foiling/wings): Herstellerinformationen zur Abhängigkeit von Können, Material, Körpergewicht und Windbedingungen. Keine daraus abgeleitete numerische Leistungszusage.

Die vorgeschlagenen Geschwindigkeiten, Winkel, 15-%-Manöverabschläge und Szenariospannen sind eigene Planungsannahmen. Es wurde keine allgemein gültige, empirisch abgesicherte Wingfoil-Tourenpolare für eure konkrete Ausrüstung gefunden. Die Umsetzung und neue Reiseauswertung sind im [Ergebnisbericht](22-umrundung-mit-aufkreuzen.md) beschrieben.
