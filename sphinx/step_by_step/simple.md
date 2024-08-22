# シンプルに顔認識だけしたい場合

`Python仮想環境`をアクティベートしてから、`example/simple.py`を起動してみましょう。

```bash
# activate virtual environment
source bin/activate

# run script
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



