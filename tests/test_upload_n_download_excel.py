import pyexcel as pe
from _compact import BytesIO, PY2


FILE_TYPE_MIME_TABLE = {
    "csv": "text/csv",
    "tsv": "text/tab-separated-values",
    "csvz": "application/zip",
    "tsvz": "application/zip",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
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
                print("Uploading %s Downloading %s" % (upload_file_type, download_file_type))
                io = pe.get_io(upload_file_type)
                sheet = pe.Sheet(self.data)
                sheet.save_to_memory(upload_file_type, io)
                io.seek(0)
                if not PY2:
                    if isinstance(io, BytesIO):
                        content = io.getvalue()
                    else:
                        content = io.getvalue().encode('utf-8')
                else:
                    content = io.getvalue()
                response = self.app.post('/switch/%s' % download_file_type,
                                         upload_files = [('file', file_name, content)],
                                         )
                assert response.content_type == FILE_TYPE_MIME_TABLE[download_file_type]
                sheet = pe.get_sheet(file_type=download_file_type, file_content=response.body)
                sheet.format(int)
                array = sheet.to_array()
                assert array == self.data

    def test_download(self):
        test_file_name = "test"
        for file_type in FILE_TYPE_MIME_TABLE.keys():
            response = self.app.get('/download/%s/%s' % (test_file_name, file_type))
            assert response.content_type == FILE_TYPE_MIME_TABLE[file_type]
            expected = "attachment; filename=%s.%s" % (test_file_name, file_type)
            assert response.content_disposition == expected
