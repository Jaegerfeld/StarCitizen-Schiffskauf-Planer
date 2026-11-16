# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Schiffskauf-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       16.11.2026
# Geändert:       16.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Schiffe des Reiters „Komponenten“: eigene, stark stilisierte Draufsicht je
#   Schiff und die Einbauorte der Komponenten darin. Die Umrisse sind von Hand
#   nach eigenen Ingame-Screenshots gezeichnet (keine fremden Bildwerke), die
#   Waffenpunkte hat der Autor im eigenen Screenshot markiert; Nicht-Waffen-
#   Komponenten stehen generisch im Rumpf. Neues Schiff: Silhouette + Eintrag
#   in SHIPS; die Steckplätze selbst kommen aus den Spieldaten (komponenten.py).
# =============================================================================
"""Ships of the components tab: hand-drawn top views and mount positions.

Coordinates are pixels of the author's own top-view screenshot (3440 x 1440); each
silhouette is drawn as one half and mirrored at the hull's centre line. The page
draws the SVG from the returned path strings.
"""
from __future__ import annotations


def _mirror(pts: list[tuple[int, int]], cx: int) -> list[tuple[int, int]]:
    """Mirror points at the vertical centre line x = cx."""
    return [(2 * cx - x, y) for x, y in pts]


def _path(pts: list[tuple[int, int]], ox: int, oy: int, close: bool = True) -> str:
    """SVG path through the points, shifted by the view origin (ox, oy)."""
    return "M" + " L".join(f"{x - ox},{y - oy}" for x, y in pts) + (" Z" if close else "")


def hornet_mk2() -> dict:
    """F7C Hornet Mk II, silhouette v2 (right half, mirrored at x = 1721).

    Returns:
        Dict with viewBox, outline path, detail paths and circles (the S5 ring).
    """
    ox, oy, cx = 1300, 330, 1721
    right = [(1721, 366), (1746, 367), (1750, 400), (1768, 505), (1800, 515), (1832, 552),
             (1835, 597), (1862, 630), (1862, 648), (1865, 670), (2045, 902), (2027, 955),
             (1868, 850), (1887, 1185), (1915, 1200), (1912, 1222), (1895, 1222), (1890, 1245),
             (1882, 1246), (1845, 1165), (1721, 1162)]
    det = [_path([(1700, 420), (1742, 420), (1745, 550), (1697, 550)], ox, oy),  # canopy
           _path([(1700, 555), (1742, 555)], ox, oy, False)]
    for side in (lambda p: p, lambda p: _mirror(p, cx)):
        det += [_path(side([(1768, 505), (1772, 600), (1835, 597)]), ox, oy, False),  # intake
                _path(side([(1880, 700), (2032, 905)]), ox, oy, False),              # wing panel
                _path(side([(1875, 860), (2010, 935)]), ox, oy, False),              # trailing edge
                _path(side([(1800, 950), (1815, 1100)]), ox, oy, False),             # hull gap
                _path(side([(1868, 850), (1885, 1170)]), ox, oy, False)]             # boom edge
    det += [_path([(1640, 1095), (1802, 1095)], ox, oy, False),                      # deck
            _path([(1655, 945), (1787, 945), (1787, 1060), (1655, 1060)], ox, oy)]   # engine
    outline = _path(right + _mirror(right[1:-1], cx)[::-1], ox, oy)
    return {"viewBox": "60 10 780 950", "outline": outline, "details": det,
            "circles": [[cx - ox, 720 - oy, 105], [cx - ox, 720 - oy, 68]]}


