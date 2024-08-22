# まっさらな`Ubuntu環境`に`FACE01`をインストールする

実環境を構築するためにまっさらなマシンに`FACE01`をインストールしたい場合、以下をご参考にして下さい。

ホストOSは`Ubuntu20.04`を想定しています。

```bash
wget https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/INSTALL_FACE01.sh
chmod +x INSTALL_FACE01.sh
bash -c ./INSTALL_FACE01.sh
```

> ![NOTE]
> ホストOSを`Ubuntu22.04`にする場合、追加の手順が必要になります。
> 詳しくは[ONNX RuntimeとCUDAのバージョンが合わない時](https://zenn.dev/ykesamaru/articles/53a3839afbc302)をご参照ください。

## NOTE
- 動作環境は`Ubuntu 20.04`を推奨します。`Ubuntu 22.04`でも動作を確認していますが、`CUDAドライバ`まわりで手を入れる必要が発生するかもしれません。
- `Windows`ユーザの方は `WSLg`を使用するか `Docker`を使用してください。
- `Ubuntu`以外のOSをお使いの方は、`Docker`, `Boxes`, or `lxd`をご使用ください
- 使用前に`Python仮想環境`をアクティベートしてください
- `Nvidia Jetson`を使用される場合、ソースコードに手を加えて`dlib`をインストールさせる必要があります
