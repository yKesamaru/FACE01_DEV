# 顔画像の登録

この記事では、顔画像の登録方法について説明します。

<br />
<div style="display: flex; align-items: center;">
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00147-2005948782.png" alt="説明文" width="200" style="margin-right: 10px; border-radius: 50%; object-fit: cover;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative;">
        <p style="margin: 10;">用意する顔画像の<span style="background-color: yellow;">「ファイル名の決まり」は超重要</span>です！！</p>
        <p style="margin: 10;">必ず確認をしてください⭐️''</p>
        <div style="position: absolute; top: 50%; left: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-right: 15px solid white; transform: translateY(-50%);"></div>
    </div>
</div>
<br />

## 登録する顔画像ファイル名のきまり
- ファイル形式は`PNG`にしてください
- 同じ人物の顔画像を複数登録できます。その場合、少なくとも1つのファイルは`<人物名>_default.png`としてください。その他の顔画像ファイルは`<人物名>_1.png`, `<人物名>_2.png`としてください。
  - 例：
  - ![](assets/2024-08-22-18-48-10.png)
  - ウィンドウに顔画像を描画する際、`default画像`が使用されます。逆に`default画像`が存在しない場合、エラーが発生します。


## 顔画像に関する基本的な知識
パスポート写真と同様に、登録する顔画像が正確であることが重要です。

> ![](../../docs/img/passport.jpg)
> 引用元: [Russia Visa Center](https://visa.d2.r-cms.jp/)

FACE01で使用する際は、*高さ224px、幅224px*にしてください。

写真から顔の部分だけを切り取る場合、FACE01の`Utils`クラスにある`align_and_resize_maintain_aspect_ratio`メソッドを使用すると非常に簡単です。
```bash
python example/aligned_crop_face.py docs/img/Elon_Musk_Colorado_2022.jpg
```
- 元の画像
  - [U.S. Air Force photo by Trevor Cokley](https://commons.wikimedia.org/wiki/File:Elon_Musk_Colorado_2022.jpg)

  ![](../../docs/img/Elon_Musk_Colorado_2022.jpg)

- 出力された顔画像
  ![](../../docs/img/Elon_Musk_Colorado_2022.jpg_align_resize.png)

ディレクトリ名を引数として指定すると、そのディレクトリ内のすべての画像ファイルが対象となります。

## `preset_images`フォルダに顔画像を配置します。

![](../../docs/img/preset_face_images.png)

アプリケーションを起動すると、顔画像が自動的に`ndarray`データに変換されます。
このとき、使用する学習モデルについて意識してください。
`preset_face_images`ディレクトリ内の顔画像ファイルは顔学習モデルによって`npKnown.npz`ファイルへ保存されます。
`FACE01`では`dlib`と`JAPANESE FACE V1`の2種類の顔学習モデルを、`config.ini`設定ファイルで選択できます。
`dlib`モデルでは顔特徴量を`128次元配列データ`として出力するのに対し、`JAPANESE FACE V1`モデルでは`512次元配列データ`として出力します。
最終的に出力されるファイル名は`npKnown.npz`ですが、使用する学習モデルによって中身が違います。
ですので、`dlib`学習モデルを使って作成された`npKnown.npz`ファイルで`JAPANESE FACE V1`を顔認証に使おうとするとエラーが出ますし、その逆も然りです。

このとき`FACE01`は一度エラーを出力して停止しますが、もう一度起動すると`config.ini`に設定されたそれぞれの学習モデルで顔画像ファイルから特徴量データを自動的に作り直します。

<br />
<div style="display: flex; align-items: center;">
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00080-2065252.png" alt="説明文" width="200" style="margin-right: 10px; border-radius: 50%; object-fit: cover;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative;">
        <p style="margin: 10;"><span style="background-color: yellow;">config.ini設定ファイル</span>で、どちらの顔学習モデルを使用したいのか、きちんと設定することが大切です！⭐️''</p>
        <div style="position: absolute; top: 50%; left: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-right: 15px solid white; transform: translateY(-50%);"></div>
    </div>
</div>
<br />

<br />
<div style="display: flex; align-items: center; justify-content: flex-end;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative; margin-right: 10px;">
        <p style="margin: 10;">`preset_images`フォルダ内の他の顔画像ファイルを<span style="background-color: yellow;">一時的に削除したい場合</span>は、アプリケーションを起動する前にそれらを`debug`フォルダに移動してください。⭐️''</p>
        <p style="margin: 10;">このときのフォルダ名は自由ですので分かりやすい名前に変更出来ます。</p>
        <div style="position: absolute; top: 50%; right: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 15px solid white; transform: translateY(-50%);"></div>
    </div>
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00129-2005948764.png" alt="説明文" width="200" style="border-radius: 50%; object-fit: cover;">
</div>
<br />

![](../../docs/img/PASTE_IMAGE_2023-01-23-21-30-46.png)

これで完了です！
とても簡単ですね！
