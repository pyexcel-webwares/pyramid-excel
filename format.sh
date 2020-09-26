isort $(find pyramid_excel -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 pyramid_excel
black -l 79 tests
