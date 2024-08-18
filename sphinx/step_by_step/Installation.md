# まっさらな`Ubuntu環境`に`FACE01`をインストールする
```bash
wget https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/INSTALL_FACE01.sh
chmod +x INSTALL_FACE01.sh
bash -c ./INSTALL_FACE01.sh
```

## NOTE
- 動作環境は`Ubuntu 20.04`を推奨します。`Ubuntu 22.04`でも動作を確認していますが、`CUDAドライバ`まわりで手を入れる必要が発生するかもしれません。
- `Windows`ユーザの方は `WSLg`を使用するか `Docker`を使用してください。
- `Ubuntu`以外のOSをお使いの方は、`Docker`, `Boxes`, or `lxd`をご使用ください
- 使用前に`Python仮想環境`をアクティベートしてください
- `Nvidia Jetson`を使用される場合、ソースコードに手を加えて`dlib`をインストールさせる必要があります
