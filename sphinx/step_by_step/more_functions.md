

# 追加の関数チュートリアル
FACE01には、`face01lib/`内に多くの関数が含まれています。
このセクションでは、FACE01で使用可能な関数の使い方について(補足的に)説明します。

<br />
<div style="display: flex; align-items: center; justify-content: flex-end;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative; margin-right: 10px;">
        <p style="margin: 10;">💥 このドキュメントは公式ドキュメントを補完するものです。そのため<span style="background-color: yellow;">最新のドキュメントを反映していません。</span></p>
        <p style="margin: 10;">正しい使い方は必ず<a https://ykesamaru.github.io/FACE01_DEV/>公式ドキュメント</a>を参照するようにしてください。</p>
        <div style="position: absolute; top: 50%; right: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 15px solid white; transform: translateY(-50%);"></div>
    </div>
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00129-2005948764.png" alt="説明文" width="200" style="border-radius: 50%; object-fit: cover;">
</div>
<br />
<a https://ykesamaru.github.io/FACE01_DEV/>公式ドキュメント</a>

## 準備
### Loggerの初期化と設定
FACE01を使用するプログラムをコーディングする際には、最初に`initialize`および`logger`をコードします。
これにより、設定ファイル`config.ini`を読み込み、エラーなどをログに記録します。
```python
from face01lib.Initialize import Initialize
from face01lib.logger import Logger

# 初期化
CONFIG: Dict =  Initialize('LIGHTWEIGHT_GUI', 'info').initialize()
# Loggerの設定
logger = Logger(CONFIG['log_level']).logger(__file__, CONFIG['RootDir'])
```

## `Dlib_api`クラス
このクラスは、ageitgeyによる[face_recognition](https://github.com/ageitgey/face_recognition)を元に修正されており、モデルデータはdaviskingによる[dlib](https://github.com/davisking/dlib)から取得しています。68点のフェイスモデルだけでなく、5点のフェイスモデルも使用します。
例については`Core.return_face_location_list`を参照してください。
```python
from face01lib.api import Dlib_api
Dlib_api_obj = Dlib_api()
```
### face_locations
フレーム内の顔のバウンディングボックスの配列を返します。
```python
face_list = Dlib_api_obj.face_locations(img, number_of_times_to_upsample, model)
```
#### 例
```python
for i in range(exec_times):
    next_frame = next_frame_gen_obj.__next__()
    if model == 'cnn':
        print( [Dlib_api_obj._trim_css_to_bounds(Dlib_api_obj._rect_to_css(face.rect), next_frame.shape) for face in Dlib_api_obj._raw_face_locations(next_frame, number_of_times_to_upsample, model)])
    else:
        print( [Dlib_api_obj._trim_css_to_bounds(Dlib_api_obj._rect_to_css(face), next_frame.shape) for face in Dlib_api_obj._raw_face_locations(next_frame, number_of_times_to_upsample, model)])
```
#### 結果
```bash
...
[(145, 177, 259, 63), (108, 521, 272, 357)]
[(134, 177, 248, 63), (92, 521, 256, 357)]
[(125, 199, 261, 62), (108, 521, 272, 357)]
[(125, 199, 261, 62), (92, 521, 256, 357)]
[(125, 199, 261, 62), (92, 521, 256, 357)]
[(138, 185, 275, 49), (92, 521, 256, 357)]
```

## `Core`クラス
Coreクラスをインポートします。
```python
from face01lib.Core import Core
```
### return_face_location_list
顔の位置リストを返します。この関数は、`api.face_locations`よりも高速です。
```python
frame_datas_array = core.frame_pre_processing(logger, CONFIG,resized_frame)

for frame_datas in frame_datas_array:
    print(f"face coordinates: {frame_datas['face_location_list']}\n")
```
#### 結果
```bash
[2023-01-23 09:28:02,587] [face01lib.load_preset_image] [load_preset_image.py] [INFO] Loading npKnown.npz
face coordinates: [(161, 443, 311, 294)]

face coordinates: [(162, 438, 286, 314)]
```
完全な例のコードは[こちら](../../example/face_coordinates.py)にあります。

### `load_preset_image`
この関数は`preset_face_images`フォルダ内の顔画像を読み込み、npKnown.npzファイルを作成します。

## `return_anti_spoof`（実験的）
このメソッドは、`spoof_or_real`、`score`、および`ELE`のデータを返します。

一般に、トレーニングされたモデルから推測される結果は、1と0に明確に分かれるわけではありません。このため、FACE01では`ELE: Equally Likely Events`という概念を取り入れています。`score`は元々0〜1の間の2つの数字を示します。このとき、2つの数字の差が`0.4`に設定され、その差が`0.4以下`の組み合わせは「同じくらい確度」であると見なされます（`=Equally Likely Events`）。FACE01ではこれを`ELE`として表現しています。つまり、2つの数字の差が`0.4未満`の場合、それが`spoof`か`not spoof`かを判断することはできません。
### 例
```python
from face01lib.Core import Core
spoof_or_real, score, ELE = Core().return_anti_spoof(frame_datas['img'], person_data["location"])
if ELE is False:
    print(
        name, "\n",
        "\t", "Anti spoof\t\t", spoof_or_real, "\n",
        "\t", "Anti spoof score\t", round(score * 100, 2), "%\n",
        "\t", "similarity\t\t", percentage_and_symbol, "\n",
        "\t", "coordinate\t\t", location, "\n",
        "\t", "time\t\t\t", date, "\n",
        "\t", "output\t\t\t", pict, "\n",
        "-------\n"
    )
```

## `VidCap`クラス
このクラスは`video_capture`に含まれています。
インポートするには、以下を参照してください。
```python
from face01lib.video_capture import VidCap
```

### `resize_frame`
リサイズされた画像のnumpy配列を返します。
```python
resized_frame = VidCap().resize_frame(set_width, set_height, original_frame)
```

### `return_movie_property`
入力された映画データのfps、高さ、幅のプロパティを返します。
```python
set_width,fps,height,width,set_height = VidCap().return_movie_property(set_width, vcap)
```
結果
```bash
...
set_width:  750
 set_height: 421
 fps:  30
```
