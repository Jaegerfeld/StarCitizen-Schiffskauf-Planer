# SC Ship Purchase Planner – Manual

## Quick guide

The planner shows you where each ship sold in game is cheapest and what is sold at a location. You collect your picks on a wishlist with a budget.

### Areas

- **By ship:** every ship and vehicle once, with the cheapest location within your filters and the prices elsewhere (**Also:**).
- **By location:** all offers, grouped by star system and location. The **Comparison** column shows **cheapest**, **only here** or the surcharge in percent.
- **Components:** swap a ship's shields, power plants, coolers, quantum drive, radar, weapons, turrets and missiles. This is a preview, currently with the **Hornet Mk II** and the **Guardian MX**.
- **Wishlist:** to the right of the list. Here you choose the buying location per ship and see **Buying stops**, **Total** and your budget.
- On narrow screens, use **Ships** and **Wishlist** at the top to switch between the list and the wishlist.

### Frequent actions

- Filter at the top: **Search**, **System**, **Location**, **Role** and **Max. budget (aUEC)**.
- Open **More filters** for **Manufacturer**, **Type** and **Min. cargo (SCU)**.
- Sort with **Sort by** and the button next to it (**↑ Ascending** / **↓ Descending**). Clicking a column header also sorts, a second click reverses the order.
- **Show rentals** adds daily rental prices and rental stations.
- **Reset filters** clears all filters. View and sort order stay.
- In the header: **DE** / **EN** for the language, **Light / Dark** for the colours, **What’s new?** for the changes.

### Data and storage

- Prices, locations and vehicle data come from [UEX](https://uexcorp.space). These are community reports. Check the price in game before buying.
- Component data comes from the [Star Citizen Wiki API](https://api.star-citizen.wiki), the component prices from UEX.
- The data line in the header shows the number of vehicles and locations, the game version, the period of the price reports and the build time.
- **Load latest build (GitHub)** fetches the data that is rebuilt every day. You need an internet connection for this.
- Your browser stores locally (localStorage): language, colour scheme, filters, wishlist and the most recently loaded data. None of it is sent to a server.
- In the **Components** tab the browser also stores your choice of ships and the loadout per ship. To take it along or share it, use the link.
- Offline: download `SC_Schiffskauf_Planer.html` from the [repository](https://github.com/Jaegerfeld/StarCitizen-Schiffskauf-Planer) and open the file with a double-click. **Load latest build (GitHub)** also works there when you are online.

## Tutorial: Buy a ship

Goal: you pick two ships, set a budget and find out where to buy them for the lowest price.

1. Open the **By ship** tab.
2. Enter your money in **Max. budget (aUEC)**, for example `5m` or `2,500,000`. The list now only shows offers up to this price. The wishlist uses the same amount.
3. Choose a job under **Role**, for example **Cargo**.
4. Set **Sort by** to **Price**. The cheapest ship is at the top.
5. Click **Save** on a ship. The button then shows **Saved ✓**. The ship is now on the **Wishlist**, at the cheapest location within your filters.
6. Save a second ship the same way.
7. Look at the **Wishlist**. The ships are grouped by buying stop. At the bottom you see **Buying stops**, **Total**, **Budget** and **Left over** or **Short by**.
8. To buy somewhere else, choose the place in the selection box under the ship. Each entry shows place and price.
9. If you buy at more than one place and one location sells all your ships, a hint with the extra cost appears. **Buy everything there** sets all ships to that location.
10. If you changed places by hand, **Set all to cheapest location** puts everything back on the lowest price.
11. Switch to **By location** and set **System** to your star system. There you see what each location sells. **Save** in this view fixes the ship to exactly that location.

### Tips

- The budget accepts `750k`, `5m`, `2.5m`, `2,500,000` and `2.500.000`. Decimals need a suffix: `2.5` on its own means 2.5 aUEC.
- When you change **System**, **Location** goes back to **All locations**.
- With **Show rentals** you can also save a ship for renting: choose an entry starting with **Rental:** on the wishlist. **Purchase total** and **Rent per day** are then shown separately, and the remaining budget includes one day of rent.
- In **By location** you can collapse single locations.
- **Clear list** deletes the whole wishlist after asking you.

## Tutorial: Components

Goal: you fit a different shield to the Hornet Mk II and find out where to buy it.

1. Open the **Components** tab. Filters, list and wishlist are hidden here.
2. Click **My ships …** (the first time **Choose ships**), tick your ships, for example the **F7C Hornet Mk II**, and click **Done**. Only your ships now appear at the top as buttons; use them to switch.
3. In the middle you see a top view. Around it are cards for each slot, with type, size (`S1`, `S2` …) and the fitted part. Lines lead to the mounting point.
4. Click a card of type **Shield**. A selection opens on the right with all parts that fit this slot.
5. Each row shows name, price, shop and the values. The numbers with + or - are the difference to the stock part. The tags **Stock** and **fitted** show what comes from the factory and what is fitted right now.
6. Click a part to fit it. The card then shows **changed**.
7. Close the selection with **Close**, the × at the top right, Esc, a second click on the same card or a click next to it.
8. Check the totals above the top view: **Total shield HP**, **Weapon damage/s**, **Total alpha damage**, **Total missile damage**, **Cooling** and the power balance (output / draw). Arrows show the difference to the stock loadout. **⚠ too little** means the power plant delivers less than the parts need.
9. Scroll to the **Shopping list**. For each swapped part it names the cheapest shop with its star system and the price. **all … shops** expands all shops with price and date of the price report.
10. The browser remembers your loadout by itself. To share it or use another device, click **Copy link to this loadout**.

### Tips

- Below each turret and missile rack there is a sub-card, for example for the missiles. A choice there applies to all identical mounts inside.
- If you fit a different turret or missile rack, the choice of weapons or missiles inside it is reset.
- At first the selection shows only parts you can buy in game. Untick **Only show parts buyable in game** to also see loot, crafting and stock parts of other variants.
- **Restore stock part** resets one slot, **Reset all to stock** the whole ship.
- The power balance is simplified: all consumers except the quantum drive run at once, without the weapon power pool.
- The top view is an own, stylised drawing and not to scale.

## FAQ

### Why is a ship missing?

- The list only shows ships that at least one location in the live game sells. Ships you can only rent are not listed.
- Check your filters. **Reset filters** shows everything again.

### Are the prices correct?

- The prices are community reports on UEX and can lag behind the game. Check the price in game before buying.

### What happens to my wishlist after an update?

- The wishlist stays in your browser. If a ship is no longer sold, it is removed. If your chosen place no longer sells it, the entry switches to the cheapest location.

### I don't see my data on another device.

- Wishlist, filters, your ships and loadouts live only in the browser where you created them. You take a loadout from **Components** with you as a link.

### What does "Load latest build (GitHub)" do?

- The button loads the data of the last daily build. If that fails, the built-in data stays active. The browser also uses loaded data the next time you open the page, as long as it is newer than the built-in data.