def guardian_mx() -> dict:
    """Mirai Guardian MX, silhouette v1 (left half, mirrored at x = 1722).

    The screenshot was taken slightly off-centre; the left side is authoritative.

    Returns:
        Dict with viewBox, outline path, detail paths and circles (none).
    """
    ox, oy, cx = 1301, 290, 1722
    left = [(1722, 520), (1690, 523), (1665, 532), (1652, 560), (1648, 620), (1596, 625),
            (1594, 390), (1580, 345), (1562, 314), (1499, 322), (1451, 574), (1434, 615),
            (1402, 759), (1365, 815), (1356, 896), (1443, 1087), (1499, 1124), (1515, 1146),
            (1527, 1206), (1559, 1215), (1621, 1212), (1652, 1190), (1665, 1146), (1690, 1162),
            (1722, 1165)]
    det = []
    for side in (lambda p: p, lambda p: _mirror(p, cx)):
        det += [_path(side([(1580, 345), (1582, 1085)]), ox, oy, False),               # wing spar
                _path(side([(1452, 574), (1546, 524)]), ox, oy, False),                # upper facet
                _path(side([(1468, 721), (1546, 652)]), ox, oy, False),                # lower facet
                _path(side([(1484, 777), (1502, 1052), (1530, 1100)]), ox, oy, False), # side panel
                _path(side([(1648, 620), (1640, 1140)]), ox, oy, False),               # hull edge
                _path(side([(1515, 1146), (1585, 1130), (1655, 1146)]), ox, oy, False)]  # nacelle
    det.append(_path([(1680, 1100), (1764, 1100)], ox, oy, False))                       # tail
    outline = _path(left + _mirror(left[1:-1], cx)[::-1], ox, oy)
    return {"viewBox": "26 0 790 950", "outline": outline, "details": det, "circles": []}


#: Ships of the tab, in display order. Keys are slugs of the Star Citizen Wiki API.
#: ``anch``: generic mount positions per component type and side (L/R/C list);
#: ``panch``: exact positions per port (``pos`` oben/unten/nase, ``low`` = underside, drawn
#: dashed, ``col`` = card column only). ``extra``: ports the data marks as turret or module
#: mounts, offered with the parts of ``siblings`` (variants of the same hull).
SHIPS: dict[str, dict] = {
    "f7c-hornet-mk-ii": {
        "short": "Hornet Mk II", "sil": hornet_mk2,
        # Weapons as marked by the author on his own screenshot (15.11.2026), rest generic.
        "anch": {"WeaponGun": {"L": [188, 430], "R": [654, 430]},
                 "MissileLauncher": {"L": [290, 430], "R": [540, 430]},
                 "Shield": {"L": [380, 560], "R": [462, 560]},
                 "Cooler": {"L": [372, 740], "R": [470, 740]},
                 "PowerPlant": {"C": [[398, 680], [444, 680]]},
                 "QuantumDrive": {"C": [[421, 790]]}, "Radar": {"C": [[421, 120]]}},
        "panch": {"hardpoint_weapon_nose": {"xy": [421, 42], "pos": "nase"},
                  "hardpoint_weapon_center": {"xy": [421, 375], "pos": "oben", "col": "R"}},
        "extra": {"hardpoint_weapon_nose": "Turret", "hardpoint_weapon_center": "Mount"},
        "siblings": ["f7a-hornet-mk-ii", "f7c-m-super-hornet-mk-ii",
                     "f7c-m-hornet-heartseeker-mk-ii", "f7c-s-hornet-ghost-mk-ii",
                     "f7c-r-hornet-tracker-mk-ii"],
    },
    "guardian-mx": {
        "short": "Guardian MX", "sil": guardian_mx,
        "anch": {},
        # Weapons 1-6 as marked by the author (16.11.2026, top, front and side view).
        "panch": {
            "hardpoint_weapon_wing_top_left": {"xy": [286, 245], "pos": "oben"},
            "hardpoint_weapon_wing_top_right": {"xy": [556, 245], "pos": "oben"},
            "hardpoint_weapon_wing_bottom_left": {"xy": [286, 272], "pos": "unten", "low": True},
            "hardpoint_weapon_wing_bottom_right": {"xy": [556, 272], "pos": "unten", "low": True},
            "hardpoint_missile_top_left": {"xy": [197, 340]},
            "hardpoint_missile_top_right": {"xy": [645, 340]},
            "hardpoint_radar": {"xy": [421, 245]},
            "hardpoint_shield_generator_01": {"xy": [395, 420], "col": "L"},
            "hardpoint_shield_generator_02": {"xy": [447, 420], "col": "R"},
            "hardpoint_power_plant_s2": {"xy": [405, 760]},
            "hardpoint_cooler_s1": {"xy": [395, 640], "col": "L"},
            "hardpoint_cooler_s2": {"xy": [447, 640], "col": "R"},
            "hardpoint_quantum_drive": {"xy": [437, 820]},
        },
    },
}
