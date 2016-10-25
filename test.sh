

pip freeze
nosetests --with-cov --cover-package Pyramid_excel --cover-package tests --with-doctest --doctest-extension=.rst tests README.rst docs/source pyramid_excel && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
