<div align="center">

<img src="https://raw.githubusercontent.com/yKesamaru/FACE01_sample/master/images/g1320.png" width="200px">

✨ `FACE01`は**日本人の顔に最適化された顔学習モデルJAPANESE FACEと、<br />
Pythonで書かれたオープンソースのリファレンス実装**です。

⚡️ Apache License 2.0と商用ライセンスのデュアルライセンス！

⚡️ 日本人の顔に最適化された顔学習モデル⭐️''

⚡️ 豊富なクラスとメソッド！

⚡️ 包括的な[ドキュメント](https://ykesamaru.github.io/FACE01_DEV/index.html)付属！

FACE01 -- さあ、始めましょう！

___

![GitHub commit activity](https://img.shields.io/github/commit-activity/y/yKesamaru/FACE01_DEV)
![](https://img.shields.io/badge/Release-v3.0-blue)
![](https://img.shields.io/badge/Python-%3E%3D3.10.12-blue)

![](docs/img/ROMAN_HOLIDAY.GIF?raw=true)

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

📖 TOC
- [About FACE01](#about-face01)
- [ℹ️: Note](#ℹ️-note)
  - [リポジトリについて](#リポジトリについて)
  - [その他](#その他)
- [インストール](#インストール)
  - [Dockerイメージを使用する](#dockerイメージを使用する)
  - [実働環境のPCにインストールする](#実働環境のpcにインストールする)
- [豊富なエグザンプルコード](#豊富なエグザンプルコード)
- [ドキュメント](#ドキュメント)
- [設定ファイル: config.ini](#設定ファイル-configini)
- [Update](#update)
- [Acknowledgments](#acknowledgments)
- [References](#references)

---

## About FACE01
✨ `FACE01`は**日本人の顔に最適化された顔学習モデルJAPANESE FACEと、Pythonで書かれたオープンソースのリファレンス実装**です。

![](https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/2024-08-23_07-55.png)

- 🎉 LICENSEが「もっと使いやすく」なりました！実稼動以外はアパッチライセンスV2です！
- 🎉 `v3.0.0`よりオープンソースとして公開いたしました。（`LICENSE`に従ってください）
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

[こちら](https://ykesamaru.github.io/FACE01_DEV/step_by_step/index.html#docker)で丁寧な導入手順を解説をしていますのでぜひご覧ください。

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
<img src="docs/img/benchmark_GUI.png" width="300px" >
<img src="docs/img/distort_barrel.png" width="300px" >
<img src="docs/img/benchmark_GUI_window.png" width="300px" >
<img src="docs/img/20_times.png" width="300px" >
</div>

包括的なドキュメントは[こちら](https://ykesamaru.github.io/FACE01_DEV/)をご参照ください。

## ドキュメント

- 🧑‍💻 [Step-by-step to use FACE01 library](https://ykesamaru.github.io/FACE01_DEV/step_by_step.html)
  - 初心者向け

    <img src="docs/img/step-by-step.png" width="400px" >

- 🧑‍💻 [Comprehensive and detailed documentation](https://ykesamaru.github.io/FACE01_DEV/face01lib.html)
  - 中級者以上向けの包括的なリソース

    <img src="docs/img/document.png" width="400px" >

## 設定ファイル: config.ini

高い柔軟性を備えた使いやすい設定ファイルで自由自在に設定しましょう！
詳しくは[こちら](https://ykesamaru.github.io/FACE01_DEV/step_by_step/index.html#id5)をご覧ください。


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