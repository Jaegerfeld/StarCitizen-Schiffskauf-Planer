# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

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
