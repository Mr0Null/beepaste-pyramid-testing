from pyramid.response import Response
from pyramid.view import view_config
import beepaste.pasteFunctions as func
from beepaste.selectOptions import languagesList
from beepaste.models.api import API
import json
import base64
from beepaste.models.pastes import Pastes

def verifyKey(apikey, request):
    api_count = request.dbsession.query(API).filter_by(apikey=apikey).count()
    if api_count == 0:
        raise Exception('api-key is not valid.')

@view_config(route_name='api', renderer='templates/apiView.jinja2')
def apiView(request):
    title = 'API' + " - " + request.registry.settings['beepaste.siteName']
    description = "Here is the rest-ful api! With this api you can create or get pastes in beepaste! For more information on how to work with API and for samples please visit the link."
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

            retData = {}
            retData['url'] = request.route_url('view_paste', pasteID=newPasteURI)

            resp = Response()
            resp.status_int = 201
            resp.json = retData

            return resp
        elif request.method == "GET":
            try:
                data = request.json_body
            except:
                return {'title': title, 'description': description}
            data = request.json_body
            try:
                pasteID = func.fetchData(data, 'pasteID')
                if not func.pasteExists(pasteID, request):
                    raise Exception('paste not found.')
            except Exception as e:
                resp = Response()
                resp.status_int = 404
                retData = {"error": str(e)}
                resp.json = retData
                return resp

            paste = func.getPaste(pasteID, request)

            retData = {}
            retData['url'] = request.route_url('view_paste', pasteID=paste.pasteURI)
            retData['pasteTitle'] = paste.title
            retData['pasteAuthor'] = paste.name
            retData['pasteLanguage'] = paste.lang
            retData['pasteRaw'] = base64.b64decode(paste.text).decode('utf-8')
            retData['pasteEncryption'] = paste.encryption
            retData['shortURL'] = paste.shortURL

            resp = Response()
            resp.status_int = 200
            resp.json = retData
            return resp
        else:
            raise Exception('invalid request.')

    except Exception as e:
        resp = Response()
        resp.status_int = 409
        retData = {"error": str(e)}
        resp.json = retData
        return resp

@view_config(route_name='api_langs')
def apiLang(request):
    retData = {}
    retData['pasteLanguages'] = languagesList

    resp = Response()
    resp.status_int = 200
    resp.json = retData

    return resp
