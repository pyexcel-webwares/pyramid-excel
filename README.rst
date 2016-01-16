=================================================================
pyramid-excel - Let you focus on data, instead of file formats
=================================================================

.. image:: https://api.travis-ci.org/pyexcel/pyramid-excel.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyramid-excel

.. image:: https://codecov.io/github/pyexcel/pyramid-excel/coverage.png
    :target: https://codecov.io/github/pyexcel/pyramid-excel

.. image:: https://readthedocs.org/projects/pyramid-excel/badge/?version=latest
    :target: http://pyramid-excel.readthedocs.org/en/latest/
	     
**pyramid-excel** is based on `pyexcel <https://github.com/pyexcel/pyexcel>`_ and makes it easy
to consume/produce information stored in excel files over HTTP protocol as well as on file
system. This library can turn the excel data into a list of lists, a list of
records(dictionaries), dictionaries of lists. And vice versa. Hence it lets you focus on
data in Pyramid based web development, instead of file formats.

The idea originated from the problem of the illiteracy of excel file formats of non-technical
office workers: such as office assistant, human resource administrator. There is nothing
with the un-deniable fact that some people do not know the difference among various excel
formats. It becomes usability problem to those people when a web service cannot parse the
excel file that they saved using Microsoft Excel. Instead of training those people about
file formats, this library helps web developers to handle most of the excel file formats by
unifying the programming interface to most of the excel readers and writers.

The highlighted features are:

#. turn uploaded excel file directly into Python data struture
#. pass Python data structures as an excel file download
#. provide data persistence as an excel file in server side
#. supports csv, tsv, csvz, tsvz by default and other formats are supported via the following plugins:


Available Plugins
=================

================ ============================================
Plugins          Supported file formats                      
================ ============================================
`pyexcel-xls`_   xls, xlsx(r), xlsm(r)
`pyexcel-xlsx`_  xlsx
`pyexcel-ods`_   ods (python 2.6, 2.7)                       
`pyexcel-ods3`_  ods (python 2.7, 3.3, 3.4)
`pyexcel-text`_  (write only) json, rst, mediawiki, etc.
================ ============================================

.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3
.. _pyexcel-text: https://github.com/pyexcel/pyexcel-text


Known constraints
==================

Fonts, colors and charts are not supported. 

Installation
==============
You can install it via pip::

    $ pip install pyramid-excel


or clone it and install it::

    $ git clone http://github.com/pyexcel/pyramid-excel.git
    $ cd pyramid-excel
    $ python setup.py install

Installation of individual plugins , please refer to individual plugin page.

Setup
====================

Once the pyramid_excel is installed, you must use the config.include mechanism to include
it into your Pyramid project's configuration::

    config = Configurator(.....)
    config.include('pyramid_excel')

Alternately, you may activate the extension by changing your application's .ini file by
adding it to the pyramid.includes list::

    pyramid.includes = pyramid_excel


License
==========

New BSD License


Dependencies
===============

* pyexcel-webio >= 0.0.3
