# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Schiffskauf-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       16.11.2026
# Geändert:       24.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Oberfläche des Reiters „Komponenten“ (HTML, CSS, JS) für die gebaute Seite:
#   eigene Draufsicht des Schiffs in der Mitte, Komponenten-Karten rundum mit
#   Linien zum Einbauort, Auswahl nur passender Teile (standardmäßig nur
#   ingame kaufbare), Unterkarten für Turmwaffen und Raketen, Einkaufsliste mit
#   günstigstem Händler und allen Händlern zum Aufklappen. Alles ist mit kp-
#   bzw. #kpPanel abgegrenzt, damit es die übrige Seite nicht berührt; das
#   Skript läuft in einer eigenen Funktion und reagiert auf die Sprache der
#   Seite. Die Auswahl-Leiste schiebt die Seite ab 1280 px zur Seite statt sie zu
#   verdecken und schließt per ×, Esc, erneutem Kartenklick oder Klick daneben.
#   Der Reiter steht neben „Nach Schiff“ und „Nach Standort“ und blendet
#   Filter, Liste und Merkliste aus. Oben stehen nur die Schiffe, die der
#   Spieler im Dialog „Meine Schiffe“ gewählt hat; Auswahl und Bestückung je
#   Schiff speichert der Browser (localStorage, Schlüssel scsk_kp). Die
#   Bestückung steckt zusätzlich im Link (#kp=<schiff>&<platz>=<teil>); ein
#   Link hat Vorrang, gespeichert wird erst, wenn der Spieler etwas ändert.
# =============================================================================
"""HTML, CSS and JS fragments of the "Komponenten" tab, inserted by the page builder."""

#: Panel markup; sits in the main panel right below the view tabs.
KP_HTML = r"""
<section id="kpPanel" aria-labelledby="kp-h">
  <div class="kp-head">
    <div>
      <h2 id="kp-h"><span class="de">Schiffskomponenten</span><span class="en">Ship components</span>
        <span class="kp-beta"><span class="de">Vorschau</span><span class="en">Preview</span></span></h2>
      <p class="kp-lede"><span class="de">Karte anklicken, Alternative wählen: Es erscheinen nur Teile, die in diesen Steckplatz passen. Die Einkaufsliste zeigt, wo du sie ingame bekommst.</span><span class="en">Click a card, pick an alternative: only parts that fit this slot are shown. The shopping list shows where to get them in game.</span></p>
    </div>
    <div class="kp-shipbar"><div class="kp-ships" id="kp-ships" role="group" aria-label="Meine Schiffe / My ships"></div>
      <button type="button" class="btn kp-minebtn" id="kp-minebtn" aria-haspopup="dialog">⚙ <span class="de">Meine Schiffe …</span><span class="en">My ships …</span></button></div>
  </div>
  <div class="kp-none" id="kp-none" hidden>
    <p><b><span class="de">Wähle zuerst deine Schiffe.</span><span class="en">Choose your ships first.</span></b><br>
    <span class="de">Sie erscheinen dann oben als Knöpfe zum Umschalten. Auswahl und Bestückung merkt sich dein Browser.</span><span class="en">They then appear at the top as buttons to switch between them. Your browser remembers the choice and the loadouts.</span></p>
    <button type="button" class="btn primary" id="kp-nonebtn"><span class="de">Schiffe wählen</span><span class="en">Choose ships</span></button>
  </div>
  <dialog class="kp-mine" id="kp-mine" aria-labelledby="kp-mineh">
    <div class="kp-mh"><h3 id="kp-mineh"><span class="de">Meine Schiffe</span><span class="en">My ships</span></h3>
      <button type="button" class="kp-x" id="kp-minex" aria-label="Schließen / Close">×</button></div>
    <p class="kp-mp"><span class="de">Hak die Schiffe an, die du planen willst. Weitere Schiffe kommen nach und nach dazu.</span><span class="en">Tick the ships you want to plan. More ships are added step by step.</span></p>
    <label class="kp-mq"><span class="de">Suchen</span><span class="en">Search</span> <input type="search" id="kp-mineq" autocomplete="off"></label>
    <div class="kp-mlist" id="kp-minelist"></div>
    <div class="kp-mf"><span id="kp-minecount" role="status"></span>
      <button type="button" class="btn primary" id="kp-mineok"><span class="de">Fertig</span><span class="en">Done</span></button></div>
  </dialog>
  <div id="kp-body">
    <div class="kp-sum" id="kp-sum"></div>
    <div class="kp-stage" id="kp-stage">
      <div class="kp-centerrow kp-toprow" id="kp-colT"></div>
      <div class="kp-col L" id="kp-colL"></div>
      <div class="kp-ship" id="kp-ship"></div>
      <div class="kp-col R" id="kp-colR"></div>
      <div class="kp-centerrow" id="kp-colC"></div>
      <svg id="kp-wires" aria-hidden="true"></svg>
    </div>
    <section class="kp-shop" aria-live="polite">
      <h3><span class="de">Einkaufsliste</span><span class="en">Shopping list</span></h3>
      <div id="kp-shoplist"></div>
      <div class="kp-acts">
        <button type="button" class="btn" id="kp-copylink"><span class="de">Link zu dieser Bestückung kopieren</span><span class="en">Copy link to this loadout</span></button>
        <button type="button" class="btn" id="kp-resetall"><span class="de">Alles auf Standard</span><span class="en">Reset all to stock</span></button>
      </div>
    </section>
    <p class="kp-foot"><span class="de">Spieldaten: Star Citizen Wiki API, Kaufpreise: UEX. Draufsicht: eigene, stilisierte Zeichnung nach eigenem Screenshot, nicht maßstäblich. * Energiebilanz vereinfacht: alle Verbraucher außer dem Quantum-Antrieb gleichzeitig an, ohne Waffen-Energiepool.</span><span class="en">Game data: Star Citizen Wiki API, prices: UEX. Top view: own stylised drawing from an own screenshot, not to scale. * Simplified power balance: all consumers except the quantum drive on at once, without the weapon power pool.</span> <span id="kp-stand"></span></p>
  </div>
  <aside class="kp-drawer" id="kp-drawer" aria-hidden="true" aria-labelledby="kp-dtitle">
    <div class="kp-dh">
      <button type="button" class="kp-x" id="kp-dx" aria-label="Schließen / Close" title="Schließen / Close (Esc)">×</button>
      <h3 id="kp-dtitle">–</h3>
      <p id="kp-dsub"></p>
      <label><input type="checkbox" id="kp-onlybuy" checked> <span class="de">Nur ingame kaufbare zeigen</span><span class="en">Only show parts buyable in game</span></label>
      <div class="kp-dbtn">
        <button type="button" class="btn" id="kp-dreset"><span class="de">Standard wiederherstellen</span><span class="en">Restore stock part</span></button>
        <button type="button" class="btn" id="kp-dclose"><span class="de">Schließen</span><span class="en">Close</span></button>
      </div>
    </div>
    <div class="kp-list" id="kp-dlist"></div>
  </aside>
</section>
"""

