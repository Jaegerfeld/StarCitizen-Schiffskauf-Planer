# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [1.13.0] – 2026-11-30

### Hinzugefügt
- **Komponenten: sechs neue Schiffe**, je mit eigener Draufsicht und eigenem Bild nach eigenen Screenshots, Einbauorte vom Autor markiert. Damit hat der Reiter 19 Schiffe.
  - **Aegis Vanguard Warden:** Hauptkanone S5 und vier S2 als dichter Viererblock an der Nase, bemannter Turm (2 × S3), vier fest verbaute Racks unter den Flügeln.
  - **Anvil C8X Pisces Expedition:** zwei Kanonen an der Nase, zwei Flügelwaffen, zwei Racks unten.
  - **Anvil C8R Pisces Rescue:** zwei Kanonen an der Nase, zwei Racks an den Seiten.
  - **Anvil Arrow:** zwei Flügelwaffen S3, Kinnturm mit zwei S1, vier Racks unter den Flügeln.
  - **Drake Cutlass Red:** vier Waffen S3 unter Nase und Flügeln (laut Spieldaten keine Racks; der Turm ist ein Scanner).
  - **Aegis Reclaimer:** bemannter Turm (2 × S5), sechs Ferntürme (je 2 × S3), zwei Bergungsköpfe mit Modulen, sieben fest verbaute Punktverteidigungen.

### Behoben
- Ein Steckplatz, der laut Spieldaten mehrere Teilearten aufnimmt, bekommt jetzt die Art des eingebauten Teils. Die Raketenracks der Pisces erschienen sonst als Waffe mit falscher Auswahl. Die bisherigen 13 Schiffe sind davon nicht betroffen (geprüft).

## [1.12.0] – 2026-11-29

### Hinzugefügt
- **Komponenten: Bild des Schiffs.** Oben links neben den Summen steht eine Seitenansicht des gezeigten Schiffs, zugeschnitten aus eigenen Screenshots (je etwa 20–25 KB, in die Seite eingebettet, also auch offline da). L-22 Alpha Wolf und Guardian QI zeigen das Bild ihres Schwestermodells mit gleichem Rumpf; die Bildunterschrift sagt das. Schmale Bildschirme stapeln Bild und Summen.

## [1.11.0] – 2026-11-28

### Hinzugefügt
- **Komponenten: Scraper-Module in den Bergungsköpfen** (MOTH, Vulture). Jeder Baler-Kopf hat zwei Modulplätze; jeder Platz ist eine eigene Unterkarte, denn meist stecken zwei verschiedene Module darin (z. B. Cinch und Abrade, an der Vulture links Cinch und ReadyGrip). Zur Wahl stehen die Scraper Abrade, Cinch, Comer, Hart, Trawler und das Traktormodul ReadyGrip, mit Preis und Händler.
  - Kennwerte in Prozent des Kopfs ohne Modul: Tempo (Abtragsgeschwindigkeit), Radius und Ausbeute.
  - Die Spieldaten führen die Modulplätze als nicht tauschbar; im Spiel lassen sie sich wechseln, deshalb bietet der Planer sie an.

## [1.10.0] – 2026-11-27

### Hinzugefügt
- **Komponenten: Schiffsliste mit Suche, Filter und Sortierung.** Der Dialog heißt jetzt **Schiffe …**; unter **Alle Schiffe** filterst du nach Hersteller und Einsatz (Kampf, Industrie, Erkundung …) und sortierst nach Hersteller, Name, Größe oder Einsatz. Jede Zeile nennt Rolle und Größe aus den Spieldaten.
- **Komponenten: Schiff ansehen ohne Flotte.** **Ansehen** öffnet ein Schiff zur Probe (oben gestrichelt mit „Vorschau“). Du kannst es bestücken und jederzeit mit **+ zu meinen Schiffen** samt Bestückung übernehmen oder mit **Vorschau schließen** verwerfen. Die Vorschau übersteht ein Neuladen; ein geteilter Link öffnet ebenfalls als Vorschau.

