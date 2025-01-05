#!/usr/bin/env bash
set -x

# -----------------------------------------------------------------
# FACE01 SETUP INSTALLER
# THIS IS *ONLY* USE FOR UBUNTU *20.04*
# -----------------------------------------------------------------

# pipのアップグレード
pip install -U pip wheel setuptools

# pyproject.tomlのインストール
pip install -e .

pip install dlib

cd ../