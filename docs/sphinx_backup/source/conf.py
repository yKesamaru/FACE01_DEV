# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# [ os.path.abspath(path)](https://docs.python.org/ja/3/library/os.path.html#os.path.abspath)
# プロジェクトのルートディレクトリを基準にパスを追加
# sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("../example"))
sys.path.append(os.path.abspath("../face01lib"))
sys.path.append(os.path.abspath("../face01lib/models"))

# DEBUG
# for i in sys.path:
#     print(i)
# exit()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'FACE01_DEV'
copyright = '2024, yKesamaru'
author = 'yKesamaru'
release = '3.3.01'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx_autodoc_typehints',  # 型ヒントのサポート
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'myst_parser',  # markdown文書用
]

# [Markdown](https://www.sphinx-doc.org/en/master/usage/markdown.html)
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# myst-parserの設定を追加
myst_enable_extensions = [
    "dollarmath",  # ドル記号を使った数式を有効にする
    "html_admonition",  # HTML形式のアドモニションを有効にする
    "html_image",  # HTML形式の画像を有効にする
    # "colon_fence",  # コロンフェンスを有効にする
    # "deflist",  # 定義リストを有効にする
    # "replacements",  # プレースホルダー置換を有効にする
    # "smartquotes",  # スマートクォートを有効にする
    # "substitution",  # 置換を有効にする
    # "tasklist",  # タスクリストを有効にする
]

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

autodoc_mock_imports = [
    "anti_spoof",
    "lightweight_GUI",
    "compile",
    "customtkinter",
    "PySimpleGUI",
    "Cython",
    # "face01lib"
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
html_output = '_build/html'
templates_path = ['_templates']
html_logo = 'https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/Logo_dist.png'
html_favicon = 'https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/Logo.ico'
html_use_opensearch = 'https://github.com/yKesamaru/FACE01_DEV/tree/master'
html_copy_source = True
html_show_sourcelink = True
