#!/usr/bin/env bash
set -x

# -----------------------------------------------------------------
# FACE01 SETUP INSTALLER
# THIS IS *ONLY* USE FOR UBUNTU *20.04*
# -----------------------------------------------------------------

# License for the Code.
# 
# Copyright Owner: Yoshitsugu Kesamaru
# Please refer to the separate license file for the license of the code.


sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential
sudo apt install -y cmake
sudo apt install -y ffmpeg
sudo apt install -y fonts-mplus
sudo apt install -y git
sudo apt install -y libavcodec-dev
sudo apt install -y libavformat-dev
sudo apt install -y libswscale-dev
sudo apt install -y libx11-dev
sudo apt install -y python3-dev
sudo apt install -y python3-tk
sudo apt install -y python3-pkg-resources
sudo apt install -y python3-venv
sudo apt install -y wget

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"

sudo apt update && sudo apt upgrade -y
sudo ubuntu-drivers autoinstall
sudo apt install -y cuda
sudo apt install -y libcublas-11-7
sudo apt install -y libcublas-dev-11-7
sudo apt install -y libcudnn8
sudo apt install -y libcudnn8-dev
sudo apt install -y liblapack-dev
sudo apt install -y libopenblas-dev
sudo apt install -y nvidia-cuda-toolkit

sudo apt autoremove -y

cat << EOS >> ~/.bashrc
export PATH="/usr/local/cuda/bin/:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/lib64/:$LD_LIBRARY_PATH"
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
EOS
source ~/.bashrc

git clone https://github.com/yKesamaru/FACE01_SAMPLE.git

cd ./FACE01_SAMPLE

python3 -m venv ./
source bin/activate

pip cache remove dlib
pip install -U pip
pip install -U wheel
pip install -U setuptools
pip install .

tar -jxvf dlib-19.24.tar.bz2
cd dlib-19.24
# `--clean` see bellow
# [Have you done sudo python3 setup.py install --clean yet?](https://github.com/davisking/dlib/issues/1686#issuecomment-471509357)
python3 setup.py install --clean
cd ../

# python CALL_FACE01.py

