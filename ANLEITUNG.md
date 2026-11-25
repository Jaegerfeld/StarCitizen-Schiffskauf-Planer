# SC Schiffskauf-Planer – Anleitung

## Kurzanleitung

Der Planer zeigt dir, wo jedes ingame kaufbare Schiff am günstigsten ist und was an einem Standort verkauft wird. Deine Auswahl sammelst du auf einer Merkliste mit Budget.

### Bereiche

- **Nach Schiff:** jedes Schiff und Fahrzeug einmal, mit dem günstigsten Standort innerhalb deiner Filter und den Preisen anderswo (**Auch:**).
- **Nach Standort:** alle Angebote, gruppiert nach Sternsystem und Standort. Die Spalte **Vergleich** zeigt **günstigster Ort**, **nur hier** oder den Aufschlag in Prozent.
- **Komponenten:** Schilde, Kraftwerke, Kühler, Quantum-Antrieb, Radar, Waffen, Türme und Raketen eines Schiffs tauschen, dazu Bergbaulaser mit ihren Modulen, Bergungsköpfe und Traktorstrahlen. Das ist eine Vorschau, zurzeit mit **Anvil F7C Hornet Mk II**, **Anvil F8C Lightning**, **Argo MOLE**, **Argo MOTH**, **Drake Clipper**, **Drake Vulture**, **Kruger L-21 Wolf**, **Kruger L-22 Alpha Wolf**, **Mirai Guardian**, **Mirai Guardian MX**, **Mirai Guardian QI**, **MISC Hull B** und **RSI Perseus**.
- **Merkliste:** rechts neben der Liste. Hier wählst du den Kaufort je Schiff und siehst **Kaufstopps**, **Summe** und dein Budget.
- Auf schmalen Bildschirmen wechselst du oben mit **Schiffe** und **Merkliste** zwischen Liste und Merkliste.

### Häufige Aktionen

- Oben filtern: **Suche**, **System**, **Standort**, **Rolle** und **Budget max. (aUEC)**.
- **Weitere Filter** aufklappen für **Hersteller**, **Art** und **Fracht mind. (SCU)**.
- Sortieren mit **Sortieren nach** und dem Knopf daneben (**↑ Aufsteigend** / **↓ Absteigend**). Ein Klick auf eine Spaltenüberschrift sortiert auch, ein zweiter Klick dreht die Richtung um.
- **Leihschiffe anzeigen** ergänzt Tagesmieten und Mietstationen.
- **Filter zurücksetzen** leert alle Filter. Ansicht und Sortierung bleiben.
- In der Kopfzeile: **DE** / **EN** für die Sprache, **Hell / Dunkel** für die Farben, **Was ist neu?** für die Änderungen.

### Daten und Speicherung

