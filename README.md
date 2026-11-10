# StarCitizen-Schiffskauf-Planer

**Version 1.0.0** · 🇬🇧 English · [🇩🇪 Deutsch](README.de.md)

A ship purchase planner for *Star Citizen*: see **where each ship is cheapest** and **what is sold at
your location**, then collect your picks on a wishlist with a budget.

**▶ Use online:** https://jaegerfeld.github.io/StarCitizen-Schiffskauf-Planer/
**▶ Use offline:** download [`SC_Schiffskauf_Planer.html`](SC_Schiffskauf_Planer.html) and open it (double-click).

The whole app is **one self-contained HTML file**: no install, no server. The interface is
**bilingual (English/German)**, switchable in the header.

## Features

- **By ship:** every ship and vehicle sold in game with its cheapest location and the prices elsewhere.
- **By location:** offers grouped by star system and location, compared to the cheapest place.
- **Sort** by name, manufacturer, price, location, cargo, crew or length.
- **Filter** by search, system, location, role, budget, manufacturer, type and minimum cargo.
- **Wishlist:** choose the buying location per ship and see buying stops, total and remaining budget.
- **Daily data:** the online version is rebuilt every day. The in-app button loads that build's
  `data.json`, also from an offline copy.

## Rebuild / update the bundled data

- **Windows:** double-click [`Schiffskauf_Planer_aktualisieren.bat`](Schiffskauf_Planer_aktualisieren.bat)
- **Linux/macOS:** `./Schiffskauf_Planer_aktualisieren.sh`
- **direct:** `python schiffskauf_planer_bauen.py`

Requires **Python 3.9+**, standard library only.

## Data sources & credits

Purchase prices, vehicle data and terminals: [UEX](https://uexcorp.space) (public API). Prices are
community reports and can lag behind the game, so verify in game before buying.

## Disclaimer

Unofficial, not affiliated with Cloud Imperium Games. Star Citizen® is a trademark of CIG.
Developed largely with AI ([Claude Code](https://claude.com/claude-code)). License: BSD-3-Clause.
