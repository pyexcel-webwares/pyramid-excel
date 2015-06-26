.. pyramid-excel documentation master file, created by
   sphinx-quickstart on Wed Jun 24 17:57:06 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyramid-excel's documentation!
=========================================

:Author: C.W.
:Issues: http://github.com/chfw/pyramid-excel/issues
:License: New BSD License
:Version: |version| 
:Generated: |today|

**pyramid-excel** is based on `pyexcel <https://github.com/chfw/pyexcel>`_ and makes it easy to consume/produce information stored in excel files over HTTP protocol as well as on file system. This library can turn the excel data into a list of lists, a list of records(dictionaries), dictionaries of lists. And vice versa. Hence it lets you focus on data in pyramid based web development, instead of file formats.

The highlighted features are:

#. excel data import into and export from databases
#. turn uploaded excel file directly into Python data struture
#. pass Python data structures as an excel file download
#. provide data persistence as an excel file in server side
#. supports csv, tsv, csvz, tsvz by default and other formats are supported via the following plugins:

   
.. _file-format-list:

.. table:: A list of file formats supported by external plugins

   ================ ==========================================
   Plugins          Supported file formats                    
   ================ ==========================================
   `xls`_           xls, xlsx(r), xlsm(r)
   `xlsx`_          xlsx
   `ods3`_          ods (python 2.6, 2.7, 3.3, 3.4)                
   `ods`_           ods (python 2.6, 2.7)                     
   `text`_          (write only)json, rst, mediawiki,
                    latex, grid, pipe, orgtbl, plain simple
   ================ ==========================================
   
.. _xls: https://github.com/chfw/pyexcel-xls
.. _xlsx: https://github.com/chfw/pyexcel-xlsx
.. _ods: https://github.com/chfw/pyexcel-ods
.. _ods3: https://github.com/chfw/pyexcel-ods3
.. _text: https://github.com/chfw/pyexcel-text

This library makes infomation processing involving various excel files as easy as processing array, dictionary when processing file upload/download, data import into and export from SQL databases, information analysis and persistence. It uses **pyexcel** and its plugins: 1) to provide one uniform programming interface to handle csv, tsv, xls, xlsx, xlsm and ods formats. 2) to provide one-stop utility to import the data in uploaded file into a database and to export tables in a database as excel files for file download 3) to provide the same interface for information persistence at server side: saving a uploaded excel file to and loading a saved excel file from file system.


Installation
============
You can install it via github::

    $ git clone http://github.com/chfw/pyramid-excel.git
    $ cd pyramid-excel
    $ python setup.py install

Installation of individual plugins , please refer to individual plugin page.

Setup
====================

Once the pyramid_excel is installed, you must use the config.include mechanism to include it into your Pyramid project's configuration::

    config = Configurator(.....)
    config.include('pyramid_excel')

Alternately, you may activate the extension by changing your application's .ini file by
adding it to the pyramid.includes list::

    pyramid.includes = pyramid_excel


Quick Start
------------

Here is the quick demonstration code for pyramid-excel::

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.response import Response
    from pyramid.view import view_config
    import pyramid_excel as excel
    import pyexcel.ext.xls # pip install pyexcel-xls
    
    
    upload_form = """
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    """
    
    
    @view_config(route_name='upload')
    def upload_view(request):
        if request.method == 'POST':
            data = request.get_array(field_name='file')
            return excel.make_response_from_array(data, 'xls')
        return Response(upload_form)
    
    
    if __name__ == '__main__':
        config = Configurator()
        config.include('pyramid_excel')
        config.add_route('upload', '/upload')
        config.scan()
        app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 5000, app)
        print("Listening on 0.0.0.0:5000")
        server.serve_forever()

Before you start the server, let's install a plugin to support xls file format::

    $ pip install pyexcel-xls

And you can start the tiny server by this command, assuming you have save it as tiny_server.py::

    $ python tiny_server.py
    Listening on 0.0.0.0:5000

