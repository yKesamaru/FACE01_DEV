# `dlib.DLIB_USE_CUDA`が`False`の場合の対処方法

> ![NOTE]
> この作業はこちらで用意している`Dockerイメージ`を使用している場合は不要です。


`FACE01`では、`GPU`の利用率を最大化するために`CUDA`を使用します。通常、ターミナルで`pip install dlib`と入力することで、使用環境に応じて`CUDA`を使用できるようになります。

`CUDA`が利用可能かどうかを確認するには、以下のコマンドを使用します。
```bash
(FACE01)
FACE01 $ pip freeze | grep dlib
dlib==19.24.0
(FACE01)
FACE01 $ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47)
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.DLIB_USE_CUDA
True
>>>
```
この時点で`False`が表示される場合、`CUDA`を使用出来ていないことが判明します。

## `Dlib`のアンインストール

まず、以下のコマンドを使用して`Dlib`をアンインストールしてください。
```bash
pip uninstall dlib
```

## `dlib-19.24.tar.bz2`の解凍

`dlib-19.24.tar.bz2`を解凍し、`dlib-19.24`ディレクトリを作成します。
```bash
tar xvjf dlib-19.24.tar.bz2
cd dlib-19.24
```

## `gcc-8`を使用してビルド

Dlibをビルドする際には、`gcc`のバージョンが非常に重要です。`gcc`のバージョンが`8`以降の場合はサポートされません。次のようにして、`gcc-8`などを指定します。
```bash
(FACE01)
FACE01/dlib-19.24 $ export CC=/usr/bin/gcc-8
(FACE01)
FACE01/dlib-19.24 $ export CXX=/usr/bin/g++-8
(FACE01)
FACE01/dlib-19.24 $ python setup.py install
```

## インストールの確認

以下のコマンドでインストールが成功したか確認します。
```bash
(FACE01)
FACE01/dlib-19.24 $ pip freeze | grep dlib
dlib==19.24.0
(FACE01)
FACE01/dlib-19.24 $ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47)
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.DLIB_USE_CUDA
True
>>>
(FACE01)
FACE01/dlib-19.24 $
```
`True`であることが確認できたら、作業は完了です🎉。
