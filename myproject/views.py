from pyramid.view import view_config
import pyexcel.ext.xls
import pyexcel.ext.xlsx
import pyexcel.ext.ods3  # noqa
import pyramid_excel as excel


from .models import (
    DBSession,
    Category,
    Post
    )


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'MyProject'}


@view_config(route_name='switch')
def switch(request):
    sheet = request.get_sheet(field_name='file')
    return excel.make_response(sheet,
                               request.matchdict.get('file_type', 'csv'))


@view_config(route_name='upload', renderer='templates/upload_form.pt')
def upload_view(request):
    if request.method == 'POST':
        data = request.get_array(field_name='file')
        return excel.make_response_from_array(data, 'xls')


@view_config(route_name='download', renderer='templates/upload_form.pt')
def download_attachment(request):
    data = [[1, 2], [3, 4]]
    return excel.make_response_from_array(
        data,
        request.matchdict.get('file_type', 'csv'),
        file_name=request.matchdict.get('file_name', ''))


@view_config(route_name='uploadall')
def upload_all(request):

    def category_init_func(row):
        c = Category(row['name'])
        c.id = row['id']
        return c

    def post_init_func(row):
        # this is lessons learned that relation needs an object not a string
        c = DBSession.query(Category).filter_by(name=row['category']).first()
        p = Post(row['title'], row['body'], c, row['pub_date'])
        return p
    request.save_book_to_database(
        field_name='file', session=DBSession,
        tables=[Category, Post],
        initializers=[category_init_func, post_init_func])
    return excel.make_response_from_tables(DBSession, [Category, Post], "xls")


@view_config(route_name='upload_categories')
def upload_categories(request):

    def table_init_func(row):
        return Category(row['name'])
    request.save_to_database(
        field_name='file', session=DBSession,
        table=Category, initializer=table_init_func)
    return excel.make_response_from_a_table(DBSession, Category, "xls")
