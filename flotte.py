# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld (identisch in StarCitizen-Handels-Planer
#                 und StarCitizen-Schiffskauf-Planer)
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       24.11.2026
# Geändert:       24.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Gemeinsame Flotte der Star-Citizen-Tools: die eigenen Schiffe des Spielers
#   mit fester ID, Modell (UEX-Fahrzeug-ID) und eigenem Namen. Das Fracht-
#   Logbuch (Handels-Planer) und der Komponenten-Reiter (Schiffskauf-Planer)
#   lesen und schreiben dieselbe Liste; jedes Tool hängt seine eigenen Daten
#   (Ladung, Bestückung) an die Schiffs-ID. Gespeichert wird im Browser unter
#   „sc_flotte_v1“. Online liegen beide Tools auf jaegerfeld.github.io und teilen
#   sich damit den Speicher; per Doppelklick geöffnete Offline-Kopien haben je
#   einen eigenen. Entfernte Schiffe bleiben als Löschmarke („del“) stehen, damit
#   das andere Tool sie nicht aus seinem alten Stand wieder anlegt. Die Datei
#   liegt byte-gleich in beiden Repos (md5 vergleichen) und ist der erste
#   Baustein für das gemeinsame Spieler-Cockpit.
# =============================================================================
"""Shared fleet store (browser localStorage) for the SC tools, inserted into each page."""

#: Version of this shared module; bump on every change and copy to both repos.
FLOTTE_VERSION = "1"

#: Shared fleet API as ``window.SCFleet``; runs before the tool scripts that use it.
FLOTTE_JS = r"""
/* ===== Shared fleet (flotte.py, identical in Handels-Planer and Schiffskauf-Planer) ===== */
window.SCFleet=(function(){
  // {v:1, ships:[{id, uex, model, name}], del:[id], saved}. uex = UEX vehicle id, model = its full name,
  // name = own name ('' = use the model name). Blocked storage: reads give an empty fleet, writes do nothing.
  const KEY='sc_flotte_v1', LEDGER='scha_ledger_v1';
  function read(){try{const o=JSON.parse(localStorage.getItem(KEY)||'null');
    if(o&&o.v===1&&Array.isArray(o.ships)) return {v:1,ships:o.ships,del:Array.isArray(o.del)?o.del:[],saved:o.saved};}catch(e){}
    return {v:1,ships:[],del:[]};}
  function write(o){o.del=o.del.slice(-300); o.saved=new Date().toISOString();
    try{localStorage.setItem(KEY,JSON.stringify(o));}catch(e){}}
  const clean=s=>({id:String(s.id),uex:s.uex,model:s.model||'',name:(s.name||'').trim()});
  // Add or update several ships at once; writes only when something changed (each write wakes the other tabs).
  function upsertMany(list){const o=read(); let ch=false;
    for(const s of list){const e=clean(s), i=o.ships.findIndex(x=>x.id===e.id);
      if(i<0){o.ships.push(e); ch=true;}
      else if(JSON.stringify(o.ships[i])!==JSON.stringify(e)){o.ships[i]=e; ch=true;}
      if(o.del.includes(e.id)){o.del=o.del.filter(d=>d!==e.id); ch=true;}}
    if(ch) write(o); return ch;}
  const upsert=s=>upsertMany([s]);
  function remove(id){const o=read(); o.ships=o.ships.filter(x=>x.id!==id); if(!o.del.includes(id)) o.del.push(id); write(o);}
  // Number of cargo posts the cargo ledger keeps aboard this ship (0 if none or no ledger in this browser).
  function cargoPosts(id){try{const l=JSON.parse(localStorage.getItem(LEDGER)||'null');
    return (l&&Array.isArray(l.stock))?l.stock.filter(p=>p&&p.l==='s:'+id&&p.n>0).length:0;}catch(e){return 0;}}
  // Call cb when another tab of the same site changed the fleet.
  function onChange(cb){window.addEventListener('storage',e=>{if(e.key===KEY) cb();});}
  return {KEY,read,upsert,upsertMany,remove,cargoPosts,onChange};
})();
"""
