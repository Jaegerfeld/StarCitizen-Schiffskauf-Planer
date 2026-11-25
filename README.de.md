# StarCitizen-Schiffskauf-Planer

**Version 1.2.1** · 🇩🇪 Deutsch · [🇬🇧 English](README.md)

Ein Schiffskauf-Planer für *Star Citizen*: Du siehst, **wo jedes Schiff am günstigsten ist** und
**was an deinem Standort verkauft wird**, und sammelst deine Auswahl auf einer Merkliste mit Budget.

**▶ Online nutzen:** https://jaegerfeld.github.io/StarCitizen-Schiffskauf-Planer/
**▶ Offline nutzen:** [`SC_Schiffskauf_Planer.html`](SC_Schiffskauf_Planer.html) herunterladen und per Doppelklick öffnen.

Die App ist **eine einzige HTML-Datei**, ohne Installation und ohne Server. Die Oberfläche ist
**zweisprachig (Deutsch/Englisch)** und wird in der Kopfzeile umgeschaltet.

## Funktionen

- **Nach Schiff:** alle ingame kaufbaren Schiffe und Fahrzeuge mit günstigstem Standort und den Preisen anderswo.
- **Nach Standort:** Angebote gruppiert nach System und Standort, verglichen mit dem günstigsten Ort.
- **Sortieren** nach Name, Hersteller, Preis, Standort, Fracht, Crew oder Länge.
- **Filtern** nach Suche, System, Standort, Rolle, Budget, Hersteller, Art und Mindestfracht.
- **Leihschiffe (optional):** Ein Schalter ergänzt beide Ansichten um Tagesmieten und Mietstationen.
- **Merkliste:** Kaufort je Schiff wählen, Kaufstopps, Summe und Budget-Rest sehen.
- **Komponenten (Vorschau):** Schilde, Kraftwerke, Kühler, Quantum, Radar, Waffen, Türme, Raketen, Bergbaulaser mit Modulen, Bergungsköpfe und Traktorstrahlen eines
  Schiffs tauschen, nur passende Teile, mit Summen und Einkaufsliste (günstigster Händler, alle Händler zum
  Aufklappen). Zunächst F7C Hornet Mk II, Guardian MX, Guardian/QI, F8C Lightning, L-21/L-22 Wolf, MISC Hull B, Drake Clipper, Drake Vulture, Argo MOLE und MOTH; eigene Flotte („Meine Schiffe“, gleiche Modelle mehrfach möglich), Bestückung je Schiff im Browser gespeichert und als Link teilbar; Waffen mit Schaden/s, Alpha und Reichweite.
- **Tägliche Daten:** Die Online-Version wird jeden Tag neu gebaut. Der Knopf in der App lädt deren
  `data.json`, auch aus einer Offline-Kopie.

## Daten neu bauen

- **Windows:** [`Schiffskauf_Planer_aktualisieren.bat`](Schiffskauf_Planer_aktualisieren.bat) doppelklicken
- **Linux/macOS:** `./Schiffskauf_Planer_aktualisieren.sh`
- **direkt:** `python schiffskauf_planer_bauen.py`

Braucht **Python 3.9+**, nur Standardbibliothek.

## Datenquellen

Kauf- und Mietpreise, Fahrzeugdaten und Terminals: [UEX](https://uexcorp.space) (öffentliche API). Die Preise
sind Community-Meldungen und können dem Spiel hinterherhinken, also vor dem Kauf im Spiel gegenprüfen.
Komponenten, Steckplätze und Kennwerte: [Star Citizen Wiki API](https://api.star-citizen.wiki) (Spieldaten des
Live-Patches, mit den UEX-Preisen je Händler). Die Draufsichten sind eigene Zeichnungen nach eigenen Screenshots.

## Hinweis

Inoffiziell, nicht mit Cloud Imperium Games verbunden. Star Citizen® ist eine Marke von CIG.
Größtenteils mit KI entwickelt ([Claude Code](https://claude.com/claude-code)). Lizenz: BSD-3-Clause.
