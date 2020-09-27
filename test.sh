pip freeze
nosetests --with-coverage --cover-package pyramid_excel --cover-package tests tests --with-doctest --doctest-extension=.rst README.rst docs/source pyramid_excel
