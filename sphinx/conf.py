# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

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
