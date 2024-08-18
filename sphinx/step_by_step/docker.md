# `Docker`を使って`FACE01`を使う
ここでは`Docker`を使って煩雑な環境構築なしに`FACE01`を使用する手順を解説します。


## `Docker image`をプル
`Dockerイメージ`をダウンロード（プル）しましょう。

![](assets/2024-08-18-12-56-10.png)

```bash
docker pull tokaikaoninsho/face01_gpu
```

> ![NOTE]:
> 使用するPCがNVIDIA GPUを使用しているなら、`face01_gpu`のような名前のついた`Docker image`を使用してください。
> そうでなければ、`face01_no_gpu`のような名前のついた`Docker image`を使用してください。

## When using `face01_gpu`
まずお使いのPCで`Nvidia GPU`が使用可能かチェックしましょう。
```bash
lspci | grep -i nvidia
```


### Docker Imageをダウンロードする
`docker pull tokaikaoninsho/face01_gpu`

### DockerイメージのTAG, IMAGE IDを確認しましょう
`docker images`

### DockerでGUIが使えるようにxhostの設定をします
`xhost +local:`
よくわからない場合は[DockerでGUIアプリケーションを開く基本的な押さえどころ](https://zenn.dev/ykesamaru/articles/add7d844f56516)を参考にしてください。

### `image id`を指定してコンテナを起動します
```bash
docker run --rm -it \
    --gpus all -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    <image id>
```

#### **NOTE**
Webカメラなどを接続して使用する場合、以下のコマンドを実行してください。
この場合`/dev/video0`を指定していますが、ご利用の環境によってはパスがちがう可能性があります。
```bash
docker run --rm -it \
  --gpus all -e DISPLAY=$DISPLAY \
  --device /dev/video0:/dev/video0:mwr \
  -v /tmp/.X11-unix/:/tmp/.X11-unix: <image id>
```
もしデバイスパスがちがう場合は以下を試してください。
```bash
ls /dev/video*
```

## **絶対に忘れてはいけないポイント**
### Python仮想環境
Python仮想環境を起動してください。
```bash
# Activate venv (IMPORTANT!)
. bin/activate
```
### `xhost`
使い終わったら`xhost`から`local`を削除しましょう
`xhost -local:`


## ここまで確認したら、簡単なエグザンプルコードを使用してみましょう
```bash
python example/simple.py
```

## トラブルシューティング
### Dockerコンテナを機動したがエグザンプルコードが動かない
- プルしたイメージが最新か確認してください
- Python仮想環境を起動したか確認してください
- `xhost`の`local`を追加したか確認してください
### エグザンプルコードは起動したが処理がおそすぎる
- Nvidia GPUを搭載したPCかどうかを確認してください
- コンテナとホストのCUDAドライバを確認してください
  - ホストのCUDAドライバのバージョンによってはコンテナ内のCUDAドライババージョンをサポートしていない場合があります。その場合はDockerの使用を諦め、まっさらなUbuntu環境に`FACE01`をインストールするか、`GUI`を使わない方法に切り替えてください。`GUI`を使わない場合、`no-gpu`のタグがついたイメージを使用し、`config.ini`ファイルの`headless`を`True`に指定してください。
- `config.ini`の`use_pipe`を`False`に設定してください。
### それでも解決しない時
- [Issue](https://github.com/yKesamaru/FACE01_DEV/issues)に投稿してください