- Preise, Standorte und Fahrzeugdaten kommen von [UEX](https://uexcorp.space). Das sind Community-Meldungen. Prüfe den Preis vor dem Kauf im Spiel.
- Komponentendaten kommen aus der [Star Citizen Wiki API](https://api.star-citizen.wiki), die Kaufpreise der Komponenten von UEX.
- Die Datenzeile in der Kopfzeile zeigt Anzahl der Fahrzeuge und Standorte, den Spielstand, den Zeitraum der Preismeldungen und die Bauzeit.
- **Neuesten Stand laden (GitHub)** holt die täglich neu gebauten Daten. Dafür brauchst du Internet.
- Dein Browser speichert lokal (localStorage): Sprache, Farbschema, Filter, Merkliste und die zuletzt geladenen Daten. Nichts davon geht an einen Server.
- Im Reiter **Komponenten** speichert der Browser auch deine Flotte und die Bestückung je Schiff. Die Flotte teilt er online mit dem Fracht-Logbuch des Handels-Planers: ein Schiff, ein Name, in beiden Tools. Zum Mitnehmen oder Teilen gibt es den Link.
- Offline: Lade `SC_Schiffskauf_Planer.html` aus dem [Repository](https://github.com/Jaegerfeld/StarCitizen-Schiffskauf-Planer) herunter und öffne die Datei per Doppelklick. Auch dort funktioniert **Neuesten Stand laden (GitHub)**, wenn du online bist.

## Tutorial: Schiff kaufen

Ziel: Du suchst zwei Schiffe aus, legst ein Budget fest und findest heraus, wo du sie am günstigsten kaufst.

1. Öffne den Reiter **Nach Schiff**.
2. Trag dein Geld in **Budget max. (aUEC)** ein, zum Beispiel `5m` oder `2.500.000`. Die Liste zeigt jetzt nur noch Angebote bis zu diesem Preis. Die Merkliste rechnet mit demselben Betrag.
3. Wähl unter **Rolle** eine Aufgabe, zum Beispiel **Fracht**.
4. Stell **Sortieren nach** auf **Preis**. Das günstigste Schiff steht oben.
5. Klick bei einem Schiff auf **Merken**. Der Knopf zeigt danach **Gemerkt ✓**. Das Schiff steht jetzt in der **Merkliste**, mit dem günstigsten Standort innerhalb deiner Filter.
6. Merk dir ein zweites Schiff auf die gleiche Weise.
7. Sieh dir die **Merkliste** an. Die Schiffe sind nach Kaufstopp gruppiert. Unten stehen **Kaufstopps**, **Summe**, **Budget** und **Bleibt übrig** oder **Fehlt**.
8. Willst du an einem anderen Ort kaufen, wähl ihn im Auswahlfeld unter dem Schiff. Jeder Eintrag zeigt Ort und Preis.
9. Kaufst du an mehreren Orten und gibt es einen Ort, der alle Schiffe verkauft, erscheint ein Hinweis mit dem Mehrpreis. Mit **Alles dort kaufen** setzt du alle Schiffe auf diesen Ort.
10. Hast du Orte von Hand geändert, setzt **Alle auf günstigsten Ort setzen** alles wieder auf den günstigsten Preis.
11. Wechsle zu **Nach Standort** und stell **System** auf dein Sternsystem. Dort siehst du, was an jedem Standort verkauft wird. **Merken** in dieser Ansicht legt das Schiff genau an diesem Standort fest.

### Tipps

- Das Budget versteht `750k`, `5m`, `2,5 Mio`, `2.500.000` und `2,500,000`. Kommazahlen brauchen ein Kürzel: `2,5` allein sind 2,5 aUEC.
- Wenn du **System** änderst, springt **Standort** auf **Alle Standorte** zurück.
- Mit **Leihschiffe anzeigen** kannst du ein Schiff auch zum Mieten merken: Wähl in der Merkliste einen Eintrag mit **Miete:**. Dann stehen **Summe Kauf** und **Miete pro Tag** getrennt, und der Budget-Rest rechnet einen Tag Miete mit ein.
- In **Nach Standort** kannst du einzelne Standorte zuklappen.
- **Liste leeren** löscht die ganze Merkliste nach einer Rückfrage.

## Tutorial: Komponenten

Ziel: Du baust bei der Hornet Mk II einen anderen Schild ein und findest heraus, wo du ihn kaufst.

1. Öffne den Reiter **Komponenten**. Filter, Liste und Merkliste sind hier ausgeblendet.
2. Klick auf **Schiffe …** (beim ersten Mal auf **Schiffe wählen**). Unter **Alle Schiffe** findest du ein Schiff über **Suchen**, die Filter **Hersteller** und **Einsatz** und die **Sortierung** (Hersteller, Name, Größe, Einsatz).
   - **Ansehen** öffnet das Schiff zur Probe, ohne es in die Flotte zu nehmen. Oben steht es gestrichelt mit „Vorschau“. Du kannst es bestücken; mit **+ zu meinen Schiffen** übernimmst du es jederzeit samt Bestückung, mit **Vorschau schließen** verwirfst du es. Es gibt immer nur eine Vorschau, sie übersteht auch ein Neuladen.
   - **+ Flotte** fügt das Schiff gleich deiner Flotte hinzu, zum Beispiel die **Anvil F7C Hornet Mk II**. Oben stehen deine Schiffe als Knöpfe; damit schaltest du um. Hast du ein Modell zweimal, füg es zweimal hinzu: Jedes Schiff hat seine eigene Bestückung, und unter **Deine Flotte** kannst du ihm einen Namen geben.
3. In der Mitte siehst du eine Draufsicht. Rundum stehen Karten für jeden Steckplatz, mit Typ, Größe (`S1`, `S2` …) und dem verbauten Teil. Linien führen zum Einbauort.
4. Klick auf eine Karte vom Typ **Schild**. Rechts öffnet sich eine Auswahl mit allen Teilen, die in diesen Steckplatz passen.
5. Jede Zeile zeigt Name, Preis, Händler und die Werte. Die Zahlen mit + oder - sind der Unterschied zum Standardteil. Die Marken **Standard** und **verbaut** zeigen, was ab Werk drin ist und was gerade eingebaut ist.
6. Klick auf ein Teil, um es einzubauen. Die Karte zeigt danach **geändert**.
7. Schließ die Auswahl mit **Schließen**, mit dem × oben rechts, mit Esc, mit einem zweiten Klick auf dieselbe Karte oder mit einem Klick daneben.
8. Prüf die Summen über der Draufsicht: **Schild-HP gesamt**, **Waffenschaden/s**, **Alpha-Schaden gesamt**, **Raketenschaden gesamt**, **Kühlung** und die Energiebilanz (erzeugt / Bedarf). Pfeile zeigen den Unterschied zum Werkszustand. **⚠ zu wenig** heißt, das Kraftwerk liefert weniger, als die Teile brauchen.
9. Scroll zur **Einkaufsliste**. Sie nennt für jedes getauschte Teil den günstigsten Händler mit Sternsystem und den Preis. Mit **alle … Händler** klappst du alle Händler mit Preis und Datum der Preismeldung auf.
10. Deine Bestückung merkt sich der Browser von selbst. Zum Teilen oder für ein anderes Gerät klick auf **Link zu dieser Bestückung kopieren**. Wer den Link öffnet, sieht das Schiff als Vorschau und kann es in seine Flotte übernehmen.

### Tipps

- Unter jedem Turm und Raketenwerfer steht eine Unterkarte, zum Beispiel für die Raketen. Eine Wahl dort gilt für alle gleichen Plätze darin.
- Baust du einen anderen Turm oder Raketenwerfer ein, wird die Wahl der Waffen oder Raketen darin zurückgesetzt.
- Die Auswahl zeigt zuerst nur ingame kaufbare Teile. Entferne den Haken bei **Nur ingame kaufbare zeigen**, um auch Loot, Crafting und Werksteile anderer Varianten zu sehen.
- **Standard wiederherstellen** setzt einen Steckplatz zurück, **Alles auf Standard** das ganze Schiff.
- Die Energiebilanz ist vereinfacht: alle Verbraucher außer dem Quantum-Antrieb laufen gleichzeitig, ohne Waffen-Energiepool.
- Die Draufsicht ist eine eigene, stilisierte Zeichnung und nicht maßstäblich.

## Fragen

### Warum fehlt ein Schiff?

- Die Liste zeigt nur Schiffe, die mindestens ein Standort im Live-Spiel verkauft. Schiffe, die man nur mieten kann, stehen nicht drin.
- Prüf deine Filter. **Filter zurücksetzen** zeigt wieder alles.

### Stimmen die Preise?

- Die Preise sind Community-Meldungen bei UEX und können dem Spiel hinterherhinken. Prüf den Preis vor dem Kauf im Spiel.

### Was passiert mit meiner Merkliste nach einem Update?

- Die Merkliste bleibt in deinem Browser. Wird ein Schiff nicht mehr verkauft, fällt es heraus. Verkauft dein gewählter Ort es nicht mehr, springt der Eintrag auf den günstigsten Ort.

### Ich sehe meine Daten auf einem anderen Gerät nicht.

- Merkliste, Filter, deine Schiffe und Bestückungen liegen nur im Browser, in dem du sie angelegt hast. Eine Bestückung aus **Komponenten** nimmst du per Link mit.

### Was zeigt „Neuesten Stand laden (GitHub)“?

- Der Knopf lädt die Daten des letzten täglichen Baus. Klappt das nicht, bleiben die eingebauten Daten aktiv. Geladene Daten nutzt der Browser auch beim nächsten Öffnen, solange sie neuer sind als die eingebauten.
