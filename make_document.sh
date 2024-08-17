#!/bin/bash

# 仮想環境を有効化
source /home/terms/bin/FACE01_DEV/bin/activate

# sphinx-apidocコマンドを実行
sphinx-apidoc -f -o sphinx/ ./
sphinx-apidoc -f -o sphinx/ sphinx/
sphinx-apidoc -f -o sphinx/ docs/
sphinx-apidoc -f -o sphinx/ example/
sphinx-apidoc -f -o sphinx/ face01lib/

# sphinx-buildコマンドを実行
sphinx-build -a -b html -E sphinx/ docs/
