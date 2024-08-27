<div align="center">

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/eye-catch.png)

✨ `FACE01`は**日本人の顔に最適化された顔学習モデルJAPANESE FACEと、<br />
Pythonで書かれたオープンソースのリファレンス実装**です。

⚡️ Apache License 2.0と商用ライセンスのデュアルライセンス！

⚡️ 日本人の顔に最適化された顔学習モデル⭐️''

⚡️ 豊富なクラスとメソッド！

⚡️ 包括的な[ドキュメント](https://ykesamaru.github.io/FACE01_DEV/index.html)付属！

FACE01 -- さあ、始めましょう！

___

![GitHub commit activity](https://img.shields.io/github/commit-activity/y/yKesamaru/FACE01_DEV)
![](https://img.shields.io/badge/Release-v3.0.03-green)
![](https://img.shields.io/badge/Python-%3E%3D3.8-blue)

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/docs/img/ROMAN_HOLIDAY.GIF?raw=true)

</div>

```bash
## result
Audrey Hepburn
         Anti spoof              real
         Anti spoof score        100.0 %
         similarity              99.1%
         coordinate              (123, 390, 334, 179)
         time                    2022,08,09,04,19,35,552949
         output                  output/Audrey Hepburn_2022,08,09,04,19,35,556237_0.39.png
 -------
 ```

---

## FACE01とは
✨ `FACE01`は**日本人の顔に最適化された顔学習モデルJAPANESE FACEと、Pythonで書かれたオープンソースのリファレンス実装**です。

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/2024-08-23_07-55.png)

- 🎉 LICENSEが「もっと使いやすく」なりました！実稼動以外はアパッチライセンスV2です！
- 🎉 `v3.0.0`よりオープンソースとして公開いたしました。（[LICENSE](https://github.com/yKesamaru/FACE01_DEV/blob/master/LICENSE/why_apache_license.md)に従ってください）
- 🎉 [JAPANESE FACE V1](https://github.com/yKesamaru/FACE01_trained_models) が利用可能になりました！
  - `JAPANESE FACE V1` は日本人の顔認証に特化したモデルです。
- **10,000人以上**の顔データからリアルタイムで顔認証が可能です
- 超高速の顔座標出力機能
- 日付と時刻情報付きの顔画像保存機能
- 出力フレーム画像を修正する設定が可能
- 設定ファイルによる機能の集中管理
- RTSP、HTTP、USBなどの入力プロトコルを選択可能
- `顔認識` や `画像処理` のための多くの機能が利用可能です（詳細は[Useful FACE01 library](https://ykesamaru.github.io/FACE01_DEV/)をご覧ください）
- ...and many others!

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/2024-08-24_16-42.png)

---


## なぜFACE01を開発したの？

顔認証システムはあらゆるシーンで使用されるのにも関わらず、AIのコアである学習モデルはほとんどが**アメリカか中国で開発**されています。

AIコアが外国産である場合、肝心なところで「**偽陽性**」、つまり誤判定が発生することがあります。この問題は発生頻度が少ないこともあり、再現性が取りづらく、その反面、発生した場合は重大なアクシデントとなり得ます。

<!-- <br />
<div style="display: flex; align-items: center;">
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00080-2065252.png" alt="説明文" width="200" style="margin-right: 10px; border-radius: 50%; object-fit: cover;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative;">
        <p style="margin: 10;">東アジアだけに絞っても<span style="background-color: yellow;">日本人、漢民族、満州族、回族、ウイグル人、チベット人、モンゴル人、チワン族、チャン族、ミャオ族、トゥチャ族、韓民族、カザフ人、ザイ族</span>が存在します⭐️''</p>
        <p style="margin: 10;">日本人以外の顔データで学習されたモデルを日本人だけに使うのは想定されてないはずです⭐️''</p>
        <div style="position: absolute; top: 50%; left: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-right: 15px solid white; transform: translateY(-50%);"></div>
    </div>
</div>
<br /> -->
![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/2024-08-25-13-52-23.png)

このため**日本人だけの大規模顔顔データセット**から学習した「JAPANESE FACE V1」を開発し、顔認証アプリケーションに必要なクラスを揃えました。



---

## モデル性能

日本人の顔認証に特化した学習モデルは、一般的な顔認証システムが抱える問題(**若年日本人女性に対する偽陽性**)を解決しました。

たとえば、一般的な学習モデルの場合、以下に示すような若年日本人女性の判別が難しい場合があります。

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/2024-08-25-12-55-59.png)
<p align="center"><em>dlib学習モデルで偽陽性を出す例</em></p>

これに対し、新しく学習されたモデル「`JAPANESE FACE`」（下のグラフでは`JAPANESE_FACE_V1.onnx`））では、精度を落とすことなく判別できていることが示されました。

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/2024-08-25-13-01-14.png)

若年日本人女性の顔画像に対して、**DlibのAUCが0.94に対し、JAPANESE FACEは0.98を達成**しています⭐️''。

既存の顔認証モデルと比べて性能が向上してるのが分かりますね⭐️''。

くわしくは、「[Dlib顔学習モデルの、若年日本人女性データセットにおける性能評価](https://tokai-kaoninsho.com/%e3%82%b3%e3%83%a9%e3%83%a0/dlib%e9%a1%94%e5%ad%a6%e7%bf%92%e3%83%a2%e3%83%87%e3%83%ab%e3%81%ae%e3%80%81%e8%8b%a5%e5%b9%b4%e6%97%a5%e6%9c%ac%e4%ba%ba%e5%a5%b3%e6%80%a7%e3%83%87%e3%83%bc%e3%82%bf%e3%82%bb%e3%83%83%e3%83%88/) 」からご覧いただけます。

---

## ℹ️: Note
### リポジトリについて
今後の開発は`FACE01_DEV`リポジトリ（このリポジトリ）で行われます。

`FACE01_SAMPLE`リポジトリは旧バージョンのため閉鎖されました。

`FACE01_DEV`リポジトリをご使用ください。

### その他
- このリポジトリが提供するファイルは、無料でお使いいただけます。
教育機関でご利用の場合、ソースコードを研究・教育にご利用できます。
  詳しくは[日本のAI教育を支援する、顔認識ライブラリ`FACE01`の提供について](https://github.com/yKesamaru/FACE01_DEV/blob/master/LICENSE/why_apache_license.md)をご覧ください。
- 商用利用では実稼動のみライセンスが必要です。（[LICENSEファイル](https://github.com/yKesamaru/FACE01_DEV/blob/master/LICENSE/LICENSE)をご参照ください。）
- YouTubeにおけるJAPANESE FACE V1の使用ライセンスを追加しました。
  - VTuverにおける顔追従用のONNXモデルとして無料で使用できます。詳しくは[YouTube用ライセンス](https://github.com/yKesamaru/FACE01_DEV/blob/master/LICENSE/YouTube_license.md)をご参照ください。
- このリポジトリには`UBUNTU 22.04`用の`FACE01`モジュール、および`顔学習モデル`が含まれています。`Windows`ユーザーの方は、提供している`Docker`上でご利用ください。
- JAPANESE FACE（日本人に最適化された顔学習モデル）だけを使用したい場合は、[FACE01_trained_models](https://github.com/yKesamaru/FACE01_trained_models)リポジトリをご使用ください。

---

## インストール

FACE01開発環境のセッティングは本当に簡単です！

### Dockerイメージを使用する

🐳 一番簡単で環境を汚さない方法は、`Docker`を使用することです。

[こちら](https://ykesamaru.github.io/FACE01_DEV/step_by_step/docker.html)で丁寧な導入手順を解説をしていますのでぜひご覧ください。

![](assets/2024-08-26-15-20-01.png)

---

### 実働環境のPCにインストールする
実働環境を想定してまっさらなマシンに直接`FACE01`をインストールするには、`INSTALL_FACE01.sh`スクリプトを実行します。

```bash
wget https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/INSTALL_FACE01.sh
chmod +x INSTALL_FACE01.sh
bash -c ./INSTALL_FACE01.sh
```

詳しくは[こちら](https://ykesamaru.github.io/FACE01_DEV/step_by_step/Installation.html)をご覧ください。

---

## 豊富なエグザンプルコード
`example`フォルダには、様々なスクリプト例が収録されています。
(全てのスクリプトが現在のバージョンに対応しているわけではないことに注意してください)

[ステップ・バイ・ステップ](https://ykesamaru.github.io/FACE01_DEV/step_by_step.html)でEXAMPLEを試してみましょう！

<div>
<img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/docs/img/benchmark_GUI.png" width="300px" >
<img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/docs/img/distort_barrel.png" width="300px" >
<img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/docs/img/benchmark_GUI_window.png" width="300px" >
<img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/docs/img/20_times.png" width="300px" >
</div>

包括的なドキュメントは[こちら](https://ykesamaru.github.io/FACE01_DEV/)をご参照ください。

---

## ドキュメント
🧑‍💻 [丁寧で包括的なドキュメント](https://ykesamaru.github.io/FACE01_DEV/step_by_step.html)が付属します⭐️''

初心者にとっても優しい！！💗

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/2024-08-25-13-56-56.png)

全てのクラスとメソッドをまとめたリファレンスも！！

開発者にもとっても優しい💗

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/2024-08-25-14-00-26.png)

---

## Update

- 🔖 v3.0
  - オープンソースとして公開しました。
  - `LICENSE`を必ずご確認ください。
- 🔖 v2.2.02
  - `pyproject.toml`を追加。
  - `./example/*.py`について修正の追加。
- 🔖 v2.2.01
  - `EfficientNetV2 Arcface Model`を正式名称の`JAPANESE_FACE_V1`へ修正しました。
  - `Python 3.10.12`対応としました。他バージョンには対応していません。使用するシステムの`Python`バージョンが異なる場合は`Docker版`をお使いください。
  - `README`ほか、ドキュメントを日本語へ変更します。
  - 使用期限を延長しました。
  - `YouTube`で使用する際のライセンスを追加しました。
- 🔖 v2.1.05
  - Add `EfficientNetV2 Arcface Model`

---

## Acknowledgments
📄 I would like to acknowledgments those who have published such wonderful libraries and models.
1. [dlib](https://github.com/davisking/dlib) /  davisking
2. [face_recognition](https://github.com/ageitgey/face_recognition) /  ageitgey
3. [mediapipe](https://github.com/google/mediapipe) / google
4. [open_model_zoo](https://github.com/openvinotoolkit/open_model_zoo/tree/master/models/public/anti-spoof-mn3) /  openvinotoolkit
5. [light-weight-face-anti-spoofing](https://github.com/kprokofi/light-weight-face-anti-spoofing) /  kprokofi
6. [openvino2tensorflow](https://github.com/PINTO0309/openvino2tensorflow) / Katsuya Hyodo (PINTO0309)
7. [PINTO_model_zoo](https://github.com/PINTO0309/PINTO_model_zoo/tree/main/191_anti-spoof-mn3) / Katsuya Hyodo (PINTO0309)
8. [FaceDetection-Anti-Spoof-Demo](https://github.com/Kazuhito00/FaceDetection-Anti-Spoof-Demo) / KazuhitoTakahashi (Kazuhito00)
9. Some images from [Pakutaso](https://www.pakutaso.com/), [pixabay](https://pixabay.com/ja/)

---

## References

- [Deep Face Recognition A Survey](https://arxiv.org/pdf/1804.06655.pdf)
- [EfficientNetV2: Smaller Models and Faster Training](https://arxiv.org/pdf/2104.00298.pdf)
- [ArcFace: Additive Angular Margin Loss for Deep](https://arxiv.org/pdf/1801.07698.pdf)
- [MobileFaceNets: Efficient CNNs for Accurate Real-Time Face Verification on Mobile Devices](https://arxiv.org/ftp/arxiv/papers/1804/1804.07573.pdf)
- [Dlib Python API](http://dlib.net/python/index.html)
- [Pytorch documentation and Python API](https://pytorch.org/docs/stable/index.html)
- [ONNX documentation](https://onnx.ai/onnx/)
- [教育と著作権](http://www.ic.daito.ac.jp/~mizutani/literacy/copyright.pdf): 水谷正大 著, 大東文化大学 (2021)
- [日本人顔認識のための新たな学習モデル JAPANESE FACE v1](https://github.com/yKesamaru/FACE01_trained_models)