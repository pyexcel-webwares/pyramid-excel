"""
    pyramid_excel
    ~~~~~~~~~~~~~~~~~~~

    A pyramid extension that provides one application programming interface
    to read and write data in different excel file formats

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel as pe
import pyexcel_webio as webio
from pyramid.request import Request
from pyramid.response import Response


class ExcelRequestFactory(webio.ExcelInputInMultiDict, Request):
    """Pyramid Request Factory for pyexcel
    """
    def get_file_tuple(self, field_name):
        filehandle = self.POST[field_name]
        filename = filehandle.filename
        extension = filename.split(".")[1]
        return extension, filehandle.file


# set up webio
webio.ExcelResponse = Response


# import all response methods
from pyexcel_webio import (
    make_response,
    make_response_from_array,
    make_response_from_dict,
    make_response_from_records,
    make_response_from_book_dict,
    make_response_from_a_table,
    make_response_from_query_sets,
    make_response_from_tables
)


def includeme(config):
    """ pyramid_excel extension
    """
    config.set_request_factory(ExcelRequestFactory)


    
