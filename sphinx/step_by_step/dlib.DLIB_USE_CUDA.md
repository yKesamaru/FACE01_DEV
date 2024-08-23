# `dlib.DLIB_USE_CUDA`が`False`の場合の対処方法

> ![NOTE]
> 

<br />
<div style="display: flex; align-items: center; justify-content: flex-end;">
    <div style="background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); position: relative; margin-right: 10px;">
        <p style="margin: 10;">この作業はこちらで用意している<span style="background-color: yellow;">`Dockerイメージ`</span>を使用している場合は<span style="background-color: yellow;">不要です</span>。⭐️''</p>
        <p style="margin: 10;">本稼働対象のPCにFACE01をインストールする時、システム環境によってはここに紹介する手順が必要になる場合があります💦</p>
        <div style="position: absolute; top: 50%; right: -15px; width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 15px solid white; transform: translateY(-50%);"></div>
    </div>
    <img src="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/00129-2005948764.png" alt="説明文" width="200" style="border-radius: 50%; object-fit: cover;">
</div>
<br />

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
