# Configuration file for the Sphinx documentation builder.
import os
import sys

# プロジェクトのルートディレクトリを基準にパスを追加
sys.path.insert(0, os.path.abspath(".."))
# sys.path.append(os.path.abspath("../example"))
# sys.path.append(os.path.abspath("../face01lib"))
# sys.path.append(os.path.abspath("../face01lib/models"))

project = 'FACE01_DEV'
copyright = '2024, yKesamaru'
author = 'yKesamaru'
release = '3.3.01'

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'myst_parser',  # markdown文書用
]

autodoc_typehints = "description"

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

myst_enable_extensions = [
    "dollarmath",
    "html_admonition",
    "html_image",
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_output = '_build/html'
templates_path = ['_templates']
html_logo = 'https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/Logo_dist.png'
html_favicon = 'https://raw.githubusercontent.com/yKesamaru/FACE01_DEV/master/assets/images/Logo.ico'
html_use_opensearch = 'https://github.com/yKesamaru/FACE01_DEV/tree/master'
html_copy_source = True
html_show_sourcelink = True