### Geändert
- **Schiffsnamen nach Schema „Hersteller Schiffsname“** (wie UEX), z. B. „Anvil F7C Hornet Mk II“ statt „Hornet Mk II“, in Knöpfen, Liste und Flotte.
- Der Link einer Bestückung steht nicht mehr dauerhaft in der Adresszeile; er entsteht beim Kopieren. Vorher öffnete ein Neuladen das gezeigte Schiff erneut als Link-Schiff.

## [1.9.0] – 2026-11-26

### Hinzugefügt
- **Komponenten: RSI Perseus.** Eigene Draufsicht nach eigenem Screenshot, Einbauorte vom Autor in Drauf-, Seiten- und Frontansicht markiert. Damit hat der Reiter 13 Schiffe.
  - Bemannte Türme oben und unten: je zwei RSI Medusa S8 (fest) und zwei Mantis S3 (tauschbar).
  - Ferngesteuerte Türme oben und unten: je zwei Waffen S3.
  - Sechs Punktverteidigungen M2C „Swarm“ S1 (fest), zwei Torpedo-Racks S5 (fest, Torpedos tauschbar).
  - Die Torpedo-Kamera trägt keine Waffe und hat keine Karte.
- **Fest verbaute Waffen** erscheinen als Karte mit „fest“, wenn ein Schiff sie als Hauptbewaffnung trägt (zurzeit nur die Perseus). Sie zählen in Schaden/s und Alpha mit; die Auswahl zeigt nur das verbaute Teil.

### Geändert
- Gleich gebaute Türme eines Schiffs (Perseus oben/unten) bekommen getrennte Steckplätze. Gespeicherte Bestückungen der anderen Schiffe bleiben gültig.

## [1.8.0] – 2026-11-25

### Hinzugefügt
- **Komponenten: F8C Lightning, MOTH, L-21 Wolf, L-22 Alpha Wolf, Guardian und Guardian QI.** Eigene Draufsichten nach eigenen Screenshots, Einbauorte vom Autor markiert. L-22 und Guardian QI nutzen die Zeichnung ihres Grundmodells (gleiche Steckplätze laut Spieldaten). Damit hat der Reiter 12 Schiffe.
  - F8C: sechs Kanonen an Nase und Flügeln (Unterseite), Kugelturm mit zwei Waffen, zwei Raketenracks.
  - MOTH: zwei Kanonen, drei Bergungsköpfe, Raketenturm oben.
  - Wolf: zwei Kanonen unter dem Rumpf, zwei Raketenracks.
  - Guardian: zwei Kanonen S5, vier Raketenracks (zwei oben, zwei unten).
- **Fest verbaute Raketenracks** (F8C, Wolf, Raketenturm der MOTH): Das Rack selbst ist laut Spieldaten nicht tauschbar, die Raketen darin schon. Solche Racks erscheinen jetzt als Karte mit „fest“; die Auswahl zeigt nur das verbaute Rack, die Raketen wählst du in der Karte darunter.

## [1.7.0] – 2026-11-25

### Hinzugefügt
- **Komponenten: Bergbau- und Bergungswerkzeuge.** Bergbaulaser (MOLE), Bergungsköpfe (Vulture) und Traktorstrahlen (Hull B) lassen sich tauschen wie Waffen, mit Preis, Händler und Unterschied zum Standardteil.
  - Bergbaulaser: Laserleistung und Reichweite auf der Karte; in der Auswahl dazu die Wirkung auf Widerstand, Instabilität und optimales Fenster (in %, Vorzeichen wie in den Spieldaten). Die Modulplätze (je nach Laser 1–3) stehen als Unterkarte darunter; eine Wahl gilt für alle Plätze des Lasers.
  - Bergbaumodule: Änderung der Laserleistung, Widerstand, bei aktiven Modulen Ladungen und Dauer.
  - Traktorstrahlen: Zugkraft, Reichweite und Abstand voller Kraft. Bergungsköpfe: Reichweite; ihre Schabermodule sind laut Spieldaten nicht tauschbar und werden nicht angeboten.
  - Strombedarf der Werkzeuge zählt in die Energiebilanz.
- Hull B: Einbauorte der beiden Traktorstrahlen nach der Markierung des Autors.

## [1.6.0] – 2026-11-25

