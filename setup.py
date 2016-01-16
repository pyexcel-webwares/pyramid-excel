try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

dependencies = [
    'pyexcel>=0.1.5',
    'pyexcel-webio>=0.0.5',
    'pyramid>=1.5.7'
]

with open("VERSION", "r") as version:
    version_txt = version.read().rstrip()

setup(
    name='pyramid-excel',
    author="C. W.",
    version=version_txt,
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/pyramid-excel",
    description='A pyramid extension that provides one application programming interface to read and write data in different excel file formats',
    install_requires=dependencies,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'myproject']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose', 'webtest'],
    keywords=['API', 'Pyramid', 'Excel'],
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)
