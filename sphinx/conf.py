# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# sys.path.insert(0, os.path.abspath("./"))
sys.path.insert(0, os.path.abspath("../"))
# sys.path.append(os.path.abspath("./example"))
# sys.path.append(os.path.abspath("./face01lib"))
# sys.path.append(os.path.abspath("../step_by_step"))
# sys.path.append(os.path.abspath("./face01lib/models"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FACE01'
copyright = '2024, yKesamaru'
author = 'yKesamaru'
release = '3.0.01'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

language = 'ja'

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
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
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

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
