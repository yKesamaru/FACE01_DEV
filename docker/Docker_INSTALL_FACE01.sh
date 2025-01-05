#!/usr/bin/env bash
# -----------------------------------------------------------------
# サマリー:
# このスクリプトは、Dockerコンテナ内でのFACE01環境のセットアップを行います。
# CUDAの環境変数設定、Python仮想環境の作成、dlibやその他の必要なパッケージのインストールを行います。
# -----------------------------------------------------------------
set -x
set -e  # エラーで停止

# pipのアップグレード
pip install -U pip wheel setuptools

# pyproject.tomlのインストール
pip install -e .

# GPU用の設定 (dlibをソースからインストール)
echo "Installing dlib from source for GPU support..."
tar -jxvf dlib-19.24.tar.bz2
cd dlib-19.24
python3 setup.py install --clean
cd ../


# ---------
# `--clean` see bellow
# [Have you done sudo python3 setup.py install --clean yet?](https://github.com/davisking/dlib/issues/1686#issuecomment-471509357)

# ベースイメージにENVとして記述があるので要らないと思われる
# cat << EOS >> ~/.bashrc
# export PATH="/usr/local/cuda/bin/:$PATH"
# export LD_LIBRARY_PATH="/usr/local/cuda/lib64/:$LD_LIBRARY_PATH"
# export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
# export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
# EOS
# 'export QT_X11_NO_MITSHM=1' >> ~/.bashrc && \
# source ~/.bashrc