.. note::
    Alternatively, you can check out the code from `github <https://github.com/chfw/pyramid-excel>`_ ::
    
        git clone https://github.com/chfw/pyramid-excel.git

    The test application for pyramid-excel is a fully fledged site according to the tutorial here.
    
    Once you have the code, please change to pyramid-excel directory and then install all dependencies::
    
        $ cd pyramid-excel
        $ pip install -r requirements.txt
        $ pip install -r test_requirements.txt
    
    Then run the test application::
    
        $ pserve development.ini
        Starting server in PID 9852.
        serving on http://127.0.0.1:5000


Handle excel file upload and download
++++++++++++++++++++++++++++++++++++++

This example shows how to process uploaded excel file and how to make data download as an excel file.
Open your browser and visit http://localhost:5000/upload, you shall see this upload form:

.. image:: _static/upload-form.png

please upload an xls file and you would get this dialog:

.. image:: _static/download-dialog.png

Please focus on the following code section::

    @view_config(route_name='upload')
    def upload_view(request):
        if request.method == 'POST':
            data = request.get_array(field_name='file')
            return excel.make_response_from_array(data, 'xls')
        return Response(upload_form)

By default, the GET request will be served with upload_form. Once an excel file is uploaded,
this library kicks in and help you get the data as an array. Then you can make an excel
file as download by using make_response_from_array.


All supported data types
--------------------------

Here is table of functions for all supported data types:

=========================== ======================================================== ===================================================
data structure              from file to data structures                             from data structures to response
=========================== ======================================================== ===================================================
dict                        :meth:`~django_excel.ExcelMixin.get_dict`                :meth:`~django_excel.make_response_from_dict`
records                     :meth:`~django_excel.ExcelMixin.get_records`             :meth:`~django_excel.make_response_from_records`
a list of lists             :meth:`~django_excel.ExcelMixin.get_array`               :meth:`~django_excel.make_response_from_array`
dict of a list of lists     :meth:`~django_excel.ExcelMixin.get_book_dict`           :meth:`~django_excel.make_response_from_book_dict`
:class:`pyexcel.Sheet`      :meth:`~django_excel.ExcelMixin.get_sheet`               :meth:`~django_excel.make_response`
:class:`pyexcel.Book`       :meth:`~django_excel.ExcelMixin.get_book`                :meth:`~django_excel.make_response`
database table              :meth:`~django_excel.ExcelMixin.save_to_database`        :meth:`~django_excel.make_response_from_a_table` 
a list of database tables   :meth:`~django_excel.ExcelMixin.save_book_to_database`   :meth:`~django_excel.make_response_from_tables`
a database query sets                                                                :meth:`~django_excel.make_response_from_query_sets`
=========================== ======================================================== ===================================================

See more examples of the data structures in :ref:`pyexcel documentation<pyexcel:a-list-of-data-structures>`

If you would like to expand the list of supported excel file formats (see :ref:`file-format-list`) for your own application, you could include one or all of the following import lines::

    import pyexcel.ext.xls
    import pyexcel.ext.xlsx
    import pyexcel.ext.ods

API Reference
---------------

**pyramid-excel** attaches **pyexcel** functions to pyramid's **Request** class.

.. module:: pyramid_excel

