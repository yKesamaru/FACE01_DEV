For Ubuntu, you can choose some method to install Docker, and before to install, should choice `Docker Desktop` or `Docker Engine`. Official tutorial is [here](https://docs.docker.com/engine/install/ubuntu/).
This section, we talk about install `Docker Engine` and `Docker ce`.

*If you're PC is not installed NVIDIA GPU card, refer [section]([docs/to_build_docker_image.md](Install_docker.md#if-youre-pc-is-not-installed-nvidia-gpu-card)) 'To build FACE01 docker image without nvidia-docker2 package'.*

## NOTE
You must meet the conditions listed below. See [official site](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#platform-requirements).

1. GNU/Linux x86_64 with kernel version > 3.10
2. Docker >= 19.03 (recommended, but some distributions may include older versions of Docker. The minimum supported version is 1.12)
3. NVIDIA GPU with Architecture >= Kepler (or compute capability 3.0)
4. NVIDIA Linux drivers >= 418.81.07 (Note that older driver releases or branches are unsupported.)

Please refer to the following.
```bash
# Your kernel version.
uname -r

# Your docker version.
docker --version

# Your GPU architecture
lspci | grep -ie nvidia
## List of architecture is [here](https://en.wikipedia.org/wiki/Category:Nvidia_microarchitectures) and [here](https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units) and [here](https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/).

# Your NVIDIA linux driver version.
nvidia-smi
```

## Use convenient script
You can install docker using convenient script.
```bash
sudo apt update && sudo apt upgrade -y \
  && curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker
```

## Manually install
Also, you can install docker manually.
```bash
# Uninstall old versions
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update && sudo apt upgrade -y
# Set up the repository
sudo apt install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
# Add Docker’s official GPG key:
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# Use the following command to set up the repository:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# NOTE: If you get an error about apt/sources.list, you should comment out docker's line at sources.list.
# Install Docker Engine
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
# NOTE: If you receive a GPG error when running apt update, run the following command and then try to update your repo again.
# sudo chmod a+r /etc/apt/keyrings/docker.gpg
# See bellow
# https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
If you want to confirm installed Docker, try the following command.
`sudo docker run hello-world`

## Install nvidia-docker2
To install `nvidia-docker2`, refer to [NVIDIA official tutorial](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit).
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-docker2
sudo systemctl restart docker
```
If you want to test, seel bellow.
```bash
sudo docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```
![](img/PASTE_IMAGE_2022-07-25-10-24-45.png)

## Post installation
If you don’t want to preface the docker command with sudo, create a Unix group called docker and add users to it.
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```
See [here](https://docs.docker.com/engine/install/linux-postinstall/)

## When you want to delete all at once
See [`docker image prune`](https://docs.docker.com/config/pruning/).
Japanese is [here](https://docs.docker.jp/config/pruning.html).
Also, you chose some manner as bellow.
### Stop all containers
`docker stop $(docker ps -q)`
### Delete all containers
`docker rm $(docker ps -q -a)`
### Delete all images
`docker rmi $(docker images -q)`
### Delete all except specific images
`docker images -aq | grep -v 98c2341c70ce | xargs docker rmi`

## If you're PC is not installed NVIDIA GPU card
The Dockerfile you build must be `Dockerfile_no_gpu`.
The settings in config.ini are limited to bellow.
- `headless = True`
- `use_pipe = True`

See 'To build FACE01 docker image without nvidia-docker2 package' section described [here](./docker.md)