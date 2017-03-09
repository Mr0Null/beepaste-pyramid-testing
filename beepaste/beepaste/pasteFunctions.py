from pyshorteners import Shortener
from beepaste.models.pastes import Pastes
import string
from random import *
import datetime
from wtforms import Form, TextField, SelectField, validators, RadioField
from beepaste.selectOptions import languagesList, encryptionMethods, expireTimes

class createPasteForm(Form):
    pasteTitle = TextField('Title', [validators.Length(min=0, max=255)])
    pasteAuthor = TextField('Author', [validators.Length(min=0, max=255)])
    pasteLanguage = SelectField('Syntax Highlighting', choices=languagesList, default='text', validators=[validators.Required()])
    pasteExpire = SelectField('Expire On', choices=expireTimes, validators=[validators.Required()])
    pasteRaw = TextField('Raw Text', [validators.Required()])
    pasteEncryption = RadioField('Paste Encryption', choices=encryptionMethods)

def pasteExists(uri, request):
    old_uris_count = request.dbsession.query(Pastes).filter_by(pasteURI=uri).count()
    if old_uris_count > 0:
        return True
    return False

def generateURI(len):
    allchar = string.ascii_letters + string.digits
    uri = "".join(choice(allchar) for x in range(len))
    return uri

def generateShortURL(url, request):
    access_token = request.registry.settings['beepaste.bitlyToken']
    shortener = Shortener('Bitly', bitly_token=access_token)
    return shortener.short(url)

def createPaste(form, request):
    newPaste = Pastes()
    URI = generateURI(6)
    while pasteExists(URI, request):
        URI = generateURI(6)
    newPaste.pasteURI = URI
    if form.pasteTitle.data:
        newPaste.title = form.pasteTitle.data
    if form.pasteAuthor.data:
        newPaste.name = form.pasteAuthor.data
    newPaste.lang = form.pasteLanguage.data
    newPaste.text = form.pasteRaw.data
    if form.pasteExpire.data != "0":
        newPaste.toexpire = True
        newPaste.expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(form.pasteExpire.data))
    newPaste.encryption = form.pasteEncryption.data
#   newPaste.shortURL = generateShortURL(request.route_url('view_paste', pasteID=URI), request)
    request.dbsession.add(newPaste)
    return URI
