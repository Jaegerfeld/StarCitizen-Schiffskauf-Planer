#!/usr/bin/env bash
# SC Schiffskauf-Planer neu bauen (Preise live von UEX ziehen).
cd "$(dirname "$0")" || exit 1
python3 schiffskauf_planer_bauen.py && echo "Fertig. SC_Schiffskauf_Planer.html wurde aktualisiert."