### Hinzugefügt
- **Komponenten: Drake Vulture und Argo MOLE.** Eigene Draufsichten nach eigenen Screenshots, Einbauorte vom Autor markiert: Vulture mit zwei Kanonen S1 am Cockpit, MOLE mit zwei Kanonen S2 vorn oben. Die Bergungsköpfe der Vulture und die drei Bergbaulaser der MOLE sind markiert, kommen aber erst mit dem Ausbau für Bergbau und Bergung in den Reiter; bis dahin zeigen beide Schiffe Kanonen, Schilde, Kühler, Kraftwerk, Quantum-Antrieb und Radar.
- **Komponenten: Drake Clipper.** Eigene Draufsicht nach eigenem Screenshot – als ganzer Umriss, weil das Schiff asymmetrisch ist: links 3, rechts 5 Racks (Spieldaten und Spiel stimmen überein). Alle 12 Waffenplätze vom Autor markiert, alle an der Unterseite: zwei Kanonen S3 an der Nase, zwei an den Flügeln, acht Racks S3 (Raketen oder Bomben). Welches Rack innen sitzt, sagen die Daten nicht; gezählt wird je Seite von innen nach außen.

### Geändert
- Breite Schiffe (Draufsicht breiter als hoch, z. B. Clipper) bekommen im Komponenten-Reiter eine breitere Mittelspalte (bis 640 statt 430 px), damit die Draufsicht lesbar bleibt.

## [1.5.0] – 2026-11-25

### Hinzugefügt
- **Komponenten: MISC Hull B.** Eigene Draufsicht nach eigenem Screenshot; Einbauorte der Waffen vom Autor markiert: zwei Kanonen S3 am Kinn (Unterseite), ferngesteuerter Turm mit zwei S3-Waffen oben, Raketenrack S6 (8 × Thunderbolt III) unter der Nase; Schilde, Kühler, Kraftwerk, Quantum-Antrieb und Radar im Rumpf. Die beiden Traktorstrahlen gehören noch nicht zum Reiter.

### Behoben
- Gemeinsame Flotte: Schiffe, die das Wiki mit Hersteller nennt („MISC Hull B“), bekommen jetzt ihre UEX-ID über den vollen UEX-Namen – vorher fehlte die Zuordnung, und die Hull B wäre nicht ins Fracht-Logbuch gekommen.

## [1.4.0] – 2026-11-24

