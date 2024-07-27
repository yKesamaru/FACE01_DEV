#!/usr/bin/env bash
set -x

# -----------------------------------------------------------------
# FACE01 SETUP INSTALLER
# THIS IS *ONLY* USE FOR UBUNTU *20.04*
# -----------------------------------------------------------------

python3 -m venv ./
source bin/activate

pip cache remove dlib
pip install -U pip
pip install -U wheel
pip install -U setuptools
pip install .
pip install -r requirements_dev.txt
pip install dlib

cd ../