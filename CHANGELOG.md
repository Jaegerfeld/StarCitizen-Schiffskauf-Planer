# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [1.4.0] – 2026-11-24

### Hinzugefügt
- **Komponenten: „Meine Schiffe …“.** Ein Dialog (nach Hersteller gruppiert, mit Suche) legt fest, welche Schiffe oben als Knöpfe zum Umschalten stehen. So bleibt die Leiste übersichtlich, wenn nach und nach alle Schiffe dazukommen. Ohne Auswahl zeigt der Reiter einen Hinweis mit dem Knopf **Schiffe wählen**.
- **Auswahl und Bestückung werden im Browser gespeichert** (je Schiff, localStorage), ebenso das zuletzt gezeigte Schiff. Nichts geht an einen Server.
- **Waffen: Alpha-Schaden und Reichweite** auf jeder Waffenkarte (neben Schaden/s), Alpha auch in der Auswahlliste und als Summe **Alpha-Schaden gesamt** über der Draufsicht.

### Geändert
- Ein Bestückungs-Link hat weiter Vorrang: Er zeigt sein Schiff auch dann, wenn es nicht zu deinen Schiffen gehört (gestrichelter Knopf, daneben **+ zu meinen Schiffen**). Gespeichert wird die Link-Bestückung erst, wenn du etwas änderst.

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
