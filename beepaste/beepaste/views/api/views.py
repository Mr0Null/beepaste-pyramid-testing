from pyramid.response import Response
from pyramid.view import view_config
import beepaste.pasteFunctions as func
from beepaste.models.api import API
import json
import base64

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
        if request.method == "POST" and request.json_body:
            data = request.json_body

            apikey = func.fetchData(data, 'api-key')
            verifyKey(apikey, request)

            pasteRaw = func.fetchData(data, 'pasteRaw')
            data['pasteRaw'] = base64.b64encode(pasteRaw.encode('utf-8')).decode('utf-8')

            pasteLanguage = func.fetchData(data, 'pasteLanguage')
            func.verifyLanguage(pasteLanguage)

            pasteTitle = func.fetchData(data, 'pasteTitle', False)
            if pasteTitle:
                func.verifyTitleAndAuthor(pasteTitle)
            else:
                data['pasteTitle'] = pasteTitle

            pasteAuthor = func.fetchData(data, 'pasteAuthor', False)
            if pasteAuthor:
                func.verifyTitleAndAuthor(pasteAuthor)
            else:
                data['pasteAuthor'] = pasteAuthor

            pasteExpire = func.fetchData(data, 'pasteExpire', False)
            if pasteExpire:
                func.verifyExpire(pasteExpire)
            else:
                data['pasteExpire'] = "0"

            pasteEncryption = func.fetchData(data, 'pasteEncryption', False)
            if pasteEncryption:
                func.verifyEncryption(pasteEncryption)
            else:
                data['pasteEncryption'] = pasteEncryption

            newPasteURI = func.createPasteFromData(data, request)

            resp = Response()
            resp.status_int = 201
            resp.text = request.route_url('view_paste', pasteID=newPasteURI) + '\n'

            return resp
        else:
            raise Exception('invalid request.')

    except Exception as e:
        resp = Response()
        resp.status_int = 409
        resp.text = str(e) + '\n'
        return resp
