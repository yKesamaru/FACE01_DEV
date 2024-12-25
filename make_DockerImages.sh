#!/usr/bin/env bash

: <<'DOCSTRING'
このスクリプトは、2種類のDockerイメージ（GPU対応版と非対応版）をビルドし、
Docker Hubにプッシュするプロセスを自動化します。

- ビルド対象:
    1. face01_gpu
    2. face01_no_gpu
- 主な操作:
    - Dockerイメージのビルド
    - Docker Hubへのログイン
    - Dockerイメージのプッシュ
- 注意:
    - ビルド中にCPU使用率が高くなるため、他の作業への影響を考慮してください。
DOCSTRING

set -euo pipefail
IFS=$'\n\t'

# 定数設定
WORKDIR=~/bin/FACE01_DEV  # 作業ディレクトリ
DOCKER_REPO=tokaikaoninsho
TAG=3.04.1

# Dockerイメージをビルドしてプッシュする関数
build_and_push_image() {
    local image_name=$1   # イメージ名
    local dockerfile=$2   # 使用するDockerfile

    echo "Building Docker image: ${image_name}:${TAG}"
    docker build -t "${DOCKER_REPO}/${image_name}:${TAG}" -f "${dockerfile}" . --network host

    echo "Pushing Docker image: ${DOCKER_REPO}/${image_name}:${TAG}"
    # ログイン
    docker login
    docker push "${DOCKER_REPO}/${image_name}:${TAG}"
}

# メイン処理
main() {
    # 作業ディレクトリに移動
    cd "${WORKDIR}"

    # GPU対応版のイメージ
    build_and_push_image "face01_gpu" "docker/Dockerfile_gpu"

    # 非GPU対応版のイメージ
    build_and_push_image "face01_no_gpu" "docker/Dockerfile_no_gpu"
}

# エラー時の処理
error_handler() {
    echo "エラーが発生しました。" >&2
    exit 1
}

# 実行
trap error_handler ERR
main
