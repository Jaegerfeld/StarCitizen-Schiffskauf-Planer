# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Schiffskauf-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       16.11.2026
# Geändert:       16.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Daten für den Reiter „Komponenten“: Steckplätze der Schiffe aus
#   komponenten_schiffe.py, alle passenden Komponenten (Typ und Größe) mit
#   wenigen Kennwerten und allen UEX-Kauforten. Quelle ist die Star-Citizen-
#   Wiki-API (Spieldaten des Live-Patches, enthält die UEX-Preise je Händler).
#   Bewusst schlank gegenüber erkul: höchstens drei Kennwerte je Teil, Unter-
#   plätze in Türmen und Raketenracks je Art und Größe zusammengefasst.
#   Energiebilanz und Kennwerte aus dem Energienetz (resource_network), nicht
#   aus dem Feld coolant_segment_generation, das für alle Kühler gleich ist.
# =============================================================================
"""Component data for the "Komponenten" tab, built from the Star Citizen Wiki API.

``build()`` returns one JSON-ready dict for all ships in ``komponenten_schiffe.SHIPS``.
The catalog is shared across ships and keyed ``<Type>_<size>``; turret and module mounts
listed in a ship's ``extra`` get their own key ``<slug>:<port>``.
"""
from __future__ import annotations

import json
import pathlib
import time
import urllib.parse
import urllib.request

from komponenten_schiffe import SHIPS

HERE = pathlib.Path(__file__).resolve().parent
#: Wiki API base; the API rejects requests without a User-Agent.
API = "https://api.star-citizen.wiki/api"
UA = {"User-Agent": "sc-tools-schiffskauf-planer (github.com/Jaegerfeld)"}
#: Local cache for ``--cache`` builds (gitignored).
CACHE = HERE / "kp_cache"

#: Component types and their card labels (DE, EN).
TYPES = {
    "WeaponGun": ("Waffe", "Weapon"),
    "MissileLauncher": ("Raketen", "Missiles"),
    "Shield": ("Schild", "Shield"),
    "PowerPlant": ("Kraftwerk", "Power plant"),
    "Cooler": ("Kühler", "Cooler"),
    "QuantumDrive": ("Quantum-Antrieb", "Quantum drive"),
    "Radar": ("Radar", "Radar"),
    "Turret": ("Turm", "Turret"),
    "Mount": ("Turm/Modul", "Turret/module"),
    "Missile": ("Rakete", "Missile"),
}
#: Types that slots() detects on its own; the others only via ``extra`` or as sub-mounts.
AUTO = {"WeaponGun", "MissileLauncher", "Shield", "PowerPlant", "Cooler", "QuantumDrive", "Radar"}
#: Parts that only carry an internal name in the game data.
NAMES = {"afe85dfc-155c-40f0-87f5-8c26cc41fc37": "Rotodome (Hornet Tracker Mk II)"}
#: Short labels for the missile seeker types.
SEEK = {"Infrared": "IR", "Electromagnetic": "EM", "CrossSection": "CS"}


