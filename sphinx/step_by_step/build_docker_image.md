# Build Docker image
If you want to build the Docker Image yourself, please refer to the article below.


First, you have to clone FACE01_DEV repository.
```bash
git clone https://github.com/yKesamaru/FACE01_DEV.git
```


## Build FACE01 docker image with nvidia-docker2 package
To make image
```bash
cd FACE01_DEV
docker build -t face01_gpu:1.4.10 -f docker/Dockerfile_gpu . --network host
```


## Build FACE01 docker image * ***without*** * nvidia-docker2 package
```bash
cd FACE01_DEV
docker build -t face01_no_gpu:1.4.10 -f docker/Dockerfile_no_gpu . --network host
```


## If you want to upload to you're own DockerHub
Reference is [here](https://docs.docker.com/docker-hub/repos/#pushing-a-docker-container-image-to-docker-hub).
Japanese is [here](https://zenn.dev/katan/articles/1d5ff92fd809e7).
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
# Docker loginr
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


## Launch FACE01_DEV
```bash
docker run --rm -it \
        --gpus all -e DISPLAY=$DISPLAY \
        --device /dev/video0:/dev/video0:mwr \
        -v /tmp/.X11-unix/:/tmp/.X11-unix: face01_gpu:1.4.10

# Check nvidia-smi
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
Docker_INSTALL_FACE01.sh  bin              dlib-19.24.tar.bz2  include  noFace       priset_face_images  share             顔無し区間を含んだテスト動画.mp4
FACE01.py                 config.ini       face01lib           lib      npKnown.npz  pyvenv.cfg          some_people.mp4

# Launch Python virtual environment (Important!)
docker@ee44d08e933f:~/FACE01_DEV$ . bin/activate

```