.. autoclass:: ExcelRequestFactory

   .. method:: get_sheet(sheet_name=None, **keywords)

      :param sheet_name: For an excel book, there could be multiple sheets. If it is left
                         unspecified, the sheet at index 0 is loaded. For 'csv', 'tsv' file,
                         *sheet_name* should be None anyway.
      :param keywords: additional keywords to :meth:`pyexcel.get_sheet`
      :returns: A sheet object

   .. method:: get_array(sheet_name=None, **keywords)

      :param sheet_name: same as :meth:`~pyramid_excel.ExcelMixin.get_sheet`
      :param keywords: additional keywords to pyexcel library
      :returns: a two dimensional array, a list of lists

   .. method:: get_dict(sheet_name=None, name_columns_by_row=0, **keywords)

      :param sheet_name: same as :meth:`~pyramid_excel.ExcelMixin.get_sheet`
      :param name_columns_by_row: uses the first row of the sheet to be column headers by default.
      :param keywords: additional keywords to pyexcel library
      :returns: a dictionary of the file content

   .. method:: get_records(sheet_name=None, name_columns_by_row=0, **keywords)

      :param sheet_name: same as :meth:`~pyramid_excel.ExcelMixin.get_sheet`
      :param name_columns_by_row: uses the first row of the sheet to be record field names by default.
      :param keywords: additional keywords to pyexcel library
      :returns: a list of dictionary of the file content

   .. method:: get_book(**keywords)

      :param keywords: additional keywords to pyexcel library
      :returns: a two dimensional array, a list of lists

   .. method:: get_book_dict(**keywords)

      :param keywords: additional keywords to pyexcel library
      :returns: a two dimensional array, a list of lists

   .. method:: save_to_database(model=None, initializer=None, mapdict=None, **keywords)

      :param model: a django model
      :param initializer: a custom table initialization function if you have one
      :param mapdict: the explicit table column names if your excel data do not have the exact column names
      :param keywords: additional keywords to :meth:`pyexcel.Sheet.save_to_django_model`

   .. method:: save_book_to_database(models=None, initializers=None, mapdicts=None, **keywords)

      :param models: a list of django models
      :param initializers: a list of model initialization functions.
      :param mapdicts: a list of explicit table column names if your excel data sheets do not have the exact column names
      :param keywords: additional keywords to :meth:`pyexcel.Book.save_to_django_models`

Response methods
-----------------

.. automodule:: pyramid_excel

   .. method:: make_response(pyexcel_instance, file_type, status=200)

      :param pyexcel_instance: :class:`pyexcel.Sheet` or :class:`pyexcel.Book`
      :param file_type: one of the following strings:
                        
                        * 'csv'
                        * 'tsv'
                        * 'csvz'
                        * 'tsvz'
                        * 'xls'
                        * 'xlsx'
                        * 'xlsm'
                        * 'ods'
                          
      :param status: unless a different status is to be returned.
            
   .. method:: make_response_from_array(array, file_type, status=200)

      :param array: a list of lists
      :param file_type: same as :meth:`~pyramid_excel.make_response`
      :param status: same as :meth:`~pyramid_excel.make_response`
            
   .. method:: make_response_from_dict(dict, file_type, status=200)

      :param dict: a dictinary of lists
      :param file_type: same as :meth:`~pyramid_excel.make_response`
      :param status: same as :meth:`~pyramid_excel.make_response`
            
   .. method:: make_response_from_records(records, file_type, status=200)

      :param records: a list of dictionaries
      :param file_type: same as :meth:`~pyramid_excel.make_response`
      :param status: same as :meth:`~pyramid_excel.make_response`
            
                
   .. method:: make_response_from_book_dict(book_dict, file_type, status=200)

      :param book_dict: a dictionary of two dimensional arrays
      :param file_type: same as :meth:`~pyramid_excel.make_response`
      :param status: same as :meth:`~pyramid_excel.make_response`

   .. autofunction:: make_response_from_a_table(model, file_type status=200)


   .. method:: make_response_from_query_sets(query_sets, column_names, file_type status=200)

      Produce a single sheet Excel book of *file_type* from your custom database queries

      :param query_sets: a query set
      :param column_names: a nominated column names. It could not be None, otherwise no data is returned.
      :param file_type: same as :meth:`~pyramid_excel.make_response`
      :param status: same as :meth:`~pyramid_excel.make_response`

   .. autofunction:: make_response_from_tables(models, file_type status=200)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

