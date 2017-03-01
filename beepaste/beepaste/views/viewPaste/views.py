from pyramid.response import Response
from pyramid.view import view_config
from beepaste.models.pastes import Pastes

@view_config(route_name='view_raw', renderer='templates/pasteRaw.jinja2')
def viewRaw(request):
    uri = request.matchdict['pasteID']
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=uri).first()
    return {'paste': paste}
