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


## Check the completed image.
```bash
docker images
REPOSITORY    TAG                       IMAGE ID       CREATED         SIZE
face01_gpu    1.4.10                    41b1d82ee908   7 seconds ago   17.5GB
```


## `FACE01_DEV`のコンテナを起動する
### カメラを接続する場合
```bash
docker run --rm -it \
        --gpus all -e DISPLAY=$DISPLAY \
        --device /dev/video0:/dev/video0:mwr \
        -v /tmp/.X11-unix/:/tmp/.X11-unix: \
        <name:tag>
```
### カメラを**接続しない**場合
```bash
docker run --rm -it \
    --gpus all -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    <name:tag>
```

# `nvidia-smi`でチェック
```bash
docker@ee44d08e933f:~/FACE01_DEV$ nvidia-smi
Fri Jul 29 09:07:03 2022
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 515.48.07    Driver Version: 515.48.07    CUDA Version: 11.7     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:08:00.0  On |                  N/A |
| 41%   37C    P8    16W / 120W |    344MiB /  6144MiB |      5%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+

# Check files
docker@6ee18359bde8:~/FACE01_DEV$  ls
CALL_FACE01.py            SystemCheckLock  dlib-19.24          images   lib64        output              requirements.txt  test.mp4
Docker_INSTALL_FACE01.sh  bin              dlib-19.24.tar.bz2  include  noFace       preset_face_images  share             顔無し区間を含んだテスト動画.mp4
FACE01.py                 config.ini       face01lib           lib      npKnown.npz  pyvenv.cfg          some_people.mp4

# Launch Python virtual environment (Important!)
docker@ee44d08e933f:~/FACE01_DEV$ . bin/activate

```
