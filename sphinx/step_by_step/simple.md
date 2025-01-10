# シンプルに顔認識だけしたい場合
`Python仮想環境`をアクティベートしておきましょう。
```bash
source bin/activate  # . venv/bin/activateなど
```
## その①: verifyスクリプトを使う
`v3.04.02`から便利な`verify`スクリプトが使えるようになりました！⭐️

<table>
  <tr>
    <td>
      <!-- figure要素は画像とキャプションをまとめて表現する際に使う -->
      <figure>
        <img 
          src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/refs/heads/master/assets/data/c/c045.png" 
          width="150px" 
        />
        <!-- 画像の説明として figcaption を使う -->
        <figcaption>c045.png</figcaption>
      </figure>
    </td>
    <td>
      <figure>
        <img 
          src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/refs/heads/master/assets/data/c/c006.png" 
          width="150px" 
        />
        <figcaption>c006.png</figcaption>
      </figure>
    </td>
  </tr>
</table>

```bash
# プロジェクトルートで。
$ python example/verify.py assets/data/c/c045.png assets/data/c/c006.png

2枚の画像は同一人物と判定しました。cos_sim=0.318
結果: True
```
ヘルプを参照する
```bash
$ python example/verify.py -h
usage: verify [-h] [--threshold THRESHOLD] image1 image2

2枚の画像から同一人物かを判定します。

positional arguments:
  image1                1枚目の画像パス (png, jpg, jpeg)
  image2                2枚目の画像パス (png, jpg, jpeg)

options:
  -h, --help            show this help message and exit
  --threshold THRESHOLD
                        同一人物判定のコサイン類似度のしきい値 (0~1, default=0.25)
```

## その②: `example/simple.py`を触ってみる

`Python仮想環境`をアクティベートしてから、`example/simple.py`を起動してみましょう。

```bash
python example/simple.py
```

## 結果
```bash

[2022-09-27 19:20:48,174] [face01lib.load_preset_image] [simple.py] [INFO] Loading npKnown.npz
菅義偉
         similarity              99.1%
         coordinate              (138, 240, 275, 104)
         time                    2022,09,27,19,20,49,835926
         output
 -------

麻生太郎
         similarity              99.6%
         coordinate              (125, 558, 261, 422)
         time                    2022,09,27,19,20,49,835926
         output
 -------
 ...
```

クロップされた顔画像は`output`ディレクトリに保存されます。



