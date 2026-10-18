---
id: null
variante: null
richtung: null
start_landeplatz_id: null
ziel_landeplatz_id: null
status: entwurf
distanz_km: null
nominale_geschwindigkeit_kmh: 25
fahrzeit_h: null
pausen_min: null
ruest_und_tragezeit_min: null
gesamtzeit_h: null
---

# Etappe: Nummer und Name ergänzen

Vorlage, keine geprüfte Etappe. Wetterunabhängige Strukturplanung; Fahrbarkeit bleibt von den genannten Bedingungen abhängig.

## Ablauf und Zeitrechnung

| Reihenfolge | Rolle | Landeplatz-ID und Link | Wasserweg ab vorigem Punkt, km | Nominale Fahrzeit | Pause / Zusatzzeit | R/G/Ü und Eignung |
|---|---|---|---:|---|---|---|
| 0 | Start | offen | — | — | offen | offen |
| 1 | Pause 1 | offen | offen | offen | offen | offen |
| 2 | Pause 2 | offen | offen | offen | offen | offen |
| 3 | Pause 3, falls geplant | offen | offen | offen | offen | offen |
| 4 | Nachtziel | offen | offen | offen | offen | offen |

Bei zwei Pausen die dritte Pausenzeile entfernen und die Reihenfolge anpassen.

- Wasserweg gesamt: offen; Geometriedatei, Datenquelle und Messmethode: offen.
- Nominale Fahrzeit: `Wasserweg_km / 25`; in Phase 2 durch bedingungsabhängige Fahrzeit ersetzen.
- Verbleibendes Fahrzeitbudget: `5 h - nominale Fahrzeit`; eine negative Zahl als Überschreitung markieren.
- Tagesdauer: Fahrzeit + Pausen + noch nicht enthaltene Rüst-/Trag-/Einkaufszeiten; Doppelzählung vermeiden.
- Geplanter Start, Ankunft, Sonnenuntergang, Tageslichtreserve: offen, datumabhängig.

## Nachtziel

| Merkmal | Wert / Quelle |
|---|---|
| Konkreter Landepunkt und Wiederstart am Folgetag | offen |
| Bevorzugtes Strandhotel, Name und Website | offen |
| Tatsächlicher Fussweg vom Landepunkt, Methode und Hindernisse | offen |
| Alternatives Hotel und Tragestrecke | unbekannt |
| Abendessen / Vorräte / Wasser | unbekannt |

Hotelöffnung und Zimmerverfügbarkeit sind nicht Gegenstand der Prüfung.

## Bedingungen und Lücken

| Aspekt | Abschnitt / Wert / Quelle | Auswirkung |
|---|---|---|
| Kaps / offene Querungen / Küstenabstand | offen | offen |
| Längster Wasserweg ohne geeigneten Ausstieg | offen | Mit persönlichem Grenzwert vergleichen |
| Längster Abschnitt ohne belegten Getränkekauf/Trinkwasser | offen | Mit Vorratsreichweite vergleichen |
| Windwinkel / Start- und Landebedingungen | offen | Phase-2-Eingabe |
| Seegang / Shorebreak / Strömung | offen | Phase-2-Eingabe und Ortsprüfung |
| Ungeklärte Kernmerkmale | offen | Entwurfsstatus bleibt sichtbar |

## Alternativen

| Alternative | Auslöser / Bedingungen | Landepunkt / Hotel | Distanz und Zeit ab Entscheidungspunkt | Quelle |
|---|---|---|---|---|
| Früheres Nachtziel | offen | offen | offen | offen |
| Zusätzlicher Ausstieg | offen | offen | offen | offen |
| Rückzug zum vorherigen geeigneten Ort | offen | offen | offen | offen |

Diese Optionen sind bedingungsabhängig. Ein Abbruchtransport zählt nicht als absolvierte Wasserstrecke.

## Vollständigkeit und Quellen

- Alle Punkte haben verlinkte Steckbriefe und wesentliche Aussagen einen Beleg.
- Wasserweg plausibel, ohne Landdurchquerung.
- Teilstrecken summieren sich zur Gesamtdistanz; Zeiten sind nachvollziehbar und ohne Doppelzählung.
- Zwei oder drei geplante Pausen; weitere Ausstiege separat.
- Zeitbudget, Versorgungslücken, Hotel-Fusswege und verbleibende Unklarheiten ausgewiesen.
- Anschluss an vorherige und nächste Etappe vorhanden; Variantenrichtung eindeutig.

Prüfstatus und Datum hier ergänzen. Quellen für Geometrie, abgeleitete Distanzen und nicht bereits in den Ortssteckbriefen belegte Aussagen direkt verlinken.