#: Panel styles, all scoped to #kpPanel so the ship and wishlist views stay untouched.
#: ``body.kp-on`` (set by the page's render()) hides filters, list and wishlist.
KP_CSS = r"""
  #kpPanel{display:none;min-width:0}
  body.kp-on #kpPanel{display:block}
  body.kp-on #mainPanel>:not(.tabs):not(#kpPanel),body.kp-on #wishPanel,body.kp-on #ptabs{display:none!important}
  body.kp-on .layout{grid-template-columns:minmax(0,1fr)}
  #kpPanel .kp-head{display:flex;flex-wrap:wrap;gap:10px 20px;align-items:flex-end;justify-content:space-between;margin:14px 0 4px}
  #kpPanel h2{font-family:var(--disp);font-size:24px;margin:0;display:flex;gap:10px;align-items:center}
  #kpPanel .kp-beta{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent2);border:1px dashed var(--accent2);border-radius:6px;padding:1px 8px}
  #kpPanel .kp-lede{color:var(--muted);margin:4px 0 0;max-width:72ch;font-size:14px}
  #kpPanel .kp-shipbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
  #kpPanel .kp-ships{display:flex;flex-wrap:wrap;gap:8px}
  #kpPanel .kp-ships button.link{border-style:dashed}
  #kpPanel .kp-minebtn{min-height:40px}
  #kpPanel .kp-none{background:var(--panel);border:1px dashed var(--line);border-radius:12px;padding:22px;margin:16px 0;text-align:center}
  #kpPanel .kp-none p{margin:0 0 12px;color:var(--muted)} #kpPanel .kp-none b{color:var(--ink);font-size:17px}
  #kpPanel .kp-none .btn,#kpPanel .kp-mf .btn{min-height:44px}
  #kpPanel .btn.primary{background:var(--accent);color:var(--onaccent);border-color:var(--accent);font-weight:700}
  #kpPanel .kp-linkadd{min-height:40px}
  .kp-mine{width:min(520px,94vw);max-height:86vh;padding:0;border:1px solid var(--line);border-radius:14px;background:var(--panel);color:var(--ink);box-shadow:var(--shadow)}
  .kp-mine[open]{display:flex;flex-direction:column}
  .kp-mine::backdrop{background:rgba(0,0,0,.55)}
  .kp-mh{position:relative;padding:16px 64px 4px 18px} .kp-mh h3{font-family:var(--disp);font-size:22px;margin:0}
  .kp-mp{margin:0 18px 10px;color:var(--muted);font-size:13.5px}
  .kp-mq{display:flex;gap:8px;align-items:center;margin:0 18px 8px;font-size:14px}
  .kp-mq input{flex:1;min-height:40px;padding:0 10px;border:1px solid var(--line);border-radius:8px;background:var(--panel2);color:var(--ink);font:inherit}
  .kp-mlist{overflow:auto;padding:0 18px 8px}
  .kp-mlist h4{font-family:var(--disp);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:12px 0 4px}
  .kp-mlist label{display:flex;gap:10px;align-items:center;min-height:44px;padding:0 8px;border-radius:8px;cursor:pointer}
  .kp-mlist label:hover{background:var(--panel2)}
  .kp-mlist input{width:20px;height:20px;accent-color:var(--accent);flex:none}
  .kp-mlist small{color:var(--muted)}
  .kp-mf{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 18px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
  #kpPanel .kp-ships button{min-height:40px;padding:0 14px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);font:600 14px var(--body);cursor:pointer}
  #kpPanel .kp-ships button[aria-pressed="true"]{border-color:var(--accent);color:var(--accent)}
  #kpPanel .kp-sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:12px 0 18px}
  #kpPanel .kp-sum>div{background:var(--panel);padding:10px 14px}
  #kpPanel .kp-sum .k{font-family:var(--disp);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
  #kpPanel .kp-sum .v{font-family:var(--disp);font-size:24px;font-weight:700}
  #kpPanel .kp-d{font-size:13px;font-weight:700;margin-left:6px}
  #kpPanel .kp-d.up{color:var(--ok)} #kpPanel .kp-d.down{color:var(--bad)}
  #kpPanel .kp-stage{position:relative;display:grid;grid-template-columns:minmax(230px,1fr) minmax(320px,430px) minmax(230px,1fr);gap:26px;align-items:center}
  #kpPanel .kp-col{display:flex;flex-direction:column;gap:12px}
  #kpPanel .kp-ship svg{width:100%;height:auto;display:block}
  #kpPanel .kp-toprow{margin:0 0 -6px}
  #kpPanel .kp-centerrow{grid-column:1/-1;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,300px));justify-content:center;gap:12px;margin-top:4px}
  #kp-wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
  #kp-wires path{fill:none;stroke:var(--accent);stroke-width:1.4;opacity:.55}
  #kp-wires path.on{opacity:1;stroke-width:2.2}
  #kp-wires circle{fill:var(--accent)}
  #kp-wires path.low{stroke-dasharray:6 4}
  #kp-wires circle.low{fill:var(--bg);stroke:var(--accent);stroke-width:1.6}
  #kpPanel .kp-card{position:relative;text-align:left;width:100%;min-height:72px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 12px 10px 14px;color:var(--ink);font:inherit;cursor:pointer;box-shadow:var(--shadow)}
  #kpPanel .kp-card:hover,#kpPanel .kp-card:focus-visible,#kpPanel .kp-card.sel{border-color:var(--accent)}
  #kpPanel .kp-card .t{font-family:var(--disp);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);display:flex;gap:8px;align-items:center;flex-wrap:wrap}
  #kpPanel .kp-card .n{font-family:var(--disp);font-size:19px;font-weight:700;line-height:1.15;margin:2px 0}
  #kpPanel .kp-card .m{font-size:13px;color:var(--muted)}
  #kpPanel .kp-sz{font-family:var(--disp);font-weight:700;font-size:12px;border:1px solid var(--line);border-radius:5px;padding:0 6px;color:var(--ink)}
  #kpPanel .kp-ps{font-size:11.5px;letter-spacing:.06em;color:var(--muted);border:1px solid var(--line);border-radius:5px;padding:0 6px}
  #kpPanel .kp-ps.low{border-style:dashed}
  #kpPanel .kp-sd{display:none;font-size:11.5px;letter-spacing:.06em;color:var(--muted)}
  #kpPanel .kp-chg{display:none;font-family:var(--disp);font-size:11.5px;font-weight:700;letter-spacing:.06em;color:var(--onaccent);background:var(--accent2);border-radius:5px;padding:1px 7px;margin-left:auto}
  #kpPanel .kp-card.changed .kp-chg{display:inline-block}
  #kpPanel .kp-card.changed{border-left:4px solid var(--accent2)}
  #kpPanel .kp-card.sub{min-height:56px;width:calc(100% - 22px);margin-left:22px;background:var(--panel2);box-shadow:none;padding-top:7px;padding-bottom:7px}
  #kpPanel .kp-card.sub::before{content:"";position:absolute;left:-14px;top:-13px;bottom:50%;width:12px;border-left:1.5px solid var(--line);border-bottom:1.5px solid var(--line);border-bottom-left-radius:6px}
  #kpPanel .kp-card.sub .n{font-size:16px}
  #kpPanel .kp-col.R .kp-card.sub{margin-left:0;margin-right:22px}
  #kpPanel .kp-col.R .kp-card.sub::before{left:auto;right:-14px;border-left:none;border-right:1.5px solid var(--line);border-bottom-left-radius:0;border-bottom-right-radius:6px}
  #kpPanel .kp-shop{margin:24px 0 10px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
  #kpPanel .kp-shop h3{font-family:var(--disp);font-size:22px;margin:0 0 6px}
  #kpPanel .kp-shop td.p{text-align:right;font-family:var(--disp);font-weight:700;font-size:16px;white-space:nowrap}
  #kpPanel .kp-shop .tot td{border-bottom:0;font-weight:700}
  #kpPanel .kp-shop .note{color:var(--muted);font-size:12px}
  #kpPanel .kp-acts{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
  #kpPanel .kp-acts .btn{min-height:44px}
  #kpPanel .kp-sys{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);border-radius:5px;padding:0 5px;margin-left:4px;white-space:nowrap}
  #kpPanel details.kp-more{margin-top:4px;font-size:13px}
  #kpPanel details.kp-more>summary{cursor:pointer;color:var(--accent);min-height:28px;display:inline-flex;align-items:center;list-style:none}
  #kpPanel details.kp-more>summary::-webkit-details-marker{display:none}
  #kpPanel details.kp-more>summary::before{content:"▸";margin-right:6px}
  #kpPanel details.kp-more[open]>summary::before{content:"▾"}
  #kpPanel details.kp-more ol{margin:4px 0 2px;padding-left:20px}
  #kpPanel details.kp-more li{margin:3px 0}
  #kpPanel .kp-dt{color:var(--muted);font-size:12px;white-space:nowrap}
  #kpPanel .kp-foot{color:var(--muted);font-size:12.5px;margin:10px 0 0}
  #kpPanel .kp-empty{color:var(--muted);padding:18px 6px}
  .kp-drawer{visibility:hidden;position:fixed;top:0;right:0;height:100%;width:min(420px,100%);background:var(--panel);border-left:1px solid var(--line);box-shadow:var(--shadow);transform:translateX(105%);transition:transform .18s;z-index:40;display:flex;flex-direction:column}
  .kp-drawer.open{transform:none;visibility:visible}
  .kp-dh{position:relative;padding:16px 64px 10px 18px;border-bottom:1px solid var(--line)}
  .kp-x{position:absolute;top:10px;right:10px;width:44px;height:44px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);color:var(--ink);font:400 28px/1 var(--body);cursor:pointer}
  .kp-x:hover,.kp-x:focus-visible{border-color:var(--accent);color:var(--accent)}
  /* Wide screens: the open drawer makes room instead of covering the right card column. */
  @media (min-width:1280px){body.kp-on.kp-open{padding-right:420px} body.kp-on.kp-open .kp-drawer{box-shadow:none}}
  .kp-dh h3{font-family:var(--disp);font-size:22px;margin:0}
  .kp-dh p{margin:2px 0 8px;color:var(--muted);font-size:13.5px}
  .kp-dh label{display:flex;gap:8px;align-items:center;font-size:14px;min-height:32px;cursor:pointer}
  .kp-dh input{width:20px;height:20px;accent-color:var(--accent)}
  .kp-dbtn{display:flex;gap:8px;margin-top:6px;flex-wrap:wrap}
  .kp-dbtn .btn{min-height:40px}
  .kp-list{overflow:auto;padding:8px 12px 24px;display:flex;flex-direction:column;gap:6px}
  .kp-opt{flex:none;display:grid;grid-template-columns:1fr auto;gap:2px 12px;text-align:left;min-height:56px;width:100%;background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:9px 12px;color:var(--ink);font:inherit;cursor:pointer}
  .kp-opt:hover,.kp-opt:focus-visible{border-color:var(--accent)}
  .kp-opt.cur{border:2px solid var(--accent)}
  .kp-opt .on{font-family:var(--disp);font-weight:700;font-size:16.5px}
  .kp-opt .os{font-size:13px;color:var(--muted);grid-column:1}
  .kp-opt .os.st{grid-column:1/-1}
  .kp-opt .op{grid-column:2;grid-row:1/3;text-align:right;font-size:13px;color:var(--muted);align-self:center;max-width:170px}
  .kp-opt .op b{display:block;color:var(--ink);font-family:var(--disp);font-size:16px}
  .kp-opt .kp-d{font-size:13px;font-weight:700;margin-left:4px}
  .kp-opt .kp-d.up{color:var(--ok)} .kp-opt .kp-d.down{color:var(--bad)}
  .kp-tag{font-family:var(--disp);font-size:11px;font-weight:700;letter-spacing:.05em;border-radius:5px;padding:0 6px;border:1px solid var(--line);margin-left:6px;color:var(--muted)}
  .kp-tag.on{color:var(--accent);border-color:var(--accent)}
  .kp-list .kp-empty{color:var(--muted);padding:18px 6px}
  @media (max-width:919px){
    #kpPanel .kp-stage{grid-template-columns:minmax(0,1fr)}
    #kpPanel .kp-ship{order:-1;max-width:420px;width:100%;margin:0 auto}
    #kp-wires{display:none}
    #kpPanel .kp-sd{display:inline}
  }
"""

