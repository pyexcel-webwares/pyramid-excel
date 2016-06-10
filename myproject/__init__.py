from pyramid.config import Configurator
from sqlalchemy import create_engine

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = create_engine('sqlite:///tmp.db')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    config = Configurator(settings=settings)
    config.include('pyramid_excel')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('upload', '/upload')
    config.add_route('download', '/download/{file_name}/{file_type}')
    config.add_route('switch', '/switch/{file_type}')
    config.add_route('uploadall', '/upload/all')
    config.add_route('upload_categories', '/upload/categories')
    config.scan()
    return config.make_wsgi_app()


def close():
    DBSession.close()
