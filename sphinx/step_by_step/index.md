# FACE01ライブラリのステップバイステップガイド
**FACE01の世界へようこそ！**

この記事では、エグザンプルプログラムを使用して、FACE01を用いた顔認識アプリケーションを作成するために必要な知識と技術を紹介します。

準備はいいですか？

まずは、**チェック項目を確認**しましょう。

<!-- TOC
1. [FACE01ライブラリのステップバイステップガイド](#face01ライブラリのステップバイステップガイド)
   1. [チェック項目](#チェック項目)
   2. [顔画像の登録](#顔画像の登録)
   3. [仮想Python環境の有効化](#仮想python環境の有効化)
   4. [vimのインストール確認](#vimのインストール確認)
2. [FACE01の簡単な使用フロー](#face01の簡単な使用フロー)
3. [簡単な顔認識](#簡単な顔認識)
4. [GUIウィンドウの表示](#guiウィンドウの表示)
5. [会社の「テロップ」や「ロゴ」画像を表示](#会社の「テロップ」や「ロゴ」画像を表示)
6. [ベンチマークを取りたい？](#ベンチマークを取りたい)
7. [例リスト](#例リスト)
8. [トラブルシューティング:thinking:](#トラブルシューティングthinking)
   1. [CUDAが動作しない](#cudaが動作しない)
   2. [dlib.DLIB\_USE\_CUDAがFalseの場合の対処法](#dlibdlib_use_cudaがfalseの場合の対処法) -->

## チェック項目
✅
- [x] Pythonの基本操作
- [x] Dockerの基本操作
- [x] Linuxターミナルの基本操作
- [x] (Nvidia GPUを使用する場合) CUDAドライバがすでにインストールされていること

すべての項目を確認しましたか？
OK！では始めましょう！

## [FACE01のインストール](Installation.md)
ここでは、FACE01のインストール方法について解説します。
[こちら](Installation.md)をご覧ください。

## [Dockerのインストール](install_docker.md)
`Docker`を使用する方法は[こちら](install_docker.md)をご覧ください。
また具体的な`Docker`の使用法について[こちら](docker.md)で解説しています。

## [顔画像の登録](register_faces.md)
この記事では、顔画像の登録方法について説明します。
詳細は[こちら](register_faces.md)をご覧ください。

## 仮想Python環境の有効化
Python標準ライブラリの`venv`を使用して仮想環境を開始します。

```bash
# 仮想環境の有効化
. bin/activate
```

## vimのインストール確認
Dockerイメージにはvimがインストールされているので、`conf.ini`を編集できます。

```bash
# vimのインストール確認
which vim
```

## [設定ファイルの編集](config_ini.md)
設定は`config.ini`ファイルで行います。
`config.ini`ファイルについては[こちら](config_ini.md)をご覧ください。

## [FACE01の簡単な使用フロー](simple_flow.md)
FACE01の使い方の一例ですが、簡単なフローを見てみましょう。
詳細は[こちら](simple_flow.md)をご覧ください。

## [ファンクションについて](functions.md)
`FACE01`を試用する上での基本的なファンクションについて[こちら](functions.md)で確認しましょう。

## [簡単な顔認識](simple.md)
`simple.py`を試してみましょう。
simple.pyはCUI動作のためのエグザンプルのスクリプトです。

```python
python example/simple.py
```
詳細は[こちら](simple.md)をご覧ください。

## [GUIウィンドウの表示](display_GUI_win.md)
かっこいいGUIウィンドウに表示したいですか？  
`example/display_GUI_window.py`を試してみてください。  
詳細は[こちら](display_GUI_win.md)をご覧ください。

```python
python example/display_GUI_window.py
```
詳細は[こちら](simple.md)をご覧ください。

## [会社の「テロップ」や「ロゴ」画像を表示](ch_telop.md)
ウィンドウに会社のロゴなどを表示したいですか？  
もちろん可能です！  
詳細は[こちら](ch_telop.md)をご覧ください。

## [ベンチマークを取りたい？](benchmark_CUI.md)
詳細は[こちら](benchmark_CUI.md)をご覧ください。

## エグザンプルリスト
```python
# 1. Simple
python example/simple.py

# 2. Display GUI window
python example/display_GUI_window.py

# 3. logging
python example/example_logging.py

# 4. data structure
python example/data_structure.py

# 5. Benchmark with CUI mode
python example/benchmark_CUI.py

# 6. Benchmark with GUI mode
python example/benchmark_GUI_window.py

# Other
- example/aligned_crop_face.py
- example/anti_spoof.py
- example/distort_barrel.py
- example/draw_datas.py
- example/face_coordinates.py
- example/get_encoded_data.py
- example/lightweight_GUI.py
...and others.
```

**FACE01の多くのクラスとメソッドの詳細については、[FACE01ドキュメント](https://ykesamaru.github.io/FACE01_DEV/)をご覧ください。**

## トラブルシューティング:thinking:
### CUDAが動作しない
[CUDAライブラリをすべて削除して再インストールする方法](reinstall_gpu.md)をご覧ください。

### dlib.DLIB_USE_CUDAがFalseの場合の対処法
[dlib.DLIB_USE_CUDAがFalseの場合の対処法](dlib.DLIB_USE_CUDA.md)をご覧ください。