#: Panel behaviour. Runs at the end of the page script; a #kp= link opens the tab.
KP_JS = r"""
/* ---------- components tab ---------- */
(function(){
const KP=/*__KP__*/null;
const box=document.getElementById('kpPanel'); if(!box) return;
const $k=id=>document.getElementById('kp-'+id);
const L=()=>(document.documentElement.getAttribute('lang')||'de').slice(0,2);
const T=(de,en)=>L()==='en'?en:de;
if(!KP){$k('body').innerHTML=`<p class="kp-empty">${T('Die Komponentendaten waren beim letzten Bau nicht erreichbar. Der nächste Bau holt sie neu.','The component data was unavailable at the last build. The next build fetches it again.')}</p>`; return;}

const CLS={Military:['Militär','Military'],Civilian:['Zivil','Civilian'],Industrial:['Industrie','Industrial'],Competition:['Wettkampf','Competition'],Stealth:['Stealth','Stealth']};
const STAT={cool:['Kühlung','Cooling',''],power:['Energie','Power',''],hp:['Schild-HP','Shield HP',''],regen:['Regeneration','Regen','/s'],
  qspeed:['Quantum','Quantum',' Mm/s'],spool:['Anlauf','Spool',' s'],dps:['Schaden','Damage','/s'],alpha:['Alpha','Alpha',''],range:['Reichweite','Range',' m'],missiles:['Raketen','Missiles',''],
  pwr:['Strombedarf','Power draw',''],mdmg:['Schaden je Rakete','Damage per missile',''],seek:['Zielsuche','Seeker',''],mspeed:['Tempo','Speed',' m/s'],
  guns:['Waffenplätze','Weapon mounts',''],ir:['IR-Signatur','IR signature',''],em:['EM-Signatur','EM signature',''],dur:['Haltbarkeit','Durability',' HP']};
// For these values less is better (difference shown green when smaller).
const LOWER=new Set(['pwr','ir','em','spool']);
const MAIN={Cooler:'cool',PowerPlant:'power',Shield:'hp',QuantumDrive:'qspeed',WeaponGun:'dps',MissileLauncher:'missiles',Radar:'pwr',Turret:'guns',Mount:'guns',Missile:'mdmg'};
const POS={oben:['oben','top'],unten:['unten','bottom'],nase:['Nase','nose']};
const byKey={}; for(const k in KP.catalog) for(const it of KP.catalog[k]) byKey[it.uuid]=it;
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt=n=>n==null?'–':(typeof n==='number'?n.toLocaleString(L()==='en'?'en-US':'de-DE'):esc(n));
const STATE={};
let ship=KP.ships[0], state={}, BASE=[], SL=[], ANC={}, open=null;

/* ---------- my ships and saved loadouts (browser only) ---------- */
// {mine:[slug], fit:{slug:{slotId:uuid}}, last:slug}; blocked storage simply means nothing is kept.
const KEY='scsk_kp'; const DB=Object.assign({mine:[],fit:{},last:null},load(KEY)||{});
DB.mine=DB.mine.filter(s=>KP.ships.some(x=>x.slug===s));
let linkShip=null;   // ship opened by a link that is not (yet) one of my ships
const persist=()=>save(KEY,DB);
const mine=()=>KP.ships.filter(x=>DB.mine.includes(x.slug));
// Keep the loadout of the current ship (only changed slots); an unchanged ship has no entry.
function keepFit(){const f={}; for(const k in state) if(state[k]) f[k]=state[k];
  if(Object.keys(f).length) DB.fit[ship.slug]=f; else delete DB.fit[ship.slug]; DB.last=ship.slug; persist();}
function loadFit(slug){return STATE[slug]||(STATE[slug]={...(DB.fit[slug]||{})});}

/* ---------- slots ---------- */
function stock(s){return s.default;}
function cur(s){return state[s.id]||stock(s);}
function item(u){return byKey[u];}
function cls(it){return it?.cls?T(...(CLS[it.cls]||[it.cls,it.cls])):'';}
// Place every slot of the ship: exact port position, else generic per type and side; row = card column.
function setup(){
  BASE=ship.slots.map(s=>({...s})); ANC={}; const idx={};
  for(const s of BASE){const pa=ship.panch[s.port]; let a=pa?pa.xy:ship.anch[s.type]?.[s.side];
    if(pa){s.low=!!pa.low; s.pos=pa.pos||'';}
    else if(s.side==='C'||!a){const arr=ship.anch[s.type]?.C||[[200,300]]; const i=idx[s.type]=(idx[s.type]??-1)+1; a=arr[Math.min(i,arr.length-1)];}
    ANC[s.id]=a; s.row=pa?.col||(s.side==='C'?(a[1]<250?'T':'C'):s.side);}
}
// Sub-mounts of a slot for the part fitted (or the stock part): weapons in turrets, missiles in racks.
function subsFor(s,u){const it=item(u); return (it?.sub||[]).map(g=>({id:s.id+'|'+g.k,parent:s,sub:true,type:g.type,size:g.size,n:g.n,
  side:s.side,pos:s.pos,low:s.low,row:s.row,default:(u===stock(s)?(s.subdef||{})[g.k]:null)??g.def??null}));}
function buildSlots(){SL=[]; for(const s of BASE){SL.push(s); SL.push(...subsFor(s,cur(s)));}}
// Place words: side plus top/bottom/nose where known.
function sideTxt(s){return [s.side==='L'?T('links','left'):s.side==='R'?T('rechts','right'):T('Mitte','centre'),s.pos?T(...POS[s.pos]):''].filter(Boolean).join(' ');}

/* ---------- link ---------- */
function readHash(){try{const p=new URLSearchParams(location.hash.slice(1)); const slug=p.get('kp'); if(!slug) return false;
  ship=KP.ships.find(x=>x.slug===slug)||KP.ships[0]; state=STATE[ship.slug]={};
  for(const [k,u] of p) if(k!=='kp'&&byKey[u]) state[k]=u; return true;}catch(e){return false;}}
function writeHash(){const p=new URLSearchParams({kp:ship.slug}); for(const s of SL) if(state[s.id]&&state[s.id]!==stock(s)) p.set(s.id,state[s.id]);
  history.replaceState(null,'','#'+p);}

/* ---------- drawing ---------- */
// Own stylised top view of the ship from the path data.
function drawShip(){const g=ship.sil; const [x,y,w,h]=g.viewBox.split(' ');
  $k('ship').innerHTML=`<svg id="kp-svg" viewBox="${g.viewBox}" role="img" aria-label="${esc(T('Draufsicht','Top view'))} ${esc(ship.name)}">
    <defs><pattern id="kp-grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25 0H0V25" fill="none" stroke="var(--line)" stroke-width=".7"/></pattern></defs>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#kp-grid)" opacity=".7" rx="16"/>
    <path d="${g.outline}" fill="var(--panel2)" stroke="var(--accent)" stroke-width="2.4" stroke-linejoin="round"/>
    <g fill="none" stroke="var(--accent)" stroke-width="1.2" opacity=".6" stroke-linejoin="round">${g.details.map(d=>`<path d="${d}"/>`).join('')}${g.circles.map(c=>`<circle cx="${c[0]}" cy="${c[1]}" r="${c[2]}"/>`).join('')}</g></svg>`;}
function cardHTML(s){
  const it=item(cur(s)); const k=MAIN[s.type]; const st=STAT[k];
  // Weapons show damage/s, alpha (one shot) and range; all other types their main value.
  const keys=s.type==='WeaponGun'?['dps','alpha','range']:[k];
  const val=it?keys.filter(x=>x&&it.stats[x]!=null).map(x=>`${T(STAT[x][0],STAT[x][1])}: <b>${fmt(it.stats[x])}${STAT[x][2]}</b>`).join(' · '):'';
  const valx=val?val+' · ':'';
  const ch=state[s.id]&&state[s.id]!==stock(s);
  return `<button class="kp-card${s.sub?' sub':''}${ch?' changed':''}" data-id="${esc(s.id)}" type="button">
    <div class="t">${s.n>1?s.n+' × ':''}${T(...KP.types[s.type])} <span class="kp-sz">S${s.size}</span>${s.pos?`<span class="kp-ps${s.low?' low':''}">${T(...POS[s.pos])}</span>`:''}<span class="kp-sd">${s.side==='L'?T('links','left'):s.side==='R'?T('rechts','right'):''}</span><span class="kp-chg">${T('geändert','changed')}</span></div>
    <div class="n">${it?esc(it.name):T('leer','empty')}</div>
    <div class="m">${valx}${it?[it.grade?`${T('Güte','Grade')} ${esc(it.grade)}`:'',cls(it)].filter(Boolean).join(' · '):''}</div></button>`;
}
// Cards per column, ordered by mount height so the lines do not cross; sub-cards follow their parent.
function render(){
  buildSlots();
  const cols={L:[],R:[],C:[],T:[]}; for(const s of BASE) cols[s.row].push(s);
  cols.L.sort((a,b)=>ANC[a.id][1]-ANC[b.id][1]||ANC[a.id][0]-ANC[b.id][0]); cols.R.sort((a,b)=>ANC[a.id][1]-ANC[b.id][1]||ANC[b.id][0]-ANC[a.id][0]);
  cols.T.sort((a,b)=>ANC[a.id][1]-ANC[b.id][1]); cols.C.sort((a,b)=>ANC[a.id][0]-ANC[b.id][0]||ANC[a.id][1]-ANC[b.id][1]);
  const h=a=>a.flatMap(s=>[s,...SL.filter(v=>v.parent===s)]).map(cardHTML).join('');
  for(const r of ['L','R','C','T']) $k('col'+r).innerHTML=h(cols[r]);
  // A second click on the selected card closes the drawer again.
  box.querySelectorAll('.kp-card').forEach(c=>c.addEventListener('click',()=>{if(open&&open.id===c.dataset.id) closeDrawer(); else openDrawer(c.dataset.id);}));
  renderShips();
  $k('stand').textContent=`· ${T('Spielstand','Game version')} ${KP.patch||'–'} · ${T('Stand','As of')} ${KP.built}`;
  renderSum(); renderShop(); requestAnimationFrame(wires); highlight();
}

/* ---------- totals and shopping list ---------- */
// The quantum drive does not run during combat and is left out of the power draw.
function total(key,useState){let t=0;
  for(const s of BASE){const u=useState?cur(s):stock(s); const list=[[s,item(u),1],...subsFor(s,u).map(v=>[v,item(useState?(state[v.id]||v.default):v.default),v.n])];
    for(const [x,it,n] of list){if(key==='pwr'&&x.type==='QuantumDrive') continue; const v=it?.stats?.[key]; if(typeof v==='number') t+=v*n;}}
  return Math.round(t);}
function renderSum(){
  const rows=[['hp',T('Schild-HP gesamt','Total shield HP')],['dps',T('Waffenschaden/s','Weapon damage/s')],['alpha',T('Alpha-Schaden gesamt','Total alpha damage')],['mdmg',T('Raketenschaden gesamt','Total missile damage')],['cool',T('Kühlung','Cooling')]];
  let h=rows.map(([k,lab])=>{const a=total(k,false),b=total(k,true),d=b-a;
    return `<div><div class="k">${lab}</div><div class="v">${fmt(b)}${d?`<span class="kp-d ${d>0?'up':'down'}">${d>0?'▲ +':'▼ '}${fmt(d)}</span>`:''}</div></div>`}).join('');
  const gen=total('power',true), use=total('pwr',true), ok=gen>=use;
  h+=`<div><div class="k">${T('Energie: erzeugt / Bedarf*','Power: output / draw*')}</div><div class="v">${fmt(gen)} / ${fmt(use)} <span class="kp-d ${ok?'up':'down'}">${ok?T('✓ reicht','✓ enough'):T('⚠ zu wenig','⚠ too little')}</span></div></div>`;
  $k('sum').innerHTML=h;
}
// Where to buy: cheapest shop with star system, all shops to expand (price per piece, date of the price report).
function shopCell(it){
  if(!it.buy) return T('nicht kaufbar (Loot/Crafting)','not buyable (loot/crafting)');
  const sys=s=>s.sys?` <span class="kp-sys">${esc(s.sys)}</span>`:'';
  const more=it.shops.length>1?`<details class="kp-more"><summary>${T(`alle ${it.shops.length} Händler`,`all ${it.shops.length} shops`)}</summary><ol>${it.shops.map(s=>
    `<li><b>${fmt(s.price)} aUEC</b> ${esc(s.shop)}${sys(s)}${s.date?` <span class="kp-dt">${T('Stand','as of')} ${new Date(s.date).toLocaleDateString(L()==='en'?'en-GB':'de-DE')}</span>`:''}</li>`).join('')}</ol></details>`:'';
  return `${esc(it.buy.shop)}${sys(it.buy)}${more}`;
}
function renderShop(){
  const ch=SL.filter(s=>state[s.id]&&state[s.id]!==stock(s)); const out=$k('shoplist');
  if(!ch.length){out.innerHTML=`<p class="note" style="margin:4px 0">${T('Noch nichts geändert. Klick auf eine Komponente, um sie zu tauschen.','Nothing changed yet. Click a component to swap it.')}</p>`;return;}
  let sum=0,missing=0;
  const rows=ch.map(s=>{const it=item(state[s.id]); const n=s.n||1; if(it.buy) sum+=it.buy.price*n; else missing++;
    return `<tr><td>${n>1?n+' × ':''}${T(...KP.types[s.type])} S${s.size}${s.sub?` <span class="note">${T('in','in')} ${esc(item(cur(s.parent))?.name||'')}</span>`:''} <span class="note">(${sideTxt(s)})</span></td><td><b>${esc(it.name)}</b></td><td>${shopCell(it)}</td>
      <td class="p">${it.buy?fmt(it.buy.price*n)+' aUEC':'–'}${it.buy&&n>1?`<br><span class="note">${n} × ${fmt(it.buy.price)}</span>`:''}</td></tr>`}).join('');
  out.innerHTML=`<div class="tablewrap"><table><thead><tr><th>${T('Steckplatz','Slot')}</th><th>${T('Neu','New')}</th><th>${T('Händler (günstigster zuerst)','Shop (cheapest first)')}</th><th class="num">${T('Preis','Price')}</th></tr></thead><tbody>${rows}
   <tr class="tot"><td colspan="3">${T('Summe','Total')}${missing?` (${missing} ${T('ohne Kaufpreis','without price')})`:''}</td><td class="p">${fmt(sum)} aUEC</td></tr></tbody></table></div>`;
}

/* ---------- lines from card to mount ---------- */
function wires(){
  const W=$k('wires'), stage=$k('stage'); const st=stage.getBoundingClientRect();
  if(!st.width||getComputedStyle(W).display==='none') return;
  W.setAttribute('viewBox',`0 0 ${st.width} ${st.height}`);
  const svg=$k('svg'); const m=svg?.getScreenCTM(); if(!m) return;
  let out='';
  for(const s of BASE){
    const card=box.querySelector(`.kp-card[data-id="${CSS.escape(s.id)}"]`); if(!card) continue;
    const p=svg.createSVGPoint(); p.x=ANC[s.id][0]; p.y=ANC[s.id][1]; const q=p.matrixTransform(m);
    const ax=q.x-st.left, ay=q.y-st.top, r=card.getBoundingClientRect(); let cx,cy;
    if(s.row==='L'){cx=r.right-st.left; cy=r.top+r.height/2-st.top;} else if(s.row==='R'){cx=r.left-st.left; cy=r.top+r.height/2-st.top;}
    else if(s.row==='T'){cx=r.left+r.width/2-st.left; cy=r.bottom-st.top;} else {cx=r.left+r.width/2-st.left; cy=r.top-st.top;}
    const mx=(cx+ax)/2, k=s.row==='T'?40:-40;
    const d=(s.row==='C'||s.row==='T')?`M${cx},${cy} C${cx},${cy+k} ${ax},${ay-k} ${ax},${ay}`:`M${cx},${cy} C${mx},${cy} ${mx},${ay} ${ax},${ay}`;
    const lw=s.low?' class="low"':'';
    out+=`<path data-id="${esc(s.id)}"${lw} d="${d}"/><circle${lw} cx="${ax}" cy="${ay}" r="${s.low?4.5:3.5}"/>`;
  }
  W.innerHTML=out;
}

/* ---------- selection drawer ---------- */
function openDrawer(id){
  open=SL.find(s=>s.id===id); if(!open) return;
  const where=item(cur(open.parent||open))?.name||'';
  $k('dtitle').textContent=`${open.n>1?open.n+' × ':''}${T(...KP.types[open.type])} S${open.size}`;
  $k('dsub').textContent=open.sub?T(`Gilt für ${open.n>1?'alle '+open.n+' Plätze':'den Platz'} in ${where}. Werte je Stück im Vergleich zum Standardteil.`,`Applies to ${open.n>1?'all '+open.n+' mounts':'the mount'} in ${where}. Values per piece compared with the stock part.`)
    :T(`Passend für diesen Steckplatz (${sideTxt(open)}). Werte im Vergleich zum Standardteil.`,`Fits this slot (${sideTxt(open)}). Values compared with the stock part.`);
  fillList(); highlight(); const d=$k('drawer'); d.classList.add('open'); d.setAttribute('aria-hidden','false'); document.body.classList.add('kp-open'); $k('dx').focus({preventScroll:true});
}
function fillList(){
  const s=open; const k=MAIN[s.type]; const only=$k('onlybuy').checked; const base=item(stock(s));
  const list=(KP.catalog[s.cat||`${s.type}_${s.size}`]||[]).filter(it=>!only||it.buy||it.uuid===cur(s));
  list.sort((a,b)=>((typeof b.stats[k]==='number'?b.stats[k]:0)-(typeof a.stats[k]==='number'?a.stats[k]:0))||((a.buy?.price||9e9)-(b.buy?.price||9e9)));
  const dl=$k('dlist');
  if(!list.length){dl.innerHTML=`<p class="kp-empty">${T('Keine ingame kaufbare Alternative bekannt. Haken oben entfernen, um auch nicht kaufbare Teile zu sehen (Loot, Crafting, Werksteile anderer Varianten).','No buyable alternative known. Untick the box above to also see parts you cannot buy (loot, crafting, stock parts of other variants).')}</p>`;return;}
  dl.innerHTML=list.map(it=>{
    const sts=Object.entries(it.stats).filter(([kk,v])=>v!=null&&STAT[kk]).map(([kk,v])=>{const b=base?.stats?.[kk]; const d=(typeof v==='number'&&typeof b==='number')?Math.round((v-b)*10)/10:0;
      const good=LOWER.has(kk)?d<0:d>0; return `${T(STAT[kk][0],STAT[kk][1])} ${fmt(v)}${STAT[kk][2]}${d?` <span class="kp-d ${good?'up':'down'}">${d>0?'+':''}${fmt(d)}</span>`:''}`}).join(' · ');
    const tags=(it.uuid===stock(s)?`<span class="kp-tag">${T('Standard','Stock')}</span>`:'')+(it.uuid===cur(s)?`<span class="kp-tag on">${T('verbaut','fitted')}</span>`:'');
    return `<button type="button" class="kp-opt${it.uuid===cur(s)?' cur':''}" data-u="${it.uuid}">
      <span class="on">${esc(it.name)}${tags}</span>
      <span class="op">${it.buy?`<b>${fmt(it.buy.price)} aUEC</b>${esc(it.buy.shop)}`:`<b>–</b>${T('nicht kaufbar','not buyable')}${it.loot?' · Loot':''}${it.craft?' · Crafting':''}`}</span>
      <span class="os">${[it.maker&&it.maker!=='Unknown'?esc(it.maker):'',it.grade?`${T('Güte','Grade')} ${esc(it.grade)}`:'',cls(it)].filter(Boolean).join(' · ')}</span>
      <span class="os st">${sts||'&nbsp;'}</span></button>`}).join('');
  dl.querySelectorAll('.kp-opt').forEach(b=>b.addEventListener('click',()=>choose(b.dataset.u)));
}
// Fit a part; a new turret or rack resets the choices for its sub-mounts.
function choose(u){if(!open.sub&&state[open.id]!==u) dropSubs(open.id); state[open.id]=u; changed();}
function dropSubs(id){for(const k in state) if(k.startsWith(id+'|')) delete state[k];}
function changed(){writeHash(); keepFit(); render(); open=open&&(SL.find(s=>s.id===open.id)||open); if(open) fillList();}
function highlight(){box.querySelectorAll('.kp-card').forEach(c=>c.classList.toggle('sel',!!open&&c.dataset.id===open.id));
  box.querySelectorAll('#kp-wires path').forEach(p=>p.classList.toggle('on',!!open&&p.dataset.id===open.id));}
function closeDrawer(){const d=$k('drawer'); d.classList.remove('open'); d.setAttribute('aria-hidden','true'); document.body.classList.remove('kp-open'); const id=open?.id; open=null; highlight();
  if(id) box.querySelector(`.kp-card[data-id="${CSS.escape(id)}"]`)?.focus({preventScroll:true});}

/* ---------- events ---------- */
$k('dclose').addEventListener('click',closeDrawer);
$k('dx').addEventListener('click',closeDrawer);
// A click outside the drawer and outside the cards closes it (cards switch the selection instead).
// The event path is taken at dispatch, so re-rendered (detached) list items still count as inside.
document.addEventListener('click',e=>{if(open&&!e.composedPath().some(n=>n.id==='kp-drawer'||n.classList?.contains('kp-card'))) closeDrawer();});
$k('onlybuy').addEventListener('change',fillList);
$k('dreset').addEventListener('click',()=>{delete state[open.id]; if(!open.sub) dropSubs(open.id); changed();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&open) closeDrawer();});
$k('resetall').addEventListener('click',()=>{for(const k in state) delete state[k]; changed();});
$k('copylink').addEventListener('click',async e=>{const b=e.currentTarget, t=b.innerHTML; writeHash();
  try{await navigator.clipboard.writeText(location.href); b.textContent=T('Link kopiert ✓','Link copied ✓');}catch(err){b.textContent=T('Kopieren nicht möglich, Adresse aus der Adresszeile nehmen','Copy failed, take the address bar URL');}
  setTimeout(()=>{b.innerHTML=t;},1800);});
$k('ships').addEventListener('click',e=>{
  if(e.target.closest('#kp-linkadd')){DB.mine.push(linkShip); linkShip=null; persist(); renderShips(); return;}
  const b=e.target.closest('button[data-slug]'); if(!b||b.dataset.slug===ship.slug) return; show(b.dataset.slug);});
// Switch to a ship with its saved (or linked) loadout.
function show(slug){if(open) closeDrawer(); ship=KP.ships.find(x=>x.slug===slug); state=loadFit(slug);
  DB.last=slug; persist(); setup(); drawShip(); render(); writeHash();}
// Buttons for my ships; a linked ship that is not one of mine is shown dashed with an "add" button.
function renderShips(){
  const list=mine(); const extra=linkShip&&!DB.mine.includes(linkShip)?KP.ships.find(x=>x.slug===linkShip):null;
  $k('ships').innerHTML=list.map(x=>`<button type="button" data-slug="${x.slug}" aria-pressed="${x.slug===ship.slug}">${esc(x.short)}</button>`).join('')
    +(extra?`<button type="button" class="link" data-slug="${extra.slug}" aria-pressed="${extra.slug===ship.slug}" title="${esc(T('aus dem Link','from the link'))}">${esc(extra.short)}</button><button type="button" class="btn kp-linkadd" id="kp-linkadd">+ ${T('zu meinen Schiffen','add to my ships')}</button>`:'');
  const none=!list.length&&!extra; $k('none').hidden=!none; $k('body').hidden=none;
}
// "My ships" dialog: grouped by manufacturer, with search; every tick is saved at once.
function renderMine(){
  const q=$k('mineq').value.trim().toLowerCase(); const groups={};
  for(const x of KP.ships) if(!q||(x.name+' '+x.short+' '+x.maker).toLowerCase().includes(q)) (groups[x.maker||'–']=groups[x.maker||'–']||[]).push(x);
  const keys=Object.keys(groups).sort((a,b)=>a.localeCompare(b));
  $k('minelist').innerHTML=keys.length?keys.map(m=>`<h4>${esc(m)}</h4>`+groups[m].sort((a,b)=>a.name.localeCompare(b.name)).map(x=>
    `<label><input type="checkbox" value="${x.slug}"${DB.mine.includes(x.slug)?' checked':''}> <span>${esc(x.name)}${x.short!==x.name?` <small>(${esc(x.short)})</small>`:''}</span></label>`).join('')).join('')
    :`<p class="kp-empty">${T('Kein Schiff gefunden.','No ship found.')}</p>`;
  const n=DB.mine.length; $k('minecount').textContent=T(`${n} von ${KP.ships.length} gewählt`,`${n} of ${KP.ships.length} chosen`);
}
function openMine(){$k('mineq').value=''; renderMine(); const d=$k('mine'); if(d.showModal) d.showModal(); else d.setAttribute('open',''); $k('mineq').focus();}
function closeMine(){const d=$k('mine'); if(d.close) d.close(); else d.removeAttribute('open');}
$k('minelist').addEventListener('change',e=>{const c=e.target; if(c.type!=='checkbox') return;
  DB.mine=c.checked?[...new Set([...DB.mine,c.value])]:DB.mine.filter(s=>s!==c.value);
  // Keep the order of the ship list, so the buttons do not jump around.
  DB.mine=KP.ships.map(x=>x.slug).filter(s=>DB.mine.includes(s)); persist(); renderMine();});
$k('mineq').addEventListener('input',renderMine);
$k('mineok').addEventListener('click',closeMine); $k('minex').addEventListener('click',closeMine);
$k('mine').addEventListener('close',afterMine);
$k('minebtn').addEventListener('click',openMine); $k('nonebtn').addEventListener('click',openMine);
// After the dialog: stay on the current ship if it is still mine (or linked), else go to the first of mine.
function afterMine(){
  if(DB.mine.includes(ship.slug)||ship.slug===linkShip){renderShips(); return;}
  const first=mine()[0]; if(first) show(first.slug); else renderShips();
}
// Follow the page language (set by the header switch).
new MutationObserver(()=>{render(); if(open) openDrawer(open.id); drawShip(); requestAnimationFrame(wires);}).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
// The panel starts hidden: redraw the lines whenever it gets a size (tab shown, window resized).
new ResizeObserver(()=>requestAnimationFrame(wires)).observe($k('stage'));

/* ---------- start ---------- */
const fromLink=readHash();
if(fromLink){if(!DB.mine.includes(ship.slug)) linkShip=ship.slug;}
else{ship=KP.ships.find(x=>x.slug===DB.last&&DB.mine.includes(x.slug))||mine()[0]||KP.ships[0]; state=loadFit(ship.slug);}
setup(); drawShip(); render();
// A loadout link opens the tab (S and the page's render() are the ship list's).
if(fromLink){S.view='kp'; window.render();}
})();
"""
