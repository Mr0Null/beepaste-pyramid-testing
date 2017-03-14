from pyramid.config import Configurator

from pyramid.view import notfound_view_config


@notfound_view_config(renderer='templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    print("booooooooooooooooooooooooooooooooooooooooz")
    return {}



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('pyramid_mailer')
    config.scan()
    return config.make_wsgi_app()
