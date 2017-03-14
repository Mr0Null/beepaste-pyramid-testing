from pyramid.response import Response
from pyramid.view import view_config
import beepaste.pasteFunctions as func
from beepaste.models.api import API
import json

def verifyKey(apikey, request):
    api_count = request.dbsession.query(API).filter_by(apikey=apikey).count()
    if api_count == 0:
        raise Exception('api-key is not valid.')

@view_config(route_name='api', renderer='templates/apiView.jinja2')
def apiView(request):
    title = 'API' + " - " + request.registry.settings['beepaste.siteName']
    return {'title': title}

@view_config(route_name='api_create', renderer='templates/apiReturn.jinja2')
def apiCreate(request):
    try:
        data = request.json_body

        apikey = func.fetchData(data, 'api-key')
        verifyKey(apikey, request)

        pasteRaw = func.fetchData(data, 'pasteRaw')

        pasteLanguage = func.fetchData(data, 'pasteLanguage')
        func.verifyLanguage(pasteLanguage)

        pasteTitle = func.fetchData(data, 'pasteTitle', False)
        func.verifyTitleAndAuthor(pasteTitle)

        pasteAuthor = func.fetchData(data, 'pasteAuthor', False)
        func.verifyTitleAndAuthor(pasteAuthor)

        pasteExpire = func.fetchData(data, 'pasteExpire', False)
        func.verifyExpire(pasteExpire)

        pasteEncryption = func.fetchData(data, 'pasteEncryption', False)
        func.verifyEncryption(pasteEncryption)

        newPasteURI = func.createPasteFromData(data, request)

        resp = Response()
        resp.status_int = 201
        resp.text = newPasteURI

        return resp

    except Exception as e:
        resp = Response()
        resp.status_int = 409
        resp.text = str(e)
        return resp
