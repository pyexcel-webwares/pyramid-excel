# -*- coding: utf-8 -*-
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

intersphinx_mapping = {
    'pyexcel': ('http://pyexcel.readthedocs.org/en/latest/', None)
}
spelling_word_list_filename = 'spelling_wordlist.txt'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'pyramid-excel'
copyright = u'2015-2016 Onni Software Ltd.'
version = '0.0.3'
release = '0.0.4'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'pyramid'
html_theme_options = {'github_url': 'https://github.com/Pylons/pyramid'}
html_theme_path = ['_themes']
html_static_path = ['_static']
htmlhelp_basename = 'pyramid-exceldoc'
latex_elements = {}
latex_documents = [
    ('index', 'pyramid-excel.tex', u'pyramid-excel Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'pyramid-excel', u'pyramid-excel Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'pyramid-excel', u'pyramid-excel Documentation',
     'Onni Software Ltd.', 'pyramid-excel', 'One line description of project.',
     'Miscellaneous'),
]
