#!/usr/bin/env bash
# Script de demostración rápida (Linux/Mac). Windows: ejecutá comandos equivalentes en PowerShell.
set -e
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python db_setup_fixed.py
python scripts/migrate_usuarios.py
python main.py
