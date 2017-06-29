# -*- coding: utf-8 -*-

import pyexcel as pe
from _compact import PY2
from nose.tools import eq_
try:
    # if in py2
    from urllib import quote as urllib_quote
    PY2_VERSION = True
except ImportError:
    # else (aka in py3)
    from urllib.parse import quote as urllib_quote # flake8: noqa
    PY2_VERSION = False


_XLSX_MIME = (
    "application/" +
    "vnd.openxmlformats-officedocument.spreadsheetml.sheet")

FILE_TYPE_MIME_TABLE = {
    "csv": "text/csv",
    "tsv": "text/tab-separated-values",
    "csvz": "application/zip",
    "tsvz": "application/zip",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "xls": "application/vnd.ms-excel",
    "xlsx": _XLSX_MIME,
    "xlsm": "application/vnd.ms-excel.sheet.macroenabled.12"
}


class TestExcelResponse:
    def setUp(self):
        from myproject import main
        from webtest import TestApp
        self.raw_app = main({})
        self.app = TestApp(self.raw_app)
        self.data = [
            [1, 2, 3],
            [4, 5, 6]
        ]

    def test_upload_and_download(self):
        for upload_file_type in FILE_TYPE_MIME_TABLE.keys():
            file_name = 'test.%s' % upload_file_type
            for download_file_type in FILE_TYPE_MIME_TABLE.keys():
                print("Uploading %s Downloading %s" % (upload_file_type,
                                                       download_file_type))
                sheet = pe.Sheet(self.data)
                io = sheet.save_to_memory(upload_file_type).getvalue()
                if not PY2:
                    if isinstance(io, bytes):
                        content = io
                    else:
                        content = io.encode('utf-8')
                else:
                    content = io
                response = self.app.post(
                    '/switch/%s' % download_file_type,
                    upload_files=[('file', file_name, content)],
                )
                eq_(response.content_type,
                    FILE_TYPE_MIME_TABLE[download_file_type])
                sheet = pe.get_sheet(file_type=download_file_type,
                                     file_content=response.body)
                sheet.format(int)
                array = sheet.to_array()
                assert array == self.data

    def test_download_file_name_in_ascii(self):
        test_file_name = "test"
        self._download_and_verify_file_name(test_file_name)

    def test_download_file_name_in_unicode(self):
        test_file_name = u'中文文件名'
        self._download_and_verify_file_name(test_file_name.encode('utf-8'))

    def test_download_file_name_in_unicode_in_string(self):
        test_file_name = '中文文件名'
        self._download_and_verify_file_name(test_file_name)

    def _download_and_verify_file_name(self, test_file_name):
        for file_type in FILE_TYPE_MIME_TABLE.keys():
            response = self.app.get(
                '/download/%s/%s' % (test_file_name, file_type))
            eq_(response.content_type,
                FILE_TYPE_MIME_TABLE[file_type])
            url_encoded_file_name = urllib_quote(test_file_name)
            expected = (
                "attachment; filename=%s.%s;filename*=utf-8''%s.%s"
                % (url_encoded_file_name, file_type,
                   url_encoded_file_name, file_type))
            assert response.content_disposition == expected
