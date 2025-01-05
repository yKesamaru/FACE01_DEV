# `Docker image`をビルドする
もしあなたが`Docker image`を自分自身でビルドしたいならば、下記を参考にしてください。

まず`FACE01_DEV`リポジトリからクローンします。
```bash
git clone https://github.com/yKesamaru/FACE01_DEV.git
```


## `nvidia-docker2`パッケージを使って`FACE01`の`Docker image`をビルドする
```bash
cd FACE01_DEV
docker build -t <name:tag> -f docker/Dockerfile_gpu . --network host
```


## `nvidia-docker2`パッケージを**使わずに**`FACE01`の`Docker image`をビルドする
```bash
cd FACE01_DEV
docker build -t <name:tag> -f docker/Dockerfile_no_gpu . --network host
```


## あなたの`DockerHub`リポジトリへアップロードしたいとき
Reference is [here](https://docs.docker.com/docker-hub/repos/#pushing-a-docker-container-image-to-docker-hub).
日本語は[こちら](https://zenn.dev/katan/articles/1d5ff92fd809e7)です。
```bash
# Built Docker Image
docker built ...
# Run Docker Image
docker run ...
# Confirm CONTAINER-ID
docker ps
# Confirm IMAGE-ID
docker images
# Commit container
docker container commit <container-id> <hub-user>/<repo-name>[:<tag>]
# Tag the Image with the repository name
docker tag <image-id> <repo-name>
# Docker login
docker login
# Docker push
docker push <hub-user>/<repo-name>[:<tag>]
```


## ビルドされたイメージを確認する
```bash
docker images
REPOSITORY   TAG        IMAGE ID       CREATED          SIZE
face01_gpu   3.0.03_1   abd4c0896c00   48 minutes ago   21.9GB
```


**以下の内容は[Dockerを使ってFACE01を使う](https://ykesamaru.github.io/FACE01_DEV/step_by_step/docker.html#dockerface01)と内容が重複します。詳細は[Dockerを使ってFACE01を使う](https://ykesamaru.github.io/FACE01_DEV/step_by_step/docker.html#dockerface01)をご参照ください。**

## DockerでGUIが使えるようにxhostの設定をする
```bash
xhost +local:
```

## `FACE01_DEV`のコンテナを起動する
### カメラを**接続しない**場合
```bash
docker run --rm -it \
  --gpus all -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix <image id>
```
### カメラを接続する場合
```bash
docker run --rm -it \
  --gpus all -e DISPLAY=$DISPLAY \
  --device /dev/video0:/dev/video0:mwr \
  -v /tmp/.X11-unix:/tmp/.X11-unix <image id>
```

### ホストとフォルダを共有する場合
```bash
docker run -it \
    --gpus all -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /path/to/host/folder:/path/to/container/folder \
    <image id>
```

# `nvidia-smi`でチェック
```bash
# nvidia-smiによるチェック
(FACE01_DEV) docker@02926f2467b4:~/FACE01_DEV$ nvidia-smi
Thu Aug 15 11:13:25 2024
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 555.42.06              Driver Version: 555.42.06      CUDA Version: 12.5     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce GTX 1660 Ti     Off |   00000000:09:00.0  On |                  N/A |
| 41%   39C    P8             13W /  120W |     570MiB /   6144MiB |      3%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
+-----------------------------------------------------------------------------------------+

# nvcc --versionによるチェック
(FACE01_DEV) docker@02926f2467b4:~/FACE01_DEV$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Tue_Mar__8_18:18:20_PST_2022
Cuda compilation tools, release 11.6, V11.6.124
Build cuda_11.6.r11.6/compiler.31057947_0

# ファイルをチェック
(FACE01_DEV) docker@02926f2467b4:~/FACE01_DEV$ ls
Docker_INSTALL_FACE01.sh  bin         docs       include  multipleFaces  output              pyvenv.cfg
SystemCheckLock           build       example    lib      noFace         preset_face_images  requirements_dev.txt
assets                    config.ini  face01lib  lib64    npKnown.npz    pyproject.toml      share

# エグザンプルコードをチェック
(FACE01_DEV) docker@02926f2467b4:~/FACE01_DEV$ ls example/
CTKtest.py               combination_similarity.py               example_logging.py                    make_npKnown_file.py
__init__.py              data_augmentation.py                    face_coordinates.py                   output.txt
__pycache__              data_augmentation_mp.py                 faiss_combination_similarity.py       pysimplegui_bk
aligned_crop_face.py     data_structure.py                       get_encoded_data.py                   similarity.py
anti_spoof.py            detect_eye_blink.py                     get_encoded_data_JAPANESE_FACE_V1.py  simple.py
average_face.py          display_GUI_window.py                   img                                   simple_JAPANESE_FACE_V1.py
benchmark_CUI.py         display_GUI_window_JAPANESE_FACE_V1.py  jitter.py                             simple_file_browser.py
benchmark_GUI_window.py  distort_barrel.py                       lightweight_GUI.py                    点検済
combination_counter.py   draw_datas.py                           make_ID_card.py                       不明_bk
(FACE01_DEV) docker@02926f2467b4:~/FACE01_DEV$
```

## コンテナ内の`Python仮想環境`を起動する（重要）
```bash
docker@02926f2467b4:~/FACE01_DEV$ . bin/activate
(FACE01_DEV) docker@02926f2467b4:~/FACE01_DEV$
```

> ![NOTE]:
> コンテナ内の``Python仮想環境`を起動しないと、`FACE01`は動作しません

## エグザンプルコードを実行する
動作確認のためにエグザンプルコードを実行してみましょう。
```bash
(FACE01_DEV) docker@02926f2467b4:~/FACE01_DEV$ python3 example/lightweight_GUI.py
[2024-08-15 11:26:42,563] [face01lib.load_preset_image] [load_preset_image.py] [INFO] Loading npKnown.npz
```
![](assets/2024-08-15-11-28-20.png)

エグザンプルコードが正常に動作すれば、動作確認終了です。

この開発環境を使って顔認証システムの開発を行いましょう！

## CUDAライセンス
コンテナの起動にあたり、以下のメッセージが出力されます。
```bash
==========
== CUDA ==
==========

CUDA Version 11.6.1

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.

*************************
** DEPRECATION NOTICE! **
*************************
THIS IMAGE IS DEPRECATED and is scheduled for DELETION.
    https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/support-policy.md
```
CUDAを使った開発環境に向けてのメッセージです。具体的なライセンスは[こちら](https://developer.download.nvidia.com/licenses/NVIDIA_Deep_Learning_Container_License.pdf?t=eyJscyI6IndlYnNpdGUiLCJsc2QiOiJkZXZlbG9wZXIubnZpZGlhLmNvbS9jdWRhLXRvb2xraXQifQ==)にあります。

このコンテナを使って商用利用のための開発ができます。
詳細は上記PDFをご覧ください。
このような制限が邪魔である場合には、`docker/Dockerfile_gpu`のベースイメージを変更してください。