# Datenquellen und APIs

Recherche- und Prüfdatum: 18.10.2026. Quellen werden für jeweils klar begrenzte Aussagen verwendet. Eine Datenquelle für Hotels ist keine Quelle für die Befahrbarkeit eines Strandes.

## Q01 — OpenStreetMap über Overpass

- Anbieter: OpenStreetMap-Mitwirkende; öffentliche Overpass-Instanz.
- Dokumentation: [Overpass-Handbuch](https://dev.overpass-api.de/overpass-doc/en/), [Abfragesprache](https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide), [Nutzungsregeln der öffentlichen Instanz](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html).
- API: `https://overpass-api.de/api/interpreter`; GET oder POST mit Overpass-QL; kein Schlüssel für diesen öffentlichen Dienst.
- Zweck: Kandidaten für Strände, Hotels, Gastronomie, Läden, Trinkwasser und Fusswege sammeln. `node`, `way` und `relation` berücksichtigen; Objekte anhand von Typ und ID referenzieren.
- Geeignete Suchmerkmale: `natural=beach`, `tourism=hotel`, `amenity=bar/cafe/restaurant/drinking_water`, `shop=supermarket/convenience`. Unterkunftsalternativen separat etwa über `tourism=guest_house` suchen.
- Grenze: Unvollständige oder veraltete Einträge; keine Garantie für Getränkesortiment, Strandtiefe oder Wiederstart. `out center` liefert bei Flächen nur einen Suchpunkt; für Anlandungen ist die tatsächliche Geometrie nötig.
- Abrufstrategie: Gebietsweise kleine Abfragen, Ergebnisse zwischenspeichern, Dubletten zusammenführen, bei Zeitlimit begrenzt erneut versuchen. Für grössere Datenmengen regionale Extrakte prüfen.
- Lizenz: © OpenStreetMap contributors; [ODbL und Attribution](https://www.openstreetmap.org/copyright).

Die tatsächlich verwendete kleine Abfrage steht in [check_sources.py](../scripts/check_sources.py); vollständiger Querytext und Ergebnisstatus werden im jeweiligen Manifest gespeichert. Das Testrechteck liegt im Raum Cagliari/Poetto. Seine Auswahl ist technisch motiviert und legt keinen Startort fest.

## Q02 — Geoportale della Regione Sardegna / SITR

- Primärquelle: [Offizielle WFS-Dokumentation](https://www.sardegnageoportale.it/index.php?c=8835&s=29692&t=1&v=2&xsl=1598).
- Dokumentierter Dienst: `http://webgis.regione.sardegna.it/geoserver/ows`; im Test funktionierte die HTTPS-Variante.
- Verwendete Abfrage: `https://webgis.regione.sardegna.it/geoserver/ows?service=WFS&request=GetCapabilities&version=1.1.0`.
- Zweck: Verfügbare Vektorlayer ermitteln; danach mit `DescribeFeatureType` und räumlich begrenztem `GetFeature` gezielt passende Geometrien beziehen. Die Dokumentation nennt maximal 10.000 Features je Anfrage.
- Im geprüften Katalog: 359 FeatureTypes. Für diese Planung unter anderem relevant: `dbu:dbgt_10k_22_v05_04_linea_costa_marina` (Küstenlinie) und `dbu:campi_dunari_sist_spiaggia` (Dünen-/Strandsysteme).
- Grenze: GetCapabilities bestätigt nur das veröffentlichte Angebot, nicht Vollständigkeit, Alter oder Eignung jedes Layers. Vor Nutzung CRS/Achsenreihenfolge, Erhebungsdatum, Metadaten und Nutzungsbedingungen des konkreten Layers prüfen.

Der Abruf der Küstengeometrie und ihre Eignung für Wasserwege sind noch zu prüfen. WFS liefert Vektordaten; ein WMS-Kartenbild ist kein Ersatz für vermessbare Wege oder konkrete Landepunkte.

## Q03 — EMODnet Bathymetry

- Primärquellen: [Produktbeschreibung](https://emodnet.ec.europa.eu/en/bathymetry), [Webservice-Dokumentation](https://emodnet.ec.europa.eu/en/emodnet-web-service-documentation).
- Geprüfter API-Aufruf: `https://ows.emodnet-bathymetry.eu/wms?service=WMS&version=1.3.0&request=GetCapabilities`.
- Zweck: Tiefen- und Küstenkontext sowie Metadaten. Für numerische Analysen geeignete Download-/Rasterdienste des konkreten Produkts wählen; WMS liefert zunächst Karten und gegebenenfalls Punktinformationen.
- Ergebnis des Tests: gültiges WMS-Capabilities-XML, unter anderem `emodnet:mean`, `emodnet:mean_multicolour`, `emodnet:quality_index` und `coastlines`.
- Grenze: Das beschriebene DTM 2024 hat 1/16 Bogenminute Rasterweite, also eine Grössenordnung um 100 m. Daraus lässt sich keine sichere Foil-Tiefe am Strand oder das Fehlen einzelner Felsen ableiten. Höher aufgelöste Produkte sind nur für ausgewählte Gebiete verfügbar und müssten für Sardinien geprüft werden.
- Tiefenreferenz, Produktversion, Originalmessung und Lizenz beim gewählten Datensatz dokumentieren. Der Test hat keine Tiefenwerte eines Landeplatzes validiert.

## Q04 — Hotel- und Anbieterwebsites

Konkrete Hotels und Verkaufsstellen zunächst über Geodaten finden, dann mit ihrer eigenen Website bzw. einer geeigneten direkten Quelle abgleichen. Name, Lage und Strandbezug erfassen. Fusswege anhand von Weggeometrien bestimmen; Routingdienste oder OSM-Wege können dabei helfen.

Es wurden noch keine Hotels ausgewählt oder kontaktiert. Saisonöffnung und Zimmerverfügbarkeit werden nicht recherchiert. Eine allgemeine Hotel-API ist für die erste Phase nicht erforderlich; falls später eine genutzt wird, Zugang, Kosten und Nutzungsbedingungen getrennt prüfen.

## Q05 — Open-Meteo Historical Weather API, für Phase 2

- Primärquelle: [Dokumentation der historischen Wetterdaten](https://open-meteo.com/en/docs/historical-weather-api).
- API: `https://archive-api.open-meteo.com/v1/archive`.
- Zweck: Stündliche Windgeschwindigkeit und Windrichtung für gewählte historische September abrufen. Modell, Koordinaten, Zeitraum, Zeitzone und Einheiten explizit festhalten.
- Einstieg: festes Modell `era5` mit `wind_speed_10m` und `wind_direction_10m`; mehrere Küsten-/Routenpunkte verwenden, ausgewählte Gitterzellen und Land-/Seelage kontrollieren.
- Grenze: ERA5 wird mit rund 25 km räumlicher Auflösung beschrieben. Modell-Reanalyse ist keine lokale Strandmessung. Der automatische Modellmix sollte für vergleichbare Zeitreihen durch eine begründete feste Modellwahl ersetzt werden.
- Böen gesondert prüfen: Die aktuelle Variablentabelle weist Böen für das reine ERA5-Modell dort nicht aus. Keine fehlenden Böen als Null behandeln und nicht ungeprüft aus Mittelwind berechnen.
- Status: Dokumentation geprüft; noch keine Wetterdaten abgerufen und keine Simulation durchgeführt. Aktuelle API-Nutzungsbedingungen vor dem Serienabruf prüfen.

## Q06 — Copernicus Marine, für Phase 2

- Primärquellen: [Toolbox-Einführung](https://help.marine.copernicus.eu/en/articles/7949409-copernicus-marine-toolbox-introduction), [Python-API für räumlich/zeitliche Ausschnitte](https://help.marine.copernicus.eu/en/articles/8283072-copernicus-marine-toolbox-api-subset).
- Zweck: Passende historische Mittelmeer-Produkte für Wellen und Strömung auswählen und räumlich/zeitlich begrenzt über CLI oder Python beziehen.
- Zu dokumentieren: Produkt-/Datensatz-ID, Version, Variable, Einheit, zeitliche Auflösung, Tiefenschicht, Gitterzelle und Lizenz. Konto-/Authentifizierungsanforderungen beim konkreten Zugriff prüfen; keine Zugangsdaten in Markdown speichern.
- Grenze: Offshore-Modellwellen sind keine direkte Vorhersage des Shorebreaks am einzelnen Strand.
- Status: API-Dokumentation geprüft, noch kein Produkt ausgewählt oder Datensatz heruntergeladen.

## Reale Abrufprüfung und Rohdaten

| Lauf | Ergebnis | Nachweis |
|---|---|---|
| Erster Versuch in eingeschränkter Netzwerkumgebung | Alle drei Anfragen scheiterten an der Namensauflösung; kein fachlicher Befund über die Dienste | [Manifest](../data/source-checks/20261018T071436527848Z/manifest.json) |
| Wiederholung mit Netzwerkzugang | Sardegna-WFS und EMODnet-WMS erfolgreich; Overpass-Lesezeitlimit | [Manifest](../data/source-checks/20261018T071448666973Z/manifest.json) |
| Einmalige gezielte Wiederholung von Overpass | Erneutes Lesezeitlimit; keine OSM-Stichprobe erhalten | [Manifest](../data/source-checks/20261018T071754540481Z/manifest.json) |

Rohantworten: [Sardegna-WFS](../data/source-checks/20261018T071448666973Z/sardegna_wfs_capabilities.xml), [EMODnet-WMS](../data/source-checks/20261018T071448666973Z/emodnet_wms_capabilities.xml). Für OSM liegt noch keine Rohantwort vor. Die Overpass-Abfrage ist vorbereitet, ihre erfolgreiche Ausführung noch nicht bestätigt; ein Zeitlimit belegt weder fehlende Orte noch einen dauerhaften Dienstausfall.

## Quellen dokumentieren

Quellen mit Titel, Anbieter, direkter URL und Abrufdatum an den jeweiligen Angaben verlinken. Bei APIs zusätzlich Request/Parameter, OSM-ID oder Layer-ID und Rohdatei speichern. Die bestehenden Abrufprotokolle mit Datenstand und Prüfsummen bleiben erhalten.

Bei berechneten Wasserweg- und Fusswegdistanzen Ausgangsgeometrie, Distanzmethode und Einheit nennen.
