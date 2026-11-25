# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Schiffskauf-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       16.11.2026
# Geändert:       25.11.2026
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


def hull_b() -> dict:
    """MISC Hull B, silhouette v1 (left half, mirrored at x = 1724), accepted on 25.11.2026.

    Returns:
        Dict with viewBox, outline path, detail paths and circles (none).
    """
    ox, oy, cx = 1301, 110, 1724
    left = [(1724, 158), (1692, 168), (1665, 205), (1648, 260), (1636, 305), (1562, 325), (1556, 410),
            (1572, 440), (1572, 560), (1548, 640), (1545, 745), (1560, 760), (1560, 880), (1572, 940),
            (1600, 1030), (1632, 1085), (1650, 1095), (1724, 1095)]
    det = [_path([(1636, 305), (1812, 305), (1804, 455), (1644, 455)], ox, oy),        # canopy
           _path([(1698, 460), (1750, 460), (1750, 700), (1698, 700)], ox, oy),        # spine channel
           _path([(1655, 760), (1793, 760), (1785, 860), (1663, 860)], ox, oy),        # deck hatch
           _path([(1600, 720), (1848, 720)], ox, oy, False),                           # deck edge
           _path([(1630, 980), (1818, 980)], ox, oy, False)]                           # stern deck
    for side in (lambda p: p, lambda p: _mirror(p, cx)):
        det += [_path(side([(1572, 440), (1640, 470), (1645, 700)]), ox, oy, False),   # side panel
                _path(side([(1565, 750), (1590, 750), (1590, 845), (1565, 845)]), ox, oy)]  # tractor housing
    outline = _path(left + _mirror(left[1:-1], cx)[::-1], ox, oy)
    return {"viewBox": "214 28 420 978", "outline": outline, "details": det, "circles": []}


def clipper() -> dict:
    """Drake Clipper, silhouette v1 (whole outline: asymmetric, 3 racks left, 5 right), accepted 25.11.2026.

    Returns:
        Dict with viewBox, outline path, detail paths and circles (none).
    """
    ox, oy = 1150, 280
    pts = [(1700, 320), (1765, 320), (1782, 395), (1815, 640), (1840, 600), (1870, 590), (1930, 595),
           (1948, 640), (1950, 662), (2455, 660), (2460, 745), (2300, 805), (2100, 885), (1990, 935),
           (1945, 935), (1935, 968), (1860, 972), (1850, 905), (1800, 905), (1785, 960), (1765, 1000),
           (1745, 1095), (1680, 1095), (1660, 1000), (1645, 950), (1600, 930), (1560, 935), (1515, 920),
           (1500, 880), (1400, 838), (1300, 798), (1205, 760), (1195, 650), (1520, 655), (1525, 615),
           (1560, 605), (1600, 612), (1612, 640), (1632, 520), (1652, 420), (1688, 372)]
    det = [_path([(1700, 320), (1765, 320), (1765, 395), (1700, 395)], ox, oy),        # nose box
           _path([(1720, 400), (1745, 400), (1745, 900), (1720, 900)], ox, oy),        # spine
           _path([(1205, 705), (1515, 705)], ox, oy, False),                           # left wing spar
           _path([(1950, 705), (2455, 705)], ox, oy, False),                           # right wing spar
           _path([(1525, 615), (1600, 615), (1600, 925), (1525, 925)], ox, oy),        # left engine pod
           _path([(1850, 600), (1945, 600), (1945, 900), (1850, 900)], ox, oy),        # right engine pod
           _path([(1670, 1000), (1755, 1000)], ox, oy, False)]                         # stern
    return {"viewBox": "20 20 1320 840", "outline": _path(pts, ox, oy), "details": det, "circles": []}


