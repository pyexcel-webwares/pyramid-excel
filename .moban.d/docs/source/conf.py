{% extends 'docs/source/conf.py.jj2' %}

{%block custom_doc_theme%}
html_theme='pyramid'
html_theme_options={'github_url': 'https://github.com/Pylons/pyramid'}
html_theme_path = ['_themes']
{%endblock%}