### Hinzugefügt
- **Komponenten: „Meine Schiffe …“.** Ein Dialog stellt deine Flotte zusammen: Modelle (nach Hersteller gruppiert, mit Suche) per **+ Hinzufügen**, auch mehrfach – zum Beispiel zwei F7C Hornet Mk II. Jedes Schiff hat seine eigene Bestückung und einen Namen, den du ändern kannst; gleiche Modelle ohne Namen werden durchnummeriert („Hornet Mk II #2“). Nur die Schiffe deiner Flotte stehen oben als Knöpfe zum Umschalten. So bleibt die Leiste übersichtlich, wenn nach und nach alle Schiffe dazukommen. Ohne Auswahl zeigt der Reiter einen Hinweis mit dem Knopf **Schiffe wählen**.
- **Gemeinsame Flotte mit dem Fracht-Logbuch des Handels-Planers** (neu `flotte.py`, byte-gleich in beiden Repos): Ein Schiff, das du hier oder im Logbuch anlegst, umbenennst oder entfernst, ist im anderen Tool genauso da – online, weil beide Seiten auf jaegerfeld.github.io liegen; Offline-Kopien haben je einen eigenen Speicher. Schiffe ohne Draufsicht (z. B. Frachter aus dem Logbuch) stehen im Dialog mit dem Hinweis „noch nicht im Komponenten-Planer“. Ein Schiff mit Fracht an Bord lässt sich hier nicht entfernen.
- **Flotte und Bestückungen werden im Browser gespeichert** (je Schiff, localStorage), ebenso das zuletzt gezeigte Schiff. Nichts geht an einen Server. Entfernen eines Schiffs mit eigener Bestückung fragt vorher nach.
- **Waffen: Alpha-Schaden und Reichweite** auf jeder Waffenkarte (neben Schaden/s), Alpha auch in der Auswahlliste und als Summe **Alpha-Schaden gesamt** über der Draufsicht.

### Geändert
- Ein Bestückungs-Link hat weiter Vorrang: Er zeigt sein Schiff auch dann, wenn es nicht zu deinen Schiffen gehört (gestrichelter Knopf). **+ zu meinen Schiffen** legt es als neues Schiff mit der Link-Bestückung an; vorher wird nichts gespeichert, ein Link überschreibt also keine eigene Bestückung.

## [1.3.1] – 2026-11-22

### Behoben
- Budget: Eine Kommazahl ohne Kürzel wurde falsch gelesen (`2.5` als 25). Jetzt gilt: Punkt oder Komma vor genau drei Ziffern trennt Tausender (`2.500.000`, `2,500,000`), sonst ist es ein Dezimaltrenner. Unlesbare Eingaben (z. B. `2.5.1`) gelten wie bisher als kein Budget.

## [1.3.0] – 2026-11-21

### Hinzugefügt
- **Knopf „Anleitung + How-To“ in der Kopfzeile** (vor „Was ist neu?“): öffnet einen Dialog mit Reitern – Kurzanleitung, Tutorials Schritt für Schritt und Fragen –, auf Deutsch und Englisch; er folgt der Sprachwahl, auch wenn er offen ist. Die Texte stehen in `ANLEITUNG.md` und `MANUAL.md` und werden wie das Changelog in die Seite eingebacken, gehen also auch in der Offline-Kopie.
- Gemeinsame Kopfzeile Kit 4 (`kopfzeile.py`, byte-gleich in allen fünf Tools); der kleine Markdown-Leser kennt jetzt auch nummerierte Listen.

## [1.2.1] – 2026-11-16

### Behoben
- **Komponenten-Auswahl:** Die Leiste rechts verdeckt auf breiten Bildschirmen (ab 1280 px, z. B. Full HD) nicht mehr die rechte Kartenspalte, sondern schiebt die Seite zur Seite. Schließen geht jetzt auch über das × oben rechts, einen zweiten Klick auf dieselbe Karte, einen Klick neben die Leiste oder Esc.

## [1.2.0] – 2026-11-16

### Hinzugefügt
- **Reiter „Komponenten“ (Vorschau):** Komponenten einzelner Schiffe tauschen, zunächst F7C Hornet Mk II und Guardian MX. In der Mitte eine eigene, stilisierte Draufsicht, rundum Karten mit Linien zum Einbauort. Die Auswahl zeigt nur Teile, die in den Steckplatz passen, standardmäßig nur ingame kaufbare.
- **Turmwaffen und Raketen:** Unter jedem Turm und Raketenrack eine Unterkarte, z. B. „12 × Rakete S2“; eine Wahl gilt für alle gleichen Plätze darin.
- **Summen:** Schild-HP, Waffenschaden/s, Raketenschaden, Kühlung und eine vereinfachte Energiebilanz, jeweils mit Differenz zum Werkszustand.
- **Einkaufsliste:** günstigster Händler mit Sternsystem, alle Händler mit Preis und Preisstand zum Aufklappen. Die Bestückung steckt im Link und lässt sich teilen.

## [1.1.0] – 2026-11-10

### Hinzugefügt
- **Schalter „Leihschiffe anzeigen“:** ergänzt beide Ansichten um Tagesmieten und Mietstationen, die Sortierung um „Miete/Tag“. Ausgeschaltet bleibt alles wie bisher.
- **Merkliste:** Schiffe lassen sich auch zum Mieten vormerken. Kaufsumme und Miete pro Tag stehen getrennt, der Budget-Rest rechnet einen Tag Miete mit ein.

## [1.0.0] – 2026-11-10

### Hinzugefügt
- **Ansicht „Nach Schiff“:** alle ingame kaufbaren Schiffe und Fahrzeuge mit günstigstem Standort und den Preisen an den anderen Standorten, sortierbar nach Name, Hersteller, Preis, Standort, Fracht, Crew und Länge.
- **Ansicht „Nach Standort“:** Angebote gruppiert nach System und Standort, mit Preisvergleich zum günstigsten Ort.
- **Filter** nach Suche, System, Standort, Rolle, Budget, Hersteller, Art und Mindestfracht.
- **Merkliste** mit wählbarem Kaufort je Schiff, Kaufstopps, Summe und Budget-Rest.
- Zweisprachig (DE/EN), offline lauffähig, Daten von UEX.
