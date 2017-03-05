from pyramid.response import Response
from pyramid.view import view_config
from beepaste.models.pastes import Pastes
import base64

@view_config(route_name='view_raw', renderer='templates/pasteRaw.jinja2')
def viewRaw(request):
    uri = request.matchdict['pasteID']
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=uri).first()
    raw = base64.b64decode(paste.text)
    return {'raw': raw}

@view_config(route_name='view_paste', renderer='templates/pasteView.jinja2')
def viewPaste(request):
    uri = request.matchdict['pasteID']
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=uri).first()
    embedCode = '<iframe src="' + request.route_url('view_embed', pasteID=paste.pasteURI) +'" style="border:none;width:100%;min-height:300px;"></iframe>'
    return {'paste': paste, 'embedCode': embedCode}
