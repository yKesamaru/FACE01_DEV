#!/usr/bin/env bash
set -x

# -----------------------------------------------------------------
# FACE01 SETUP INSTALLER
# THIS IS *ONLY* USE FOR UBUNTU *20.04*
# -----------------------------------------------------------------

# pipのアップグレード
pip install -U pip wheel setuptools

python3 -m venv ./
# shellcheck disable=SC1091
source bin/activate

# pyproject.tomlのインストール
pip install --no-cache-dir .

pip install dlib

cd ../