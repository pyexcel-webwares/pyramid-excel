"""
    pyramid_excel
    ~~~~~~~~~~~~~~~~~~~

    A pyramid extension that provides one application programming interface
    to read and write data in different excel file formats

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel_webio as webio
from pyramid.request import Request
from pyramid.response import Response
# import all response methods
from pyexcel_webio import (  # noqa
    make_response,
    make_response_from_array,
    make_response_from_dict,
    make_response_from_records,
    make_response_from_book_dict,
    make_response_from_a_table,
    make_response_from_query_sets,
    make_response_from_tables
)
try:
    # if in py2
    from urllib import quote as urllib_quote
    PY2_VERSION = True
except ImportError:
    # else (aka in py3)
    from urllib.parse import quote as urllib_quote # flake8: noqa
    PY2_VERSION = False


class ExcelRequestFactory(webio.ExcelInputInMultiDict, Request):
    """Pyramid Request Factory for pyexcel
    """
    def get_file_tuple(self, field_name):
        filehandle = self.POST[field_name]
        filename = filehandle.filename
        extension = filename.split(".")[1]
        return extension, filehandle.file

    def save_book_to_database(self, auto_commit=False,
                              **keywords):
        webio.ExcelInputInMultiDict.save_book_to_database(
            self,
            auto_commit=auto_commit,
            **keywords)

    def save_to_database(self, auto_commit=False,
                         **keywords):
        webio.ExcelInputInMultiDict.save_to_database(
            self,
            auto_commit=auto_commit,
            **keywords)


def _make_response(content, content_type, status, file_name=None):
    """
    Custom response function that is called by pyexcel-webio
    """
    response = Response(content, content_type=content_type, status=status)
    if file_name:
        if PY2_VERSION and isinstance(file_name, unicode):
            file_name = file_name.encode('utf-8')
        url_encoded_file_name = urllib_quote(file_name)
        response.content_disposition = (
            "attachment; filename=%s;filename*=utf-8''%s"
            % (url_encoded_file_name, url_encoded_file_name)
        )
    return response


def includeme(config):
    """ pyramid_excel extension
    """
    webio.init_webio(_make_response)
    config.set_request_factory(ExcelRequestFactory)
