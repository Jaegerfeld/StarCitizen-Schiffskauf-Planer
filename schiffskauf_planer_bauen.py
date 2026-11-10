# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Schiffskauf-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       10.11.2026
# Geändert:       10.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Baut den SC Schiffskauf-Planer: eine einzelne, offline lauffähige HTML-Seite,
#   in der man ingame kaufbare Schiffe und Fahrzeuge nach Schiff oder nach
#   Standort durchsucht, sortiert und auf einer Merkliste mit Budget sammelt.
#   Quelle ist die öffentliche UEX-API (Kaufpreise je Terminal, Fahrzeug-
#   stammdaten, Terminals, aktueller Spielstand).
#   Erzeugt im Skript-Ordner:
#     SC_Schiffskauf_Planer.html  die App mit eingebetteten Daten
#     data.json                   derselbe Datenstand; der Knopf „Neuesten Stand
#                                 laden“ holt ihn zur Laufzeit von GitHub Pages
#   Kopfzeile, Design und „Was ist neu?“-Dialog kommen aus kopfzeile.py und
#   sc_design.py (gemeinsam mit den anderen SC-Tools). Die Seite ruft UEX nie
#   selbst auf; aktuelle Daten kommen nur aus dem Build.
# =============================================================================
"""Build the ship purchase planner page and data.json from the UEX API.

Usage:
  py schiffskauf_planer_bauen.py            fetch from UEX and build
  py schiffskauf_planer_bauen.py --cache    use uex_cache.json instead of UEX (dev)
"""
import json
import pathlib
import re
import sys
import urllib.request
from datetime import datetime, timezone

import kopfzeile as kz
import sc_design as sd
from version import VERSION

#: Script folder; all outputs are written here.
HERE = pathlib.Path(__file__).resolve().parent
#: The generated app with embedded data.
OUT_HTML = HERE / "SC_Schiffskauf_Planer.html"
#: Same data as the page; fetched by the in-app refresh button.
OUT_JSON = HERE / "data.json"
#: Raw UEX data for offline development (--cache).
CACHE = HERE / "uex_cache.json"
#: Base URL of the UEX API.
API = "https://api.uexcorp.space/2.0/"
#: UEX endpoints the build needs.
ENDPOINTS = ("vehicles_purchases_prices_all", "vehicles", "terminals", "companies",
             "game_versions")
#: Tool key in the shared header.
TOOL = "schiffskauf"
#: Published data.json the page loads on "Load latest build".
DATA_URL = "https://jaegerfeld.github.io/StarCitizen-Schiffskauf-Planer/data.json"
#: UEX role flags offered as filter, in display order. Labels live in the page script.
ROLE_FLAGS = ("starter", "cargo", "mining", "salvage", "medical", "repair", "refuel",
              "exploration", "science", "passenger", "racing", "military", "stealth",
              "bomber", "interdiction", "construction")
#: A build below this many price rows means UEX answered with partial data; abort instead.
MIN_PRICE_ROWS = 100


