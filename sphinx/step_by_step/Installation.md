# まっさらな`Ubuntu環境`に`FACE01`をインストールする

実環境を構築するためにまっさらなマシンに`FACE01`をインストールしたい場合、以下をご参考にして下さい。

<br />
<div style="display: flex; align-items: center; justify-content: flex-end;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative; margin-right: 10px;">
        <p style="margin: 10;">FACE01をまだ試していない方は<span style="background-color: yellow;">Dockerを使用</span>してください⭐️''</p>
        <div style="position: absolute; top: 50%; right: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 15px solid white; transform: translateY(-50%);"></div>
    </div>
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00129-2005948764.png" alt="説明文" width="200" style="border-radius: 50%; object-fit: cover;">
</div>
<br />

ホストOSは`Ubuntu20.04`を想定しています。

```bash
wget https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/INSTALL_FACE01.sh
chmod +x INSTALL_FACE01.sh
bash -c ./INSTALL_FACE01.sh
```
<br />
<div style="display: flex; align-items: center;">
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00103-1322935144.png" alt="説明文" width="200" style="margin-right: 10px; border-radius: 50%; object-fit: cover;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative;">
        <p style="margin: 10;">ホストOSを`Ubuntu22.04`にする場合、<span style="background-color: yellow;">追加の手順が必要</span>になります。</p>
        <p style="margin: 10;">詳しくは<a https://zenn.dev/ykesamaru/articles/53a3839afbc302>ONNX RuntimeとCUDAのバージョンが合わない時</a>をご参照ください。</p>
        <div style="position: absolute; top: 50%; left: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-right: 15px solid white; transform: translateY(-50%);"></div>
    </div>
</div>
<br />

## NOTE
- 動作環境は`Ubuntu 20.04`を推奨します。`Ubuntu 22.04`でも動作を確認していますが、`CUDAドライバ`まわりで手を入れる必要が発生するかもしれません。
- `Windows`ユーザの方は `WSLg`を使用するか `Docker`を使用してください。
- `Ubuntu`以外のOSをお使いの方は、`Docker`, `Boxes`, or `lxd`をご使用ください
- 使用前に`Python仮想環境`をアクティベートしてください
- `Nvidia Jetson`を使用される場合、ソースコードに手を加えて`dlib`をインストールさせる必要があります（バージョンによります）。
  - `dlib/cuda/cudnn_dlibapi.cpp`854行目`forward_algo = forward_best_algo;`をコメントアウトしてコンパイルして下さい。
    - 参考: [Jetson NanoでDlibをビルドして顔認識でGPUを使ってみる ](https://wisteriahill.sakura.ne.jp/CMS/WordPress/2020/12/15/jetson-nano-build-dlib-use-gpu-for-face-recognition/)
