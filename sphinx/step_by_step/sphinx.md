# sphinxでのドキュメント作成手順

ここでは簡易的にsphinxを使ったドキュメント自動作成の手順をまとめます。

```bash
# 開発用ライブラリをインストールする
pip install -r requirements_dev.txt

# working dir にsphinxフォルダを作成
if [ ! -d ./sphinx ]; then mkdir ./sphinx; fi
if [ ! -d ./docs ]; then mkdir ./docs; fi

# docsフォルダに`.nojekyll`ファイルがないとgithub pages上で表示が崩れる原因になる
if [ -f ./docs/.nojekyll ]; then
    touch ./docs/.nojekyll

# sphinx-quickstartは用いない

# sphinx_bkフォルダからconf.pyとindex.rst他を複製
cp -f -r sphinx_bk/origin/* sphinx/

# [sphinx-apidoc](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)
sphinx-apidoc -f -o /home/terms/bin/FACE01_DEV/sphinx /home/terms/bin/FACE01_DEV


# titleをFACE01_DEVにする-E: 完全に再構築
sphinx-build -a -b html -E ./sphinx ./docs

```