def vulture() -> dict:
    """Drake Vulture, silhouette v1 (left half, mirrored at x = 1722), accepted on 25.11.2026.

    Returns:
        Dict with viewBox, outline path, detail paths and circles (none).
    """
    ox, oy, cx = 1300, 30, 1722
    left = [(1722, 640), (1670, 640), (1660, 660), (1602, 660), (1600, 300), (1592, 205), (1592, 65),
            (1572, 65), (1574, 205), (1507, 207), (1505, 790), (1557, 800), (1557, 935), (1452, 935),
            (1450, 1236), (1545, 1236), (1560, 1230), (1575, 1295), (1610, 1317), (1722, 1317)]
    det = [_path([(1680, 645), (1764, 645), (1764, 800), (1680, 800)], ox, oy),        # cockpit
           _path([(1640, 960), (1804, 960), (1804, 1220), (1640, 1220)], ox, oy)]      # cargo deck
    for side in (lambda p: p, lambda p: _mirror(p, cx)):
        det += [_path(side([(1507, 207), (1600, 207)]), ox, oy, False),                # arm tip
                _path(side([(1557, 935), (1557, 1236)]), ox, oy, False)]               # pod seam
    outline = _path(left + _mirror(left[1:-1], cx)[::-1], ox, oy)
    return {"viewBox": "120 15 610 1300", "outline": outline, "details": det, "circles": []}