def get(path: str, name: str, use_cache: bool) -> dict:
    """Fetch one API resource, optionally from the local cache (valid one day).

    Args:
        path: Path below ``API`` including the query string.
        name: Cache file name without extension.
        use_cache: Read a cached copy if it is younger than one day.

    Returns:
        The decoded JSON response.
    """
    f = CACHE / f"{name.replace(':', '_')}.json"
    if use_cache and f.exists() and time.time() - f.stat().st_mtime < 86400:
        return json.loads(f.read_text(encoding="utf-8"))
    req = urllib.request.Request(f"{API}/{path}", headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if use_cache:
        CACHE.mkdir(exist_ok=True)
        f.write_text(json.dumps(data), encoding="utf-8")
    return data


def ptypes(p: dict) -> set:
    """Compatible item types of a port."""
    return {(x.get("type") if isinstance(x, dict) else x) for x in (p.get("compatible_types") or [])}


def side_of(port: str) -> str:
    """L, R or C from the port name (the data names left and right ports explicitly)."""
    p = port.lower()
    return "L" if "left" in p else "R" if "right" in p else "C"


def subgroups(ports: list | None) -> dict:
    """Sub-mounts of a turret or rack, grouped by kind and size.

    One choice in the page applies to all ``n`` mounts of a group, which keeps the
    tab simple; the game allows mixing.

    Args:
        ports: Ports of the turret or rack (item data or vehicle data).

    Returns:
        ``{"WeaponGun_3": {"k", "type", "size", "n", "def"}}``; ``def`` is the fitted
        part if the data names one (only vehicle data does).
    """
    groups: dict = {}
    for p in ports or []:
        ts, size = ptypes(p), (p.get("sizes") or {}).get("max")
        typ = "WeaponGun" if "WeaponGun" in ts else "Missile" if "Missile" in ts else None
        if not typ or not size:
            continue
        k = f"{typ}_{size}"
        g = groups.setdefault(k, {"k": k, "type": typ, "size": size, "n": 0, "def": None})
        g["n"] += 1
        e = p.get("equipped_item") or {}
        if e.get("type") == typ and not g["def"]:
            g["def"] = e.get("uuid")
    return groups


def slots(vehicle: dict) -> list[dict]:
    """Editable slots of the AUTO types, weapons inside gimbals included.

    Swappable gimbals or turrets themselves get no card; the weapon inside does.

    Args:
        vehicle: Vehicle record of the Wiki API.

    Returns:
        Slot dicts with id, port, type, size, side, default part and sub-mount defaults.
    """
    out = []

    def walk(ports: list, parent: str | None = None) -> None:
        for p in ports:
            t = set() if "Turret" in ptypes(p) else ptypes(p) & AUTO
            if t and p.get("editable") and (p.get("sizes") or {}).get("max"):
                typ = sorted(t, key=list(TYPES).index)[0]
                port = parent or p["name"]
                out.append({"id": f"{parent}/{p['name']}" if parent else p["name"], "port": port,
                            "type": typ, "size": p["sizes"]["max"], "side": side_of(port),
                            "default": (p.get("equipped_item") or {}).get("uuid"),
                            "subdef": {k: g["def"] for k, g in subgroups(p.get("ports")).items()
                                       if g["def"]}})
            walk(p.get("ports") or [], p["name"])

    walk(vehicle["ports"])
    return out


def _net(it: dict) -> tuple[float | None, float | None, dict]:
    """Power draw, generated amount and signature in the item's first (online) state."""
    st = ((it.get("resource_network") or {}).get("states") or [{}])[0]
    use = gen = None
    for d in st.get("deltas") or []:
        if d.get("type") in ("Consumption", "Conversion") and d.get("resource") == "Power":
            use = d.get("rate")
        if d.get("type") == "Generation" and d.get("resource") == "Power":
            gen = d.get("rate")
        if d.get("type") == "Conversion" and d.get("generated_rate") is not None:
            gen = d.get("generated_rate")
    return use, gen, st.get("signature") or {}


def _mounts_text(it: dict) -> str | None:
    """Weapon and rack mounts of a turret as text, e.g. ``2 × S3 + 1 × Rack S4``."""
    ports = it.get("ports") or []
    guns = [(p.get("sizes") or {}).get("max") for p in ports if "WeaponGun" in ptypes(p)]
    racks = [(p.get("sizes") or {}).get("max") for p in ports if "MissileLauncher" in ptypes(p)]
    parts = [f"{len(guns)} × S{max(guns)}"] if guns else []
    if racks:
        parts.append(f"{len(racks)} × Rack S{max(racks)}")
    return " + ".join(parts) or None


def _weapon(it: dict, use: float | None) -> dict:
    """Damage per second, alpha damage (one shot), range and power draw of a gun."""
    w = it.get("vehicle_weapon") or {}
    dmg = sum(d.get("damage") or 0 for d in (w.get("damages") or [])) or w.get("damage_per_shot") or 0
    rpm = w.get("rpm") or 0
    return {"dps": round(dmg * rpm / 60) if dmg and rpm else None,
            "alpha": round(dmg, 1) if dmg else None, "range": w.get("range"), "pwr": use}


def _rack(it: dict) -> dict:
    """Missile count and size of a rack."""
    sizes = [s for s in ((p.get("sizes") or {}).get("max") for p in it.get("ports") or []) if s]
    return {"missiles": f"{len(sizes)} × S{max(sizes)}" if sizes else None}


def stats(it: dict) -> dict:
    """At most three key values per type, always the same ones, plus power draw (pwr).

    Args:
        it: Item record of the Wiki API.

    Returns:
        Key values by short name (see STAT in the page).
    """
    t = it.get("type")
    use, gen, sig = _net(it)
    sh = it.get("shield") or {}
    jump = (it.get("quantum_drive") or {}).get("standard_jump") or {}
    mis = it.get("missile") or {}
    table = {
        "Cooler": lambda: {"cool": gen, "pwr": use, "ir": sig.get("ir")},
        "PowerPlant": lambda: {"power": gen, "em": sig.get("em"),
                               "dur": (it.get("durability") or {}).get("health")},
        "Shield": lambda: {"hp": sh.get("max_health"), "regen": sh.get("regen_rate"), "pwr": use},
        "QuantumDrive": lambda: {
            "qspeed": round(jump["drive_speed"] / 1e6, 1) if jump.get("drive_speed") else None,
            "spool": jump.get("spool_up_time"), "pwr": use},
        "WeaponGun": lambda: _weapon(it, use),
        "MissileLauncher": lambda: _rack(it),
        "Radar": lambda: {"pwr": use, "em": sig.get("em")},
        "Missile": lambda: {"mdmg": mis.get("damage_total"),
                            "seek": SEEK.get(mis.get("signal_type"), mis.get("signal_type")),
                            "mspeed": mis.get("speed")},
        "Turret": lambda: {"guns": _mounts_text(it)},
    }
    return table[t]() if t in table else {}


def shops(it: dict) -> list[dict]:
    """All UEX purchase offers of an item, cheapest first (ties alphabetical).

    Args:
        it: Item record of the Wiki API (with ``uex_prices``).

    Returns:
        Offers with price, shop, star system and date of the last price report.
    """
    out: dict = {}
    for p in (it.get("uex_prices") or {}).get("purchase") or []:
        price, name = p.get("price_buy") or 0, p.get("terminal_name")
        if price > 0 and name and (name not in out or price < out[name]["price"]):
            out[name] = {"price": price, "shop": name,
                         "sys": (p.get("starmap_location") or {}).get("star_system_name"),
                         "date": (p.get("date_updated") or "")[:10]}
    return sorted(out.values(), key=lambda s: (s["price"], s["shop"]))


def entry(it: dict) -> dict:
    """Compact catalog entry of an item as used by the page."""
    man = it.get("manufacturer")
    sh = shops(it)
    return {"uuid": it["uuid"], "name": NAMES.get(it["uuid"], it["name"]),
            "grade": it.get("grade"), "cls": it.get("class"),
            "maker": man.get("name") if isinstance(man, dict) else man,
            "loot": bool(it.get("is_lootable")), "craft": bool(it.get("is_craftable")),
            "stats": stats(it), "buy": sh[0] if sh else None, "shops": sh,
            "sub": (list(subgroups(it.get("ports")).values())
                    if it.get("type") in ("Turret", "MissileLauncher") else [])}


def candidates(typ: str, size: int, use_cache: bool) -> list[dict]:
    """All items of one type and size (placeholders dropped)."""
    q = urllib.parse.urlencode({"filter[type]": typ, "filter[size]": size, "limit": 200})
    data = get(f"items?{q}", f"items_{typ}_{size}", use_cache)["data"]
    return [entry(it) for it in data
            if not (it.get("name", "").startswith("<=") or "PLACEHOLDER" in it.get("name", ""))]


def extra_slot(slug: str, v: dict, port: str, typ: str, siblings: list[str],
               use_cache: bool) -> tuple[dict, list[dict]]:
    """A turret or module mount (e.g. the Hornet's nose and S5 centre slot).

    Candidates are turrets of the matching kind and size from the game data plus the stock
    parts of sibling variants at the same port; modules are hull-specific and only come
    from the siblings.

    Args:
        slug: Slug of the ship (catalog key prefix).
        v: Vehicle record of the ship.
        port: Port name of the mount.
        typ: Card type (``Turret`` or ``Mount``).
        siblings: Slugs of variants of the same hull.
        use_cache: Passed on to ``get``.

    Returns:
        The slot dict and its candidate entries.
    """
    p = next(x for x in v["ports"] if x["name"] == port)
    size = p["sizes"]["max"]
    subs = {s for c in p.get("compatible_types") or [] if isinstance(c, dict)
            and c.get("type") == "Turret" for s in c.get("sub_types") or []}
    found: dict = {}
    if subs:
        q = urllib.parse.urlencode({"filter[type]": "Turret", "filter[size]": size, "limit": 200})
        for it in get(f"items?{q}", f"items_Turret_{size}", use_cache)["data"]:
            if it.get("sub_type") in subs:
                found[it["uuid"]] = it
    stock = (p.get("equipped_item") or {}).get("uuid")
    uuids = [stock] if stock else []
    for sib in siblings:
        sv = get(f"v3/vehicles/{sib}", f"vehicle_{sib}", use_cache)["data"]
        sp = next((x for x in sv["ports"] if x["name"] == port), None)
        u = ((sp or {}).get("equipped_item") or {}).get("uuid")
        if u:
            uuids.append(u)
    for u in uuids:
        if u not in found:
            found[u] = get(f"items/{u}", f"item_{u}", use_cache)["data"]
    slot = {"id": port, "port": port, "type": typ, "size": size, "side": "C", "default": stock,
            "cat": f"{slug}:{port}",
            "subdef": {k: g["def"] for k, g in subgroups(p.get("ports")).items() if g["def"]}}
    return slot, [entry(it) for it in found.values()]


def attach_uex(data: dict, vehicles: list[dict]) -> list[str]:
    """Add the UEX vehicle id and full name to every ship, matched by name.

    The UEX id is the model key of the shared fleet (flotte.py) that the cargo
    ledger of the Handels-Planer uses as well.

    Args:
        data: Result of :func:`build`; changed in place (``uex``, ``model`` per ship).
        vehicles: UEX ``vehicles`` records of this build.

    Returns:
        Names of ships without a UEX match (their ``uex`` is None).
    """
    by = {}
    for v in vehicles:
        by.setdefault((v.get("name") or "").lower(), v)
    missing = []
    for s in data["ships"]:
        v = by.get(s["name"].lower())
        s["uex"] = v["id"] if v else None
        s["model"] = (v.get("name_full") or v.get("name")) if v else s["name"]
        if not v:
            missing.append(s["name"])
    return missing


def build(use_cache: bool = False) -> dict:
    """Build the data of the components tab for all ships.

    Args:
        use_cache: Use the local cache (development); CI always fetches fresh.

    Returns:
        ``{"ships": [...], "catalog": {...}, "types": TYPES, "patch": ..., "built": ...}``.

    Raises:
        OSError, ValueError: If the Wiki API is unreachable or answers unexpectedly; the
            caller builds the page without the tab in that case.
    """
    ships, cat, patch = [], {}, None
    for slug, cfg in SHIPS.items():
        v = get(f"v3/vehicles/{slug}", f"vehicle_{slug}", use_cache)["data"]
        patch = patch or v.get("version")
        sl = slots(v)
        for s in sl:
            key = f"{s['type']}_{s['size']}"
            if key not in cat:
                cat[key] = candidates(s["type"], s["size"], use_cache)
        for port, typ in cfg.get("extra", {}).items():
            s, c = extra_slot(slug, v, port, typ, cfg.get("siblings", []), use_cache)
            sl.append(s)
            cat[s["cat"]] = c
        sil = cfg["sil"]()
        ships.append({"slug": slug, "short": cfg["short"], "name": v["name"],
                      "maker": (v.get("manufacturer") or {}).get("name") or "", "sil": sil,
                      "anch": cfg["anch"], "panch": cfg["panch"], "slots": sl})
    # Catalogs of the sub-mounts (weapons in turrets, missiles in racks).
    for c in list(cat.values()):
        for it in c:
            for g in it["sub"]:
                if g["k"] not in cat:
                    cat[g["k"]] = candidates(g["type"], g["size"], use_cache)
    return {"ships": ships, "catalog": cat, "types": TYPES, "patch": patch,
            "built": time.strftime("%d.%m.%Y")}
