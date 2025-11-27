#!/usr/bin/env bash
# Change to where we are
cd "$(dirname "$0")"
# Activate our venv with all our deps
source .venv/bin/activate
# Let's go!
python3 calibrate.py