def mole() -> dict:
    """Argo MOLE, silhouette v1 (left half, mirrored at x = 1720), accepted on 25.11.2026.

    Returns:
        Dict with viewBox, outline path, detail paths and circles (none).
    """
    ox, oy, cx = 1300, 50, 1720
    left = [(1720, 95), (1617, 95), (1574, 214), (1546, 293), (1503, 300), (1500, 486), (1510, 540),
            (1467, 529), (1400, 535), (1396, 914), (1381, 943), (1381, 1350), (1560, 1357),
            (1580, 1214), (1630, 1220), (1720, 1220)]
    det = [_path([(1650, 260), (1790, 260), (1760, 400), (1680, 400)], ox, oy),        # canopy
           _path([(1650, 560), (1790, 560), (1790, 1200), (1650, 1200)], ox, oy)]      # cargo spine
    for side in (lambda p: p, lambda p: _mirror(p, cx)):
        det += [_path(side([(1503, 300), (1546, 300)]), ox, oy, False),                # side cabin
                _path(side([(1400, 914), (1560, 914)]), ox, oy, False)]                # engine block
    outline = _path(left + _mirror(left[1:-1], cx)[::-1], ox, oy)
    return {"viewBox": "50 25 740 1310", "outline": outline, "details": det, "circles": []}


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
    "misc-hull-b": {
        "short": "Hull B", "sil": hull_b,
        "anch": {},
        # Weapons 1-4 as marked by the author (25.11.2026, top, side and front view); the
        # tractor beams (5, 6) are not part of the tab yet. Other components generic in the hull.
        "panch": {
            "hardpoint_weapon_left": {"xy": [329, 190], "pos": "unten", "low": True},
            "hardpoint_weapon_right": {"xy": [517, 190], "pos": "unten", "low": True},
            "weapon_left": {"xy": [410, 510], "pos": "oben"},
            "weapon_right": {"xy": [436, 510], "pos": "oben"},
            "hardpoint_missile_rack": {"xy": [423, 65], "pos": "unten", "low": True},
            "hardpoint_radar": {"xy": [423, 140]},
            "hardpoint_shield_generator_front_left": {"xy": [299, 370], "col": "L"},
            "hardpoint_shield_generator_front_right": {"xy": [547, 370], "col": "R"},
            "hardpoint_shield_generator_rear_left": {"xy": [299, 590], "col": "L"},
            "hardpoint_shield_generator_rear_right": {"xy": [547, 590], "col": "R"},
            "hardpoint_cooler_left": {"xy": [319, 790], "col": "L"},
            "hardpoint_cooler_right": {"xy": [529, 790], "col": "R"},
            "hardpoint_power_plant": {"xy": [423, 690]},
            "hardpoint_quantum_drive": {"xy": [423, 890]},
        },
    },
    "clipper": {
        "short": "Clipper", "sil": clipper,
        "anch": {},
        # All 12 weapons as marked by the author (25.11.2026), all on the underside. The data does
        # not say which rack sits inside: racks are numbered from the hull outwards (left_1..3,
        # right_1..5), as the author numbered them. Other components generic in the hull.
        "panch": {
            "hardpoint_weapon_left": {"xy": [540, 85], "pos": "unten", "low": True},
            "hardpoint_weapon_right": {"xy": [625, 85], "pos": "unten", "low": True},
            "hardpoint_weapon_wing_left": {"xy": [355, 410], "pos": "unten", "low": True},
            "hardpoint_weapon_wing_right": {"xy": [805, 410], "pos": "unten", "low": True},
            "hardpoint_missile_rack_left_1": {"xy": [290, 425], "pos": "unten", "low": True},
            "hardpoint_missile_rack_left_2": {"xy": [220, 425], "pos": "unten", "low": True},
            "hardpoint_missile_rack_left_3": {"xy": [150, 425], "pos": "unten", "low": True},
            "hardpoint_missile_rack_right_1": {"xy": [930, 425], "pos": "unten", "low": True},
            "hardpoint_missile_rack_right_2": {"xy": [990, 425], "pos": "unten", "low": True},
            "hardpoint_missile_rack_right_3": {"xy": [1059, 425], "pos": "unten", "low": True},
            "hardpoint_missile_rack_right_4": {"xy": [1140, 425], "pos": "unten", "low": True},
            "hardpoint_missile_rack_right_5": {"xy": [1222, 425], "pos": "unten", "low": True},
            "hardpoint_radar": {"xy": [582, 160]},
            "hardpoint_shield_generator_1": {"xy": [548, 330], "col": "L"},
            "hardpoint_shield_generator_2": {"xy": [618, 330], "col": "R"},
            "hardpoint_cooler": {"xy": [582, 480]},
            "hardpoint_power_plant_1": {"xy": [548, 600], "col": "L"},
            "hardpoint_power_plant_2": {"xy": [618, 600], "col": "R"},
            "hardpoint_quantum_drive": {"xy": [582, 740]},
        },
    },
    "vulture": {
        "short": "Vulture", "sil": vulture,
        "anch": {},
        # Guns 1/2 and salvage heads 3/4 as marked by the author (25.11.2026). The tab does not
        # offer salvage heads yet; their positions are kept for the salvage extension.
        "panch": {
            "hardpoint_weapon_nose_left": {"xy": [300, 760]},
            "hardpoint_weapon_nose_right": {"xy": [544, 760]},
            "hardpoint_salvage_arm_left": {"xy": [282, 110]},
            "hardpoint_salvage_arm_right": {"xy": [562, 110]},
            "hardpoint_radar": {"xy": [422, 670]},
            "hardpoint_shield_generator_left": {"xy": [310, 970], "col": "L"},
            "hardpoint_shield_generator_right": {"xy": [534, 970], "col": "R"},
            "hardpoint_shield_generator_rear": {"xy": [422, 1250]},
            "hardpoint_cooler_left": {"xy": [200, 1050], "col": "L"},
            "hardpoint_cooler_right": {"xy": [644, 1050], "col": "R"},
            "hardpoint_power_plant_01": {"xy": [390, 1070], "col": "L"},
            "hardpoint_power_plant_02": {"xy": [454, 1070], "col": "R"},
            "hardpoint_quantum_drive": {"xy": [422, 1150]},
        },
    },
    "mole": {
        "short": "MOLE", "sil": mole,
        "anch": {},
        # Guns 1/2 and mining lasers 3-5 as marked by the author (25.11.2026). The tab does not
        # offer mining lasers yet; their positions are kept for the mining extension.
        "panch": {
            "hardpoint_gun_left": {"xy": [290, 200], "pos": "oben"},
            "hardpoint_gun_right": {"xy": [550, 200], "pos": "oben"},
            "hardpoint_mining_cab_front": {"xy": [420, 60], "pos": "unten", "low": True},
            "hardpoint_mining_cab_left": {"xy": [190, 570]},
            "hardpoint_mining_cab_right": {"xy": [650, 570]},
            "hardpoint_radar": {"xy": [420, 400]},
            "hardpoint_radar_cab_front": {"xy": [420, 95]},
            "hardpoint_radar_cab_left": {"xy": [190, 610], "col": "L"},
            "hardpoint_radar_cab_right": {"xy": [650, 610], "col": "R"},
            "hardpoint_shield_generator_left": {"xy": [300, 650], "col": "L"},
            "hardpoint_cooler": {"xy": [420, 850]},
            "hardpoint_power_plant": {"xy": [420, 1000]},
            "hardpoint_quantum_drive": {"xy": [420, 1130]},
        },
    },
}
