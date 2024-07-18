# Configuration file for the Sphinx documentation builder.
"""自動ドキュメント生成のためのconf.py.

files:
    ~/bin/FACE01/sphinx_bk/conf.py
    ~/bin/FACE01/sphinx_bk/index.rst
"""
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys


# [ os.path.abspath(path)](https://docs.python.org/ja/3/library/os.path.html#os.path.abspath)
# os.path.abspath: (function)
# abspath(path: PathLike[AnyStr@abspath]) -> AnyStr@abspath
# abspath(path: AnyStr@abspath) -> AnyStr@abspath
# Return an absolute path.
# sys.path.insert: (method) insert(__index: SupportsIndex, __object: str, /) -> None
sys.path.insert(0, os.path.abspath("."))
# sys.path.append: (method) append(__object: str, /) -> None
sys.path.append(os.path.abspath("./example"))
sys.path.append(os.path.abspath("./face01lib"))
sys.path.append(os.path.abspath("./face01lib/models"))
print("sys.path: ", sys.path)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'FACE01'
copyright = '2023, yKesamaru'
author = 'yKesamaru'
release = '2.2.02'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
]

# extensions = [
#     'sphinx.ext.napoleon',
#     'myst_parser',
#     'sphinx.ext.autodoc',
# ]

# [Markdown](https://www.sphinx-doc.org/en/master/usage/markdown.html)
source_suffix = {
    '.rst': 'restructuredtext'
}

# source_suffix = {
#     '.rst': 'restructuredtext',
#     '.md': 'markdown',
# }


# この設定は、Sphinx の「exclude_patterns」オプションです。この設定で指定されたパターンのファイルやディレクトリは、Sphinx のドキュメント生成時に無視されます。
# この例では、次のパターンのファイルやディレクトリが生成されたドキュメントに含まれないように指定されています。
#     _build：Sphinx のビルド結果を保存するためのディレクトリ。
#     Thumbs.db、.DS_Store：Windows や MacOS で生成されるイメージキャッシュファイル。
#     system_check.py、compile.py、CTKtest.py、version_control.py：生成されたドキュメントに含まれないように指定された Python スクリプトファイル。
# このように、不要なファイルやディレクトリを無視することで、生成されたドキュメントのサイズや複雑さを減らすことができます。
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'system_check.py',
    'compile.py',
    'CTKtest.py',
    'version_control.py',
    'setup.py'
]


# この設定は、Sphinx の「autodoc」拡張を使用している場合に役立ちます。「autodoc」拡張は、Python のモジュール、クラス、関数などのドキュメントを自動生成する機能を提供します。
# この設定で指定されたモジュールのインポート時にエラーが発生する場合、「autodoc」拡張はモジュールのインポートに失敗してもドキュメント生成を続行するようになります。このため、「anti_spoof」、「lightweight_GUI」、「compile」といったモジュールが存在しない場合でも、Sphinx のビルド時にエラーが発生しなくなります。
# この設定は、開発環境と生成環境が異なる場合に特に役立ちます。例えば、開発環境には「anti_spoof」などのモジュールがインストールされているが、生成環境にはインストールされていない場合などです。
autodoc_mock_imports = [
    "anti_spoof",
    "lightweight_GUI",
    "compile",
]

# [sphinx.ext.napoleon – Support for NumPy and Google style docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
# Napoleon settings
# [Configuration](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#configuration)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_keyword = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
napoleon_custom_sections = None


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'sphinx_rtd_theme'  # Read the Docs
html_static_path = ['_static']
templates_path = ['_templates']
html_logo = 'https://raw.githubusercontent.com/yKesamaru/FACE01_SAMPLE/master/images/Logo_dist.png'
html_favicon = 'https://raw.githubusercontent.com/yKesamaru/FACE01_SAMPLE/master/images/Logo.ico'
# 最終更新日の記述。デフォルト：None
# html_last_updated_fmt = True
# 「autodoc」拡張機能によって生成された「Source code:」につづくリンクを変更するには、Sphinx の設定ファイル（通常は conf.py）に以下のような設定を追加することが必要です。
html_context = {
    'base_url': 'https://github.com/yKesamaru/FACE01_SAMPLE/tree/master/'
}
html_use_opensearch = 'https://github.com/yKesamaru/FACE01_SAMPLE/tree/master'

# html_additional_pages = {
#     'Tokai kaoninsho': 'https://tokai-kaoninsho.com/',
#     'GitHub': 'https://github.com/yKesamaru/FACE01_SAMPLE'
# }
html_copy_source = False
html_show_sourcelink = False