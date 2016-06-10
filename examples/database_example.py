from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import pyramid_excel as excel
import datetime
import pyexcel.ext.xls  # noqa


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

# database operations
from sqlalchemy import (  # noqa
    Column,
    Integer,
    Text,
    String,
    ForeignKey,
    DateTime,
    create_engine
    )

from sqlalchemy.ext.declarative import declarative_base  # noqa
from sqlalchemy.orm import relationship, backref  # noqa
from sqlalchemy.orm import (  # noqa
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension  # noqa

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    body = Column(Text)
    pub_date = Column(DateTime)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category',
                            backref=backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


@view_config(route_name="import")
def doimport(request):
    if request.method == 'POST':

        def category_init_func(row):
            c = Category(row['name'])
            c.id = row['id']
            return c

        def post_init_func(row):
            c = DBSession.query(Category).filter_by(
                name=row['category']).first()
            p = Post(row['title'], row['body'], c, row['pub_date'])
            return p
        request.save_book_to_database(
            field_name='file', session=DBSession,
            tables=[Category, Post],
            initializers=[category_init_func, post_init_func])
        return Response("Saved")
    return Response(upload_form)


@view_config(route_name="export")
def doexport(request):
    return excel.make_response_from_tables(DBSession, [Category, Post], "xls")


@view_config(route_name="custom_export")
def docustomexport(request):
    query_sets = DBSession.query(Category).filter_by(id=1).all()
    column_names = ['id', 'name']
    return excel.make_response_from_query_sets(query_sets, column_names, "xls")


def init_db():
    engine = create_engine('sqlite:///tmp.db')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_excel')
    config.add_route('upload', '/upload')
    config.add_route('import', '/import')
    config.add_route('export', '/export')
    config.add_route('custom_export', '/custom_export')
    config.scan()
    init_db()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app)
    print("Listening on 0.0.0.0:5000")
    server.serve_forever()