def fetch(endpoint):
    """Fetch one UEX endpoint and return its data value.

    Args:
        endpoint: Endpoint name below the API base URL.

    Returns:
        The decoded ``data`` value of the response.

    Raises:
        urllib.error.URLError: On network or HTTP errors.
        ValueError: If the response is not valid JSON or reports an error status.
    """
    req = urllib.request.Request(API + endpoint, headers={"User-Agent": "Mozilla/5.0 sc-schiffe"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read().decode("utf-8"))
    if body.get("status") != "ok":
        raise ValueError(f"{endpoint}: status {body.get('status')}")
    return body["data"]


def load_raw(use_cache):
    """Load all UEX endpoints from the API or from the local cache.

    Args:
        use_cache: Read ``uex_cache.json`` instead of calling UEX.

    Returns:
        Dict mapping endpoint name to its data value.
    """
    if use_cache:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    raw = {e: fetch(e) for e in ENDPOINTS}
    CACHE.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    return raw


def parse_crew(value):
    """Parse the UEX crew text into a minimum and maximum.

    UEX writes crew as "2", "1,4" or "1-4"; some vehicles have no value at all.

    Args:
        value: Raw crew value from UEX.

    Returns:
        List ``[min, max]``, or None if the value holds no number.
    """
    nums = [int(n) for n in re.findall(r"\d+", str(value or ""))]
    return [min(nums), max(nums)] if nums else None


def location_record(term):
    """Convert a UEX terminal into a location record of the page.

    The terminal name has the form "Shop - Place" or "Shop - Hall - Place"; the last
    part repeats the place, so it is cut off to get the shop name.

    Args:
        term: UEX terminal dict.

    Returns:
        Dict with terminal id, star system, planet, place and shop name.
    """
    parts = term["name"].split(" - ")
    return {"id": term["id"], "sys": term.get("star_system_name") or "",
            "body": term.get("planet_name") or "",
            "place": term.get("city_name") or term.get("space_station_name") or parts[-1],
            "shop": " – ".join(parts[:-1]) or term["name"]}


def ship_record(veh, offers, companies):
    """Convert a UEX vehicle and its offers into a ship record of the page.

    Args:
        veh: UEX vehicle dict.
        offers: List of ``[terminal id, price]``.
        companies: Mapping of company id to company name.

    Returns:
        Dict with id, name, manufacturer, ground flag, roles, cargo, crew, length and offers.
    """
    return {"id": veh["id"], "n": veh["name_full"], "m": companies.get(veh["id_company"], ""),
            "g": 1 if veh.get("is_ground_vehicle") else 0,
            "r": [f for f in ROLE_FLAGS if veh.get("is_" + f)],
            "scu": veh.get("scu") or 0, "crew": parse_crew(veh.get("crew")),
            "len": veh.get("length") or None,
            "p": sorted(offers, key=lambda o: o[1])}


def build_data(raw):
    """Build the compact data object embedded in the page and written to data.json.

    Only terminals marked as available in the live game count; a vehicle without any
    remaining offer is left out.

    Args:
        raw: Dict from load_raw().

    Returns:
        Dict with schema, version, patch, build time, report date range, locs and ships.

    Raises:
        ValueError: If UEX delivered fewer price rows than plausible.
    """
    prices = raw["vehicles_purchases_prices_all"]
    if len(prices) < MIN_PRICE_ROWS:
        raise ValueError(f"nur {len(prices)} Preiszeilen von UEX")
    terminals = {t["id"]: t for t in raw["terminals"] if t.get("is_available_live")}
    vehicles = {v["id"]: v for v in raw["vehicles"]}
    companies = {c["id"]: c["name"] for c in raw["companies"]}
    offers, used, dates = {}, set(), []
    for row in prices:
        tid, vid = row["id_terminal"], row["id_vehicle"]
        if tid in terminals and vid in vehicles and row.get("price_buy"):
            offers.setdefault(vid, []).append([tid, row["price_buy"]])
            used.add(tid)
            dates.append(row["date_modified"])
    locs = sorted((location_record(terminals[t]) for t in used),
                  key=lambda x: (x["sys"], x["place"], x["shop"]))
    ships = sorted((ship_record(vehicles[v], o, companies) for v, o in offers.items()),
                   key=lambda s: s["n"])

    def day(ts):
        """Format a UNIX timestamp as an ISO date."""
        return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d")

    return {"schema": 1, "version": VERSION, "patch": raw["game_versions"].get("live", ""),
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "from": day(min(dates)), "to": day(max(dates)), "locs": locs, "ships": ships}


def bilingual(html):
    """Replace ``{{Deutsch|English}}`` markers with language spans the page CSS switches.

    Args:
        html: Page template.

    Returns:
        The template with all markers replaced.
    """
    return re.sub(r"\{\{([^|{}]*)\|([^|{}]*)\}\}",
                  r'<span class="de">\1</span><span class="en">\2</span>', html)


def fill_header(html):
    """Insert the shared header, design CSS/JS, fonts, "What's new?" dialog and changelog.

    Args:
        html: The page template with its placeholders.

    Returns:
        The template with all kopfzeile.py / sc_design.py placeholders replaced.
    """
    b = kz.bi
    refresh = ('<button class="btn fh-btn" id="refreshBtn" type="button">'
               f'🔄 {b("Neuesten Stand laden (GitHub)", "Load latest build (GitHub)")}</button>')
    head = kz.header_html(
        TOOL,
        eyebrow=("Schiffe · Preise · Standorte", "Ships · Prices · Locations"),
        title=("SC Schiffskauf-Planer", "SC Ship Purchase Planner"),
        lede=("Welches Schiff wo am günstigsten ist und was an deinem Standort verkauft wird. "
              "Community-Daten von UEX – vor dem Kauf im Spiel gegenprüfen.",
              "Where each ship is cheapest and what is sold at your location. "
              "Community data from UEX – verify in game before buying."),
        version=VERSION, refresh=refresh, data='<span id="buildStat"></span>')
    html = html.replace("<!--FH_HEADER-->", head)
    html = html.replace("/*FH_CSS*/", kz.CSS + sd.CSS).replace("/*FH_JS*/", kz.JS + sd.JS)
    html = html.replace("<!--SD_FONTS-->", sd.FONTS)
    return html.replace("<!--FH_DIALOG-->", kz.dialog_html(TOOL, VERSION) + "\n"
                        + kz.changelog_script(HERE / "CHANGELOG.md"))


def main(argv):
    """Fetch the data and write the page and data.json.

    Args:
        argv: Command-line arguments (--cache).

    Returns:
        Exit code: 0 on success, 1 if UEX is unreachable or its data is implausible.
    """
    try:
        data = build_data(load_raw("--cache" in argv))
    except Exception as e:  # noqa: BLE001
        print(f"FEHLER: UEX-Daten nicht verfügbar: {e}", file=sys.stderr)
        return 1
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = fill_header(bilingual(HTML_TEMPLATE))
    html = html.replace("/*__DATA__*/{}", payload).replace("__DATA_URL__", DATA_URL)
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_JSON.write_text(payload, encoding="utf-8")
    print(f"Geschrieben: {OUT_HTML.name} ({OUT_HTML.stat().st_size // 1024} KB), {OUT_JSON.name}")
    print(f"  {len(data['ships'])} Fahrzeuge, {len(data['locs'])} Standorte, "
          f"Spielstand {data['patch']}, Preise gemeldet {data['from']} bis {data['to']}.")
    return 0


# ============================================================ HTML template
#: Page template; placeholders are filled by bilingual(), fill_header() and main().
HTML_TEMPLATE = r"""<!DOCTYPE html>
<!-- SC Schiffskauf-Planer (SC Ship Purchase Planner) - generated by schiffskauf_planer_bauen.py, do not edit this file by hand -->
<html lang="de" data-lang="de" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SC Schiffskauf-Planer</title>
<meta name="description" content="Star Citizen Schiffskauf-Planer: ingame kaufbare Schiffe nach Schiff oder Standort sortieren, Preise vergleichen, Merkliste mit Budget. Daten: UEX.">
<!--SD_FONTS-->
<style>
  *{box-sizing:border-box}
  :root[data-lang="de"] .en,:root[data-lang="en"] .de{display:none!important}
  .wrap{max-width:1400px;margin:0 auto;padding:0 16px 60px}
  .tabs{display:flex;gap:6px;margin:14px 0 0;border-bottom:1px solid var(--line)}
  .tab{font-family:var(--disp);font-weight:700;font-size:16px;letter-spacing:.03em;background:transparent;color:var(--muted);border:0;border-bottom:3px solid transparent;padding:10px 16px;min-height:44px;cursor:pointer}
  .tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
  .filters{display:flex;flex-wrap:wrap;gap:10px 12px;align-items:flex-end;margin:14px 0 6px}
  .f{display:flex;flex-direction:column;gap:3px;font-size:12.5px;color:var(--muted);min-width:130px}
  .f.grow{flex:1 1 220px}
  .f input,.f select{width:100%}
  details.more{margin:0 0 6px}
  details.more>summary{cursor:pointer;font-family:var(--disp);font-weight:600;color:var(--accent2);min-height:32px;display:inline-flex;align-items:center}
  .resultbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:6px 0 10px;font-size:13.5px;color:var(--muted)}
  .layout{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:18px;align-items:start}
  table{width:100%;border-collapse:collapse;background:var(--panel)}
  th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-size:14px}
  td.num,th.num{text-align:right;white-space:nowrap}
  th{font-family:var(--disp);font-size:13.5px;color:var(--muted);background:var(--panel2);white-space:nowrap}
  th button{all:unset;cursor:pointer;display:inline-block;padding:2px 0}
  th button:hover{color:var(--accent)}
  th button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  th[aria-sort="ascending"],th[aria-sort="descending"]{color:var(--accent)}
  .name{font-weight:700}
  .sub{font-size:12.5px;color:var(--muted)}
  .price{font-weight:700;white-space:nowrap}
  .best{display:inline-block;font-size:11.5px;font-weight:700;color:var(--oktx);background:var(--okbg);border:1px solid var(--okbd);border-radius:6px;padding:0 6px;white-space:nowrap}
  .alts{margin-top:3px;font-size:12.5px;color:var(--muted)}
  .wbtn{font-family:var(--disp);font-weight:600;font-size:13px;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:4px 10px;min-height:32px;cursor:pointer;white-space:nowrap}
  .wbtn:hover{border-color:var(--accent);color:var(--accent)}
  .wbtn[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--onaccent)}
  .sysh{font-family:var(--disp);font-size:22px;margin:20px 0 8px;color:var(--accent2)}
  .sysh:first-child{margin-top:0}
  details.loc{margin:0 0 12px;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--panel)}
  details.loc>summary{cursor:pointer;padding:10px 14px;display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;background:var(--panel2)}
  details.loc>summary b{font-family:var(--disp);font-size:18px}
  .side{position:sticky;top:12px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;max-height:calc(100vh - 24px);overflow:auto}
  .side h2{font-family:var(--disp);font-size:20px;margin:0 0 8px}
  .stop{margin:12px 0}
  .stop h3{font-family:var(--disp);font-size:15px;margin:0 0 4px;display:flex;justify-content:space-between;gap:8px;color:var(--accent)}
  .witem{padding:6px 0;border-top:1px solid var(--line)}
  .witem .top{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
  .witem .row{display:flex;gap:6px;margin-top:4px}
  .witem select{flex:1 1 auto;min-width:0;font-size:12.5px}
  .sum{border-top:2px solid var(--line);margin-top:10px;padding-top:8px;display:grid;grid-template-columns:1fr auto;gap:3px 10px;font-size:14px}
  .sum .v{text-align:right;font-weight:700;white-space:nowrap}
  .sum .over{color:var(--bad)} .sum .okv{color:var(--ok)}
  .hint{margin-top:10px;padding:8px 10px;background:var(--warnbg);border-radius:8px;font-size:13px}
  .hint .btn{margin-top:6px;width:100%}
  .sidefoot{margin-top:14px;text-align:right}
  .empty{padding:28px;text-align:center;background:var(--panel);border:1px dashed var(--line);border-radius:10px;color:var(--muted)}
  .empty .btn{margin-top:10px}
  #toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:var(--panel);color:var(--ink);border:1px solid var(--accent);border-radius:10px;padding:10px 16px;box-shadow:var(--shadow);z-index:50;max-width:90vw}
  footer{margin-top:28px;font-size:12.5px;color:var(--muted)}
  footer a{color:var(--accent)}
  @media (max-width:919px){.layout{grid-template-columns:minmax(0,1fr)} .side{position:static;max-height:none}}
  @media (max-width:700px){.hide-s{display:none} .f{min-width:calc(50% - 6px);flex:1 1 calc(50% - 6px)} .f.grow{flex-basis:100%} th,td{padding:7px 6px}}
  @media (pointer:coarse){.wbtn,.tab{min-height:44px}}
  /*FH_CSS*/
</style>
</head>
<body>
<div class="hazard"></div>
<div class="wrap">
<!--FH_HEADER-->
<div class="sc-ptabs" id="ptabs"></div>
<div class="layout">
  <main id="mainPanel">
    <div class="tabs" role="tablist">
      <button class="tab" role="tab" type="button" data-view="ship">{{Nach Schiff|By ship}}</button>
      <button class="tab" role="tab" type="button" data-view="loc">{{Nach Standort|By location}}</button>
    </div>
    <div class="filters">
      <label class="f grow">{{Suche|Search}}<input type="search" id="q" autocomplete="off"></label>
      <label class="f">{{System|System}}<select id="sys"></select></label>
      <label class="f">{{Standort|Location}}<select id="loc"></select></label>
      <label class="f">{{Rolle|Role}}<select id="role"></select></label>
      <label class="f">{{Budget max. (aUEC)|Max. budget (aUEC)}}<input type="text" inputmode="decimal" id="budget" autocomplete="off"></label>
      <label class="f">{{Sortieren nach|Sort by}}<select id="sort"></select></label>
      <button class="btn" id="dirBtn" type="button"></button>
    </div>
    <details class="more"><summary>{{Weitere Filter|More filters}}</summary>
      <div class="filters">
        <label class="f">{{Hersteller|Manufacturer}}<select id="man"></select></label>
        <label class="f">{{Art|Type}}<select id="type"></select></label>
        <label class="f">{{Fracht mind. (SCU)|Min. cargo (SCU)}}<input type="number" min="0" id="scu"></label>
      </div>
    </details>
    <div class="resultbar" aria-live="polite"><span id="count"></span><button class="btn" id="resetBtn" type="button">{{Filter zurücksetzen|Reset filters}}</button></div>
    <div id="content"></div>
    <footer>{{Inoffiziell, nicht mit Cloud Imperium Games verbunden. Preise sind Community-Meldungen von|Unofficial, not affiliated with Cloud Imperium Games. Prices are community reports from}} <a href="https://uexcorp.space" target="_blank" rel="noopener">UEX</a>. {{Alle Angaben ohne Gewähr.|No guarantee of accuracy.}}</footer>
  </main>
  <aside class="side" id="wishPanel"><h2>{{Merkliste|Wishlist}}</h2><div id="wish"></div></aside>
</div>
</div>
<div id="toast" role="status" hidden></div>
<!--FH_DIALOG-->
<script>
const RAW = /*__DATA__*/{};
const DATA_URL = '__DATA_URL__';
const LS = {theme:'scsk_theme', lang:'scsk_lang', raw:'scsk_raw', state:'scsk_state'};
const root = document.documentElement;
const $ = s => document.querySelector(s);

/* ---------- storage and text ---------- */
// Read a JSON value from localStorage; null if missing or storage is blocked.
function load(k){try{const v=localStorage.getItem(k);return v?JSON.parse(v):null;}catch(e){return null;}}
// Write a JSON value to localStorage; ignores blocked storage.
function save(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
// Escape HTML special characters of API text.
const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

const I18N = {
  de:{all:'Alle',allSys:'Alle Systeme',allLoc:'Alle Standorte',allRole:'Alle Rollen',allMan:'Alle Hersteller',allType:'Schiffe und Fahrzeuge',space:'Nur Raumschiffe',ground:'Nur Bodenfahrzeuge',
    name:'Name',man:'Hersteller',price:'Preis',loc:'Standort',scu:'Fracht (SCU)',crew:'Crew',len:'Länge (m)',ship:'Schiff',here:'Preis hier',cmp:'Vergleich',asc:'↑ Aufsteigend',desc:'↓ Absteigend',
    hits:n=>`${n} ${n===1?'Treffer':'Treffer'}`,hitsLoc:(n,l)=>`${n} Angebote an ${l} ${l===1?'Standort':'Standorten'}`,offers:n=>`${n} ${n===1?'Schiff':'Schiffe'}`,from:'ab',cheapest:'günstigster Ort',only:'nur hier',also:'Auch:',
    save:'Merken',saved:'Gemerkt ✓',none:'Keine Schiffe passen zu diesen Filtern.',wishEmpty:'Noch nichts gemerkt. Klicke in der Liste bei einem Schiff auf „Merken“. Hier siehst du dann Summe, Budget und deine Kaufstopps.',
    remove:'Entfernen',total:'Summe',stops:'Kaufstopps',budget:'Budget',rest:'Bleibt übrig',missing:'Fehlt',oneStop:(l,d)=>`Alles auch in ${l} erhältlich${d>0?`, ${money(d)} teurer als die günstigste Verteilung`:''}.`,useOne:'Alles dort kaufen',cheapAll:'Alle auf günstigsten Ort setzen',clear:'Liste leeren',clearAsk:'Merkliste wirklich leeren?',
    search:'Schiff oder Hersteller',budgetPh:'z. B. 5m oder 2.500.000',stat:d=>`${d.ships.length} Fahrzeuge · ${d.locs.length} Standorte · Spielstand ${d.patch} · Preise gemeldet ${d.from} bis ${d.to} · gebaut ${d.generated}`,busy:'Lädt …',loaded:'Stand geladen:',failed:'Laden fehlgeschlagen. Die eingebauten Daten bleiben aktiv.',
    roles:{starter:'Starter',cargo:'Fracht',mining:'Bergbau',salvage:'Bergung',medical:'Medizin',repair:'Reparatur',refuel:'Betankung',exploration:'Erkundung',science:'Forschung',passenger:'Passagiere',racing:'Rennen',military:'Militär',stealth:'Tarnung',bomber:'Bomber',interdiction:'Abfangen',construction:'Bau'}},
  en:{all:'All',allSys:'All systems',allLoc:'All locations',allRole:'All roles',allMan:'All manufacturers',allType:'Ships and vehicles',space:'Spaceships only',ground:'Ground vehicles only',
    name:'Name',man:'Manufacturer',price:'Price',loc:'Location',scu:'Cargo (SCU)',crew:'Crew',len:'Length (m)',ship:'Ship',here:'Price here',cmp:'Comparison',asc:'↑ Ascending',desc:'↓ Descending',
    hits:n=>`${n} ${n===1?'result':'results'}`,hitsLoc:(n,l)=>`${n} offers at ${l} ${l===1?'location':'locations'}`,offers:n=>`${n} ${n===1?'ship':'ships'}`,from:'from',cheapest:'cheapest',only:'only here',also:'Also:',
    save:'Save',saved:'Saved ✓',none:'No ships match these filters.',wishEmpty:'Nothing saved yet. Click “Save” on a ship in the list. You will then see the total, your budget and your buying stops here.',
    remove:'Remove',total:'Total',stops:'Buying stops',budget:'Budget',rest:'Left over',missing:'Short by',oneStop:(l,d)=>`Everything is also sold at ${l}${d>0?`, ${money(d)} more than the cheapest split`:''}.`,useOne:'Buy everything there',cheapAll:'Set all to cheapest location',clear:'Clear list',clearAsk:'Really clear the wishlist?',
    search:'Ship or manufacturer',budgetPh:'e.g. 5m or 2,500,000',stat:d=>`${d.ships.length} vehicles · ${d.locs.length} locations · game version ${d.patch} · prices reported ${d.from} to ${d.to} · built ${d.generated}`,busy:'Loading …',loaded:'Data loaded:',failed:'Loading failed. The built-in data stays active.',
    roles:{starter:'Starter',cargo:'Cargo',mining:'Mining',salvage:'Salvage',medical:'Medical',repair:'Repair',refuel:'Refuel',exploration:'Exploration',science:'Science',passenger:'Passenger',racing:'Racing',military:'Military',stealth:'Stealth',bomber:'Bomber',interdiction:'Interdiction',construction:'Construction'}}
};
let LANG = load(LS.lang)==='en' ? 'en' : 'de';
const t = k => I18N[LANG][k];
// Format a number in the page language.
const fmt = n => Number(n).toLocaleString(LANG==='de'?'de-DE':'en-GB');
// Format a price with its currency.
const money = n => fmt(n)+' aUEC';

/* ---------- data and state ---------- */
let D, LOC, SHIP;
const DEFAULTS = {view:'ship',q:'',sys:'',loc:'',role:'',man:'',type:'',budget:'',scu:'',sort:'price',dir:1};
const saved = load(LS.state) || {};
const S = Object.assign({}, DEFAULTS, saved.filters||{});
let WISH = saved.wish || {};
const closedLocs = new Set();

// Take a data object into use and drop wishlist entries it no longer sells.
function ingest(d){
  D=d; LOC=new Map(d.locs.map(l=>[l.id,l])); SHIP=new Map(d.ships.map(s=>[s.id,s]));
  for(const id of Object.keys(WISH)){
    const s=SHIP.get(+id);
    if(!s){delete WISH[id];continue;}
    if(!s.p.some(o=>o[0]===WISH[id])) WISH[id]=s.p[0][0];
  }
}
// Persist filters and wishlist for the next visit.
const persist = () => save(LS.state,{filters:S,wish:WISH});
// Parse a budget leniently: "5m", "2,5 Mio", "750k" or "2.500.000"; null if empty or unreadable.
function parseBudget(v){
  const s=String(v).trim().toLowerCase().replace(/\s/g,'');
  if(!s) return null;
  const m=s.match(/^([\d.,]+)(k|m|mio|mil|b|mrd)?$/);
  if(!m) return null;
  const f={k:1e3,m:1e6,mio:1e6,mil:1e6,b:1e9,mrd:1e9}[m[2]];
  const n=f?parseFloat(m[1].replace(',','.'))*f:parseInt(m[1].replace(/[.,]/g,''),10);
  return Number.isFinite(n)?Math.round(n):null;
}
// Location label for lists: place plus planet if there is one.
const locLabel = l => l.body ? `${l.place} (${l.body})` : l.place;
// Crew as text; a range only if minimum and maximum differ.
const crewText = c => !c ? '–' : (c[0]===c[1] ? String(c[0]) : `${c[0]}–${c[1]}`);
// Does a location pass the system and location filters?
const locPass = id => {const l=LOC.get(id); return (!S.sys||l.sys===S.sys)&&(!S.loc||l.id===+S.loc);};
// Do the ship's own attributes pass the filters (everything except place and budget)?
function shipPass(s){
  const q=S.q.trim().toLowerCase();
  if(q&&!(s.n+' '+s.m).toLowerCase().includes(q)) return false;
  if(S.role&&!s.r.includes(S.role)) return false;
  if(S.man&&s.m!==S.man) return false;
  if(S.type==='space'&&s.g) return false;
  if(S.type==='ground'&&!s.g) return false;
  return !(S.scu&&s.scu<+S.scu);
}
// Compare two values for sorting; missing values always go last.
function cmp(a,b){
  if(a==null&&b==null) return 0; if(a==null) return 1; if(b==null) return -1;
  const r=typeof a==='string'?a.localeCompare(b,LANG):a-b;
  return r*S.dir;
}
// Value of the active sort key for one ship at one offer.
function sortValue(s,o){
  switch(S.sort){
    case 'name':return s.n; case 'man':return s.m; case 'price':return o[1];
    case 'loc':return locLabel(LOC.get(o[0])); case 'scu':return s.scu;
    case 'crew':return s.crew?s.crew[1]:null; default:return s.len;
  }
}
// Sort [ship, offer] pairs by the active key, then by name.
const sortPairs = pairs => pairs.sort((x,y)=>cmp(sortValue(x[0],x[1]),sortValue(y[0],y[1]))||x[0].n.localeCompare(y[0].n,LANG));

/* ---------- list views ---------- */
// The save button; in the location view it pins the ship to that location.
function wishBtn(s,tid){
  const on=(s.id in WISH)&&(tid==null||WISH[s.id]===tid);
  return `<button class="wbtn" type="button" aria-pressed="${on}" data-wish="${s.id}" data-tid="${tid==null?'':tid}">${t(on?'saved':'save')}</button>`;
}
// Sortable table header cell.
function th(key,label,cls){
  const on=S.sort===key, aria=on?` aria-sort="${S.dir>0?'ascending':'descending'}"`:'';
  return `<th class="${cls||''}"${aria}><button type="button" data-sort="${key}">${esc(label)}${on?(S.dir>0?' ▲':' ▼'):''}</button></th>`;
}
// Name cell shared by both views.
const nameCell = s => `<td><div class="name">${esc(s.n)}</div><div class="sub">${esc([s.m,...s.r.map(r=>t('roles')[r])].filter(Boolean).join(' · '))}</div></td>`;
// Attribute cells shared by both views.
const attrCells = s => `<td class="num">${fmt(s.scu)}</td><td class="num hide-s">${crewText(s.crew)}</td><td class="num hide-s">${s.len?fmt(s.len):'–'}</td>`;

// Render the view that lists each ship once with its best offer inside the filters.
function renderShips(){
  const budget=parseBudget(S.budget), pairs=[];
  for(const s of D.ships){
    if(!shipPass(s)) continue;
    const o=s.p.find(x=>locPass(x[0]));
    if(o&&(budget==null||o[1]<=budget)) pairs.push([s,o]);
  }
  sortPairs(pairs);
  $('#count').textContent=t('hits')(pairs.length);
  if(!pairs.length) return emptyHtml();
  const rows=pairs.map(([s,o])=>{
    const isBest=o[1]===s.p[0][1];
    const others=s.p.filter(x=>x[0]!==o[0]).map(x=>`${esc(LOC.get(x[0]).place)} ${fmt(x[1])}`).join(' · ');
    const badge=s.p.length===1?`<span class="best">${t('only')}</span>`:(isBest?`<span class="best">${t('cheapest')}</span>`:'');
    return `<tr><td>${wishBtn(s,null)}</td>${nameCell(s)}${attrCells(s)}<td class="num"><span class="price">${fmt(o[1])}</span></td><td><div>${esc(locLabel(LOC.get(o[0])))} ${badge}</div><div class="sub">${esc(LOC.get(o[0]).sys)}</div>${others?`<div class="alts">${t('also')} ${others}</div>`:''}</td></tr>`;
  }).join('');
  return `<div class="tablewrap"><table><thead><tr><th></th>${th('name',t('ship'))}${th('scu',t('scu'),'num')}${th('crew',t('crew'),'num hide-s')}${th('len',t('len'),'num hide-s')}${th('price',t('price')+' (aUEC)','num')}${th('loc',t('loc'))}</tr></thead><tbody>${rows}</tbody></table></div>`;
}
// Comparison cell of the location view: cheapest label or surcharge against the cheapest place.
function cmpCell(s,o){
  if(s.p.length===1) return `<span class="best">${t('only')}</span>`;
  if(o[1]===s.p[0][1]) return `<span class="best">${t('cheapest')}</span>`;
  const pct=((o[1]/s.p[0][1]-1)*100).toLocaleString(LANG==='de'?'de-DE':'en-GB',{maximumFractionDigits:1});
  return `<span class="sub">+${pct} % · ${esc(LOC.get(s.p[0][0]).place)} ${fmt(s.p[0][1])}</span>`;
}
// Render the view grouped by star system and location.
function renderLocs(){
  const budget=parseBudget(S.budget), groups=new Map();
  for(const s of D.ships){
    if(!shipPass(s)) continue;
    for(const o of s.p){
      if(!locPass(o[0])||(budget!=null&&o[1]>budget)) continue;
      if(!groups.has(o[0])) groups.set(o[0],[]);
      groups.get(o[0]).push([s,o]);
    }
  }
  const total=[...groups.values()].reduce((a,g)=>a+g.length,0);
  $('#count').textContent=t('hitsLoc')(total,groups.size);
  if(!total) return emptyHtml();
  let html='',sys=null;
  for(const l of D.locs){
    const g=groups.get(l.id); if(!g) continue;
    if(l.sys!==sys){sys=l.sys;html+=`<h2 class="sysh">${esc(sys)}</h2>`;}
    sortPairs(g);
    const low=Math.min(...g.map(p=>p[1][1]));
    const rows=g.map(([s,o])=>`<tr><td>${wishBtn(s,l.id)}</td>${nameCell(s)}${attrCells(s)}<td class="num"><span class="price">${fmt(o[1])}</span></td><td>${cmpCell(s,o)}</td></tr>`).join('');
    html+=`<details class="loc" data-loc="${l.id}"${closedLocs.has(l.id)?'':' open'}><summary><b>${esc(l.place)}</b><span class="sub">${esc([l.body,l.shop].filter(Boolean).join(' · '))}</span><span class="sub">${t('offers')(g.length)} · ${t('from')} ${money(low)}</span></summary><div class="tablewrap"><table><thead><tr><th></th>${th('name',t('ship'))}${th('scu',t('scu'),'num')}${th('crew',t('crew'),'num hide-s')}${th('len',t('len'),'num hide-s')}${th('price',t('here')+' (aUEC)','num')}<th>${t('cmp')}</th></tr></thead><tbody>${rows}</tbody></table></div></details>`;
  }
  return html;
}
// Empty result with a way out.
const emptyHtml = () => `<div class="empty">${t('none')}<br><button class="btn" type="button" data-reset="1">${$('#resetBtn').innerHTML}</button></div>`;

/* ---------- wishlist ---------- */
// Locations that sell every saved ship, cheapest total first.
function commonLocs(ids){
  return D.locs.map(l=>{
    let sum=0;
    for(const id of ids){const o=SHIP.get(+id).p.find(x=>x[0]===l.id); if(!o) return null; sum+=o[1];}
    return {l,sum};
  }).filter(Boolean).sort((a,b)=>a.sum-b.sum);
}
// Price of a saved ship at its chosen location.
const wishPrice = id => SHIP.get(+id).p.find(x=>x[0]===WISH[id])[1];
// One saved ship with its location choice.
function wishItem(id){
  const s=SHIP.get(+id);
  const opts=s.p.map(o=>`<option value="${o[0]}"${o[0]===WISH[id]?' selected':''}>${esc(LOC.get(o[0]).place)} – ${fmt(o[1])}</option>`).join('');
  return `<div class="witem"><div class="top"><span class="name">${esc(s.n)}</span><span class="price">${fmt(wishPrice(id))}</span></div><div class="row"><select data-wloc="${id}" aria-label="${t('loc')}">${opts}</select><button class="wbtn" type="button" data-remove="${id}">${t('remove')}</button></div></div>`;
}
// Render the wishlist: stops, total, budget and the one-stop hint.
function renderWish(){
  const ids=Object.keys(WISH);
  if(panels) panels.count('wish',ids.length);
  if(!ids.length){$('#wish').innerHTML=`<p class="sub">${t('wishEmpty')}</p>`;return;}
  const stops=new Map();
  ids.forEach(id=>{const k=WISH[id]; if(!stops.has(k)) stops.set(k,[]); stops.get(k).push(id);});
  const total=ids.reduce((a,id)=>a+wishPrice(id),0);
  const cheapest=ids.reduce((a,id)=>a+SHIP.get(+id).p[0][1],0);
  let html='';
  for(const l of D.locs){
    const g=stops.get(l.id); if(!g) continue;
    g.sort((a,b)=>SHIP.get(+a).n.localeCompare(SHIP.get(+b).n,LANG));
    html+=`<div class="stop"><h3><span>${esc(locLabel(l))}</span><span>${fmt(g.reduce((a,id)=>a+wishPrice(id),0))}</span></h3>${g.map(wishItem).join('')}</div>`;
  }
  const budget=parseBudget(S.budget);
  html+=`<div class="sum"><span>${t('stops')}</span><span class="v">${stops.size}</span><span>${t('total')}</span><span class="v">${money(total)}</span>`;
  if(budget!=null){
    const rest=budget-total;
    html+=`<span>${t('budget')}</span><span class="v">${money(budget)}</span><span>${t(rest<0?'missing':'rest')}</span><span class="v ${rest<0?'over':'okv'}">${money(Math.abs(rest))}</span>`;
  }
  html+='</div>';
  const common=stops.size>1?commonLocs(ids)[0]:null;
  if(common) html+=`<div class="hint">${esc(t('oneStop')(locLabel(common.l),common.sum-cheapest))}<button class="btn" type="button" data-onestop="${common.l.id}">${t('useOne')}</button></div>`;
  if(total>cheapest) html+=`<div class="hint"><button class="btn" type="button" data-cheapall="1">${t('cheapAll')}</button></div>`;
  html+=`<div class="sidefoot"><button class="btn danger" type="button" data-clear="1">${t('clear')}</button></div>`;
  $('#wish').innerHTML=html;
}

/* ---------- filter controls ---------- */
// Fill one select and keep its value if it still exists.
function fill(id,opts,key){
  const el=$(id);
  el.innerHTML=opts.map(([v,l])=>`<option value="${esc(v)}">${esc(l)}</option>`).join('');
  if(!opts.some(o=>String(o[0])===String(S[key]))) S[key]=opts[0][0];
  el.value=S[key];
}
// Build all select options from the data and the current language.
function buildControls(){
  const systems=[...new Set(D.locs.map(l=>l.sys))];
  fill('#sys',[['',t('allSys')],...systems.map(s=>[s,s])],'sys');
  fill('#loc',[['',t('allLoc')],...D.locs.filter(l=>!S.sys||l.sys===S.sys).map(l=>[l.id,`${l.place} · ${l.shop}`])],'loc');
  const roles=[...new Set(D.ships.flatMap(s=>s.r))].map(r=>[r,t('roles')[r]]).sort((a,b)=>a[1].localeCompare(b[1],LANG));
  fill('#role',[['',t('allRole')],...roles],'role');
  const mans=[...new Set(D.ships.map(s=>s.m).filter(Boolean))].sort((a,b)=>a.localeCompare(b,LANG));
  fill('#man',[['',t('allMan')],...mans.map(m=>[m,m])],'man');
  fill('#type',[['',t('allType')],['space',t('space')],['ground',t('ground')]],'type');
  fill('#sort',['price','name','man','loc','scu','crew','len'].map(k=>[k,t(k)]),'sort');
  $('#q').value=S.q; $('#budget').value=S.budget; $('#scu').value=S.scu;
  $('#q').placeholder=t('search'); $('#budget').placeholder=t('budgetPh');
}
// Redraw list, wishlist and the small status texts.
function render(){
  document.querySelectorAll('.tab').forEach(b=>b.setAttribute('aria-selected',b.dataset.view===S.view?'true':'false'));
  $('#dirBtn').textContent=t(S.dir>0?'asc':'desc');
  $('#content').innerHTML=S.view==='ship'?renderShips():renderLocs();
  renderWish();
  $('#buildStat').textContent=t('stat')(D);
  persist();
}
// Show a short status message.
function toast(msg){const el=$('#toast');el.textContent=msg;el.hidden=false;clearTimeout(toast.h);toast.h=setTimeout(()=>{el.hidden=true;},4000);}
// Reset all filters but keep view and sort order.
function resetFilters(){Object.assign(S,{q:'',sys:'',loc:'',role:'',man:'',type:'',budget:'',scu:''});buildControls();render();}
// Toggle a saved ship; a location button pins that location, a list button uses the best offer in the filters.
function toggleWish(id,tid){
  const s=SHIP.get(id);
  if(tid==null){
    if(id in WISH) delete WISH[id]; else WISH[id]=(s.p.find(o=>locPass(o[0]))||s.p[0])[0];
  } else if(WISH[id]===tid) delete WISH[id]; else WISH[id]=tid;
}

/* ---------- events ---------- */
['q','budget','scu'].forEach(k=>$('#'+k).addEventListener('input',e=>{S[k]=e.target.value;render();}));
['role','man','type'].forEach(k=>$('#'+k).addEventListener('change',e=>{S[k]=e.target.value;render();}));
$('#sys').addEventListener('change',e=>{S.sys=e.target.value;S.loc='';buildControls();render();});
$('#loc').addEventListener('change',e=>{S.loc=e.target.value;render();});
$('#sort').addEventListener('change',e=>{S.sort=e.target.value;S.dir=1;render();});
$('#dirBtn').addEventListener('click',()=>{S.dir=-S.dir;render();});
$('#resetBtn').addEventListener('click',resetFilters);
document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>{S.view=b.dataset.view;render();}));
$('#content').addEventListener('click',e=>{
  const so=e.target.closest('[data-sort]');
  if(so){const k=so.dataset.sort; if(S.sort===k) S.dir=-S.dir; else {S.sort=k;S.dir=1;} $('#sort').value=S.sort; render(); $(`#content [data-sort="${k}"]`).focus(); return;}
  if(e.target.closest('[data-reset]')){resetFilters();return;}
  const w=e.target.closest('[data-wish]');
  if(w){
    const sel=`[data-wish="${w.dataset.wish}"][data-tid="${w.dataset.tid}"]`;
    toggleWish(+w.dataset.wish,w.dataset.tid===''?null:+w.dataset.tid); render();
    const again=$('#content '+sel); if(again) again.focus();
  }
});
// Remember collapsed locations; toggle events do not bubble, so capture them.
$('#content').addEventListener('toggle',e=>{const l=e.target.dataset&&e.target.dataset.loc; if(l){if(e.target.open) closedLocs.delete(+l); else closedLocs.add(+l);}},true);
$('#wish').addEventListener('change',e=>{const id=e.target.dataset.wloc; if(id){WISH[id]=+e.target.value;render();}});
$('#wish').addEventListener('click',e=>{
  const d=e.target.closest('button'); if(!d) return;
  if(d.dataset.remove){delete WISH[d.dataset.remove];render();}
  else if(d.dataset.onestop){Object.keys(WISH).forEach(id=>{WISH[id]=+d.dataset.onestop;});render();}
  else if(d.dataset.cheapall){Object.keys(WISH).forEach(id=>{WISH[id]=SHIP.get(+id).p[0][0];});render();}
  else if(d.dataset.clear&&confirm(t('clearAsk'))){WISH={};render();}
});
$('#themeBtn').addEventListener('click',()=>{const n=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',n);save(LS.theme,n);});
$('#langBtn').addEventListener('click',e=>{const b=e.target.closest('[data-lang]');if(!b||b.dataset.lang===LANG)return;setLang(b.dataset.lang);buildControls();render();});
// Apply a language to the page.
function setLang(l){LANG=l;save(LS.lang,l);root.setAttribute('lang',l);root.setAttribute('data-lang',l);}
// Load the latest published build; failure keeps the current data.
async function refresh(){
  const btn=$('#refreshBtn'); if(btn.disabled) return;
  const old=btn.innerHTML; btn.disabled=true; btn.textContent=t('busy');
  try{
    const r=await fetch(DATA_URL,{cache:'no-store'}); if(!r.ok) throw new Error('HTTP '+r.status);
    const d=await r.json(); if(!d.ships||!d.locs) throw new Error('format');
    save(LS.raw,d); ingest(d); buildControls(); render(); toast(t('loaded')+' '+d.generated);
  }catch(e){toast(t('failed'));}
  btn.disabled=false; btn.innerHTML=old;
}
$('#refreshBtn').addEventListener('click',refresh);

/* ---------- start ---------- */
const theme=load(LS.theme); if(theme) root.setAttribute('data-theme',theme);
var panels=null;
setLang(LANG);
const cached=load(LS.raw);
ingest(cached&&cached.schema===RAW.schema&&cached.generated>RAW.generated?cached:RAW);
/*FH_JS*/
panels=scPanels($('#ptabs'),[{key:'list',label:'<span class="de">Schiffe</span><span class="en">Ships</span>',els:[$('#mainPanel')]},{key:'wish',label:'<span class="de">Merkliste</span><span class="en">Wishlist</span>',els:[$('#wishPanel')]}],'list');
buildControls();
render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
