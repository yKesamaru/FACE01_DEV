#!/usr/bin/env bash
set -x

# -----------------------------------------------------------------
# サマリー:
# このスクリプトは、Dockerコンテナ内でのFACE01環境のセットアップを行います。
# CUDAの環境変数設定、Python仮想環境の作成、dlibやその他の必要なパッケージのインストールを行います。
# THIS IS *ONLY* USE FOR UBUNTU *20.04*
# -----------------------------------------------------------------

# ベースイメージにENVとして記述があるので要らないと思われる
# cat << EOS >> ~/.bashrc
# export PATH="/usr/local/cuda/bin/:$PATH"
# export LD_LIBRARY_PATH="/usr/local/cuda/lib64/:$LD_LIBRARY_PATH"
# export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
# export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
# EOS
# 'export QT_X11_NO_MITSHM=1' >> ~/.bashrc && \
# source ~/.bashrc

python3 -m venv ./
source bin/activate

pip cache remove dlib
pip install -U pip
pip install -U wheel
pip install -U setuptools
pip install .
pip install -r requirements_dev.txt

tar -jxvf dlib-19.24.tar.bz2
cd dlib-19.24
# `--clean` see bellow
# [Have you done sudo python3 setup.py install --clean yet?](https://github.com/davisking/dlib/issues/1686#issuecomment-471509357)
python3 setup.py install --clean
cd ../