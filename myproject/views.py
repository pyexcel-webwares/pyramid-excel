from pyramid.view import view_config
from pyramid.response import Response
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import pyexcel.ext.ods3
import pyramid_excel as excel

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'MyProject'}

@view_config(route_name='switch')
def switch(request):
    sheet = request.get_sheet(field_name='file')
    return webio.make_response(sheet, request.matchdict.get('file_type', 'csv'))

@view_config(route_name='upload', renderer='templates/upload_form.pt')
def upload_view(request):
    if request.method == 'POST':
        data = request.get_array(field_name='file')
        return excel.make_response_from_array(data, 'xls')
