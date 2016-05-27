import pyexcel as pe
from datetime import datetime
from _compact import BytesIO, PY2


class TestSheet:
    def init(self):
        from myproject import main
        from webtest import TestApp
        self.raw_app = main({})
        self.app = TestApp(self.raw_app)

    def done(self):
        from myproject import close
        close()

    def test_single_sheet_file(self):
        array = [
            ["id", "name"],
            [1, "News"],
            [2, "Sports"]
        ]
        for upload_file_type in ['ods', 'xls']:
            self.init()
            print("Uploading %s" % upload_file_type)
            file_name = "test.%s" % upload_file_type
            io = pe.save_as(array=array, dest_file_type=upload_file_type)
            if not PY2:
                if isinstance(io, BytesIO):
                    content = io.getvalue()
                else:
                    content = io.getvalue().encode('utf-8')
            else:
                content = io.getvalue()
            response = self.app.post('/upload/categories',
                                     upload_files=[('file', file_name, content)])
            ret = pe.get_array(file_type="xls", file_content=response.body)
            assert array == ret
            self.done()


class TestBook:
    def setUp(self):
        from myproject import main
        from webtest import TestApp
        self.raw_app = main({})
        self.app = TestApp(self.raw_app)

    def test_book_file(self):
        data = {
            "category":[
                ["id", "name"],
                [1, "News"],
                [2, "Sports"]
            ],
            "post":[
                ["id", "title", "body", "pub_date", "category"],
                [1, "Title A", "formal", datetime(2015,1,20,23,28,29), "News"],
                [2, "Title B", "informal", datetime(2015,1,20,23,28,30), "Sports"]
            ]
        }
        for upload_file_type in ['xls']:
            print("Uploading %s" % upload_file_type)
            file_name = "test.%s" % upload_file_type
            io = pe.save_book_as(bookdict=data, dest_file_type=upload_file_type)
            if not PY2:
                if isinstance(io, BytesIO):
                    content = io.getvalue()
                else:
                    content = io.getvalue().encode('utf-8')
            else:
                content = io.getvalue()
            response = self.app.post('/upload/all',
                                     upload_files=[('file', file_name, content)])
            ret = pe.get_book_dict(file_type="xls", file_content=response.body)
            assert data['category'] == ret['category']
            sheet = pe.Sheet(data['post'], name_columns_by_row=0)
            sheet.column.format("pub_date", lambda d: d.isoformat())
            sheet2 = pe.Sheet(ret['post'], name_columns_by_row=0)
            for key in sheet.colnames:
                if key == "category":
                    continue
                assert sheet.column[key] == sheet2.column[key]
            assert sheet2.column['category_id'] == [1, 2]
    def tearDown(self):
        from myproject import close
        close()
