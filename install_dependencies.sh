#!/usr/bin/env bash
rpm-ostree install evtest
rpm-ostree install python3-devel
brew install pkg-config
brew install raylib

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
