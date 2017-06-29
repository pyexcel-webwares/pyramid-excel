pip freeze
nosetests --with-cov --cover-package pyramid_excel --cover-package tests --with-doctest --doctest-extension=.rst README.rst tests docs/source pyramid_excel && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
