#!/usr/bin/env bash
set -Ceux -o pipefail
IFS=$'\n\t'

# License for the Code.
# 
# Copyright Owner: Yoshitsugu Kesamaru
# Please refer to the separate license file for the license of the code.


# Automation docker operation from local build to push to DockerHub.

# TODO: face01_gpuとface01_no_gpuをfor loopでまわすこと

# -----------------------------------------------------------------
# サマリー:
# このスクリプトは、DockerイメージのビルドおよびDocker Hubへのプッシュを自動化します。
# face01_gpuとface01_no_gpuの2種類のイメージを作成し、それぞれをDocker Hubにプッシュします。
# -----------------------------------------------------------------

function my_command() {

# cd: FACE01_DEV/
cd ~/bin/FACE01_DEV


# ////////////////////////////////////////

# face01_gpu

# ////////////////////////////////////////

# docker build: CPU100%になるので他の作業との兼ね合いに注意すること
docker build -t tokaikaoninsho/face01_gpu:3.0.03 -f docker/Dockerfile_gpu . --network host
# dockerを起動
# docker run --rm -it   -e DISPLAY=$DISPLAY   -v /tmp/.X11-unix/:/tmp/.X11-unix: face01_gpu:3.0.03
# # get `container-id`
# face01_gpu_container-id = docker ps -a | grep face01_gpu:3.0.03 | awk '{print $1}'
# # commit
# # docker container commit "${face01_gpu_container-id}" tokaikaoninsho/face01_gpu:3.0.03
# # get `image-id`
# face01_gpu_image-id = docker images | grep -E "tokaikaoninsho/face01_gpu\s+3.0.03.*" | awk '{print $3}'
# # add tag
# docker tag "${face01_gpu_image-id}" face01_gpu
# # login
docker login
# docker push
docker push tokaikaoninsho/face01_gpu:3.0.03


# ////////////////////////////////////////

# face01_no_gpu

# ////////////////////////////////////////

# docker build: CPU100%になるので他の作業との兼ね合いに注意すること
docker build -t tokaikaoninsho/face01_no_gpu:3.0.03 -f docker/Dockerfile_no_gpu . --network host
# # dockerを起動
# docker run --rm -it   -e DISPLAY=$DISPLAY   -v /tmp/.X11-unix/:/tmp/.X11-unix: face01_no_gpu:3.0.03
# # get `container-id`
# face01_no_gpu-container-id = docker ps -a | grep face01_no_gpu:3.0.03 | awk '{print $1}'
# # commit
# docker container commit "${face01_no_gpu_container-id}" tokaikaoninsho/face01_no_gpu:3.0.03
# # get `image-id`
# face01_no_gpu_image-id = docker images | grep -E "tokaikaoninsho/face01_no_gpu\s+3.0.03.*" | awk '{print $3}'
# # add tag
# docker tag "${face01_no_gpu_image-id}" face01_no_gpu
# login
docker login
# docker push
docker push tokaikaoninsho/face01_no_gpu:3.0.03


    return 0
}


function my_error() {
    zenity --error --text="\
    失敗しました。
    "
    exit 1
}

my_command || my_error


# ////////////////////////////////////////
# REFERENCE:

#   Docker
#       [docker push 手順](https://zenn.dev/katan/articles/1d5ff92fd809e7)
#       [grep, awkによる抽出](https://zenn.dev/sickleaf/articles/99884a12b0489cf21d45)
#   google style guide
#       [Shell Style Guide](https://github.com/google/styleguide/blob/gh-pages/shellguide.md)
#       [Googleの肩に乗ってShellコーディングしちゃおう](https://qiita.com/ma91n/items/5f72ca668f1c58176644)


# ////////////////////////////////////////
# MEMORANDUM:

# set
#   C: リダイレクトで既存のファイルを上書きしない
#   e: exit status not equal 0 -> terminate script
#   u: 初期化していない変数があるとエラー(特殊パラメーターである「@」と「*」は除く）
#   x: 実行するコマンドを出力して何をしたらどうなったかがログに残る(トレース情報として、シェルが実行したコマンドとその引数を出力する。情報の先頭にはシェル変数PS4の値を使用)
#   o: when error occurred on pipeline, terminate the script
#   -o pipefail: パイプの途中で発生したエラーがexit codeとなる。デフォルトではパイプ最後のコマンドのexit code。
#   IFS=$'\n\t': 引数の区切り文字は改行とタブのみに指定。（空白は区切り文字に含めない）