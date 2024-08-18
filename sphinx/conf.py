# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
for i in sys.path:
    print(i)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FACE01'
copyright = '2024, yKesamaru'
author = 'yKesamaru'
release = '3.0.03'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',
    'myst_parser',
    # 'sphinx_wagtail_theme'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'NumPy': ('https://numpy.org/doc/stable/reference/index.html#reference', None)
}

language = 'ja'

# Googleスタイルのdocstringをサポートするかどうかを指定。`True`: GoogleスタイルのdocstringをSphinxが理解し、正しくフォーマットする。
napoleon_google_docstring = True
# NumPyスタイルのdocstringをサポートするかどうかを指定。`False`: NumPyスタイルのdocstringはサポートされない。
napoleon_numpy_docstring = False
# クラスの`__init__`メソッドのdocstringをクラスのdocstringに含めるかどうかを指定。`False`: `__init__`のdocstringは無視される。
napoleon_include_init_with_doc = False
# プライベートメンバー（アンダースコアで始まるメソッドや属性）のdocstringをドキュメントに含めるかどうかを指定。`False`: プライベートメンバーのdocstringは無視される。
napoleon_include_private_with_doc = False
# 特殊メソッド（`__str__`, `__repr__`など）のdocstringをドキュメントに含めるかどうかを指定。`True`: 特殊メソッドのdocstringもドキュメントに含まれる。
napoleon_include_special_with_doc = True
# "Examples"セクションに対してadmonition（注意書き）ブロックを使用するかどうかを指定。`True`: "Examples"セクションがadmonitionブロックとして表示される。
napoleon_use_admonition_for_examples = True
# "Notes"セクションに対してadmonitionブロックを使用するかどうかを指定。`False`: 通常のセクションとして表示される。
napoleon_use_admonition_for_notes = False
# "References"セクションに対してadmonitionブロックを使用するかどうかを指定。`False`: 通常のセクションとして表示される。
napoleon_use_admonition_for_references = False
# 属性（インスタンス変数）を`ivar`フィールドとしてドキュメントに含めるかどうかを指定。`False`: 通常の属性として扱われる。
napoleon_use_ivar = False
# 関数やメソッドの引数に対して`param`フィールドを使用するかどうかを指定。`True`: 引数が`param`フィールドとして表示される。
napoleon_use_param = True
# 関数やメソッドのキーワード引数に対して`keyword`フィールドを使用するかどうかを指定。`True`: キーワード引数が`keyword`フィールドとして表示される。
napoleon_use_keyword = True
# 関数やメソッドの戻り値に対して`rtype`フィールドを使用するかどうかを指定。`True`: 戻り値が`rtype`フィールドとして表示される。
napoleon_use_rtype = True
# 型情報を事前に処理するかどうかを指定。`False`: 型情報はそのまま表示される。
napoleon_preprocess_types = False
# 型の別名（type alias）を定義するための辞書。`None`: 別名は定義されない。
napoleon_type_aliases = None
# 属性にアノテーションがある場合、それをドキュメントに含めるかどうかを指定。`True`: アノテーションもドキュメントに含まれる。
napoleon_attr_annotations = True
# カスタムセクションを定義するためのリスト。`None`: カスタムセクションは定義されない。
napoleon_custom_sections = None


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# -- HTML THEME OPTIONS ------------------------------------------------------
# ---- READ THE DOCS ---------------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_logo = 'https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/Logo_dist.png'
html_favicon = 'https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/Logo.ico'
# html_last_updated_fmt = True
# ---- WAGTAIL THEME ---------------------------------------------------------
# https://sphinx-wagtail-theme.readthedocs.io/en/latest/customizing.html
# html_theme = 'sphinx_wagtail_theme'
# html_theme_options = dict(
#     project_name="FACE01_DEV",
#     logo="https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/Logo_dist.png",
#     # logo="Logo_dist.png",
#     logo_alt="Tokai-kaoninsho",
#     logo_url="https://tokai-kaoninsho.com/",
#     logo_height=55,
#     logo_width=57,
#     github_url="https://github.com/yKesamaru/FACE01_DEV",
#     footer_links=",".join([
#         "About Us|https://tokai-kaoninsho.com/",
#         "Contact|https://tokai-kaoninsho.com/%e3%81%8a%e5%95%8f%e3%81%84%e5%90%88%e3%82%8f%e3%81%9b/",
#         "Legal|https://github.com/yKesamaru/FACE01_DEV/blob/master/LICENSE",
#     ]),
# )
# copyright = "2024, yKesamaru, 東海顔認証"
# html_show_copyright = True
# html_last_updated_fmt = "%b %d, %Y"

html_static_path = ['_static']
# メソッドなどのページに区切り線を挿入する
html_css_files = [
    'custom.css',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_context = {
    'base_url': 'https://github.com/yKesamaru/FACE01_DEV/tree/master/'
}
html_use_opensearch = 'https://github.com/yKesamaru/FACE01_DEV/tree/master'

# html_additional_pages = {
#     'Tokai kaoninsho': 'https://tokai-kaoninsho.com/',
#     'GitHub': 'https://github.com/yKesamaru/FACE01_DEV'
# }
html_copy_source = False
html_show_sourcelink = False

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
