from pyramid.response import Response
from pyramid.view import view_config
from beepaste.selectOptions import languagesList, encryptionMethods, expireTimes
from beepaste.models.pastes import Pastes

import string
from random import *

import datetime
from wtforms import Form, TextField, SelectField, validators, RadioField

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    class createPaste(Form):
        pasteTitle = TextField('Title', [validators.Length(min=0, max=255)])
        pasteAuthor = TextField('Author', [validators.Length(min=0, max=255)])
        pasteLanguage = SelectField('Syntax Highlighting', choices=languagesList, default='text', validators=[validators.Required()])
        pasteExpire = SelectField('Expire On', choices=expireTimes, validators=[validators.Required()])
        pasteRaw = TextField('Raw Text', [validators.Required()])
        pasteEncryption = RadioField('Paste Encryption', choices=encryptionMethods)

    def pasteExists(uri):
        old_uris_count = request.dbsession.query(Pastes).filter_by(pasteURI=uri).count()
        if old_uris_count > 0:
            return True
        return False

    def generateURI(len):
        allchar = string.ascii_letters + string.digits
        uri = "".join(choice(allchar) for x in range(len))
        return uri
    print(datetime.datetime.utcnow())
    form = createPaste(request.POST)
    if request.method == 'POST':
        if form.validate():
            #print(form.pasteRaw.data)
            newPaste = Pastes()
            URI = generateURI(6)
            while pasteExists(URI):
                URI = generateURI(6)
            newPaste.pasteURI = URI
            newPaste.title = form.pasteTitle.data
            newPaste.name = form.pasteAuthor.data
            newPaste.lang = form.pasteLanguage.data
            newPaste.text = form.pasteRaw.data
            if form.pasteExpire.data != "0":
                newPaste.toexpire = True
                newPaste.expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(form.pasteExpire.data))
            newPaste.encryption = form.pasteEncryption.data
            request.dbsession.add(newPaste)
        else:
            print("not valid :|")
            print(form.errors)
    return {'form': form}

@view_config(route_name='test', renderer='templates/paste.jinja2')
def test(request):
    uri = request.matchdict['pasteID']
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=uri).first()
    return {'paste': paste}
