#!/usr/bin/env bash
set -x

# -----------------------------------------------------------------
# FACE01 SETUP INSTALLER
# THIS IS *ONLY* USE FOR UBUNTU *20.04*
# -----------------------------------------------------------------

# pipのアップグレード
pip install -U pip wheel setuptools

python3 -m venv ./venv
# shellcheck disable=SC1091
source venv/bin/activate

# requirements_CPU.txtのインストール
pip install -r requirements_CPU.txt

cd ../