from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import pyramid_excel as excel
import pyexcel.ext.xls


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
