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
        pasteLanguage = SelectField('Syntax Highlighting', choices=languagesList, default='text')
        pasteExpire = SelectField('Expire On', choices=expireTimes)
        pasteRaw = TextField('Raw Text', [validators.Required()])
        pasteEncryption = RadioField('Paste Encryption', choices=encryptionMethods)

    def generateURI():
        min_char = 6
        max_char = 6
        allchar = string.ascii_letters + string.digits
        password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        return password

    def pasteExists(uri):
        old_uris_count = request.dbsession.query(Pastes).filter_by(pasteURI=uri).count()
        if old_uris_count > 0:
            return True
        return False

    form = createPaste(request.POST)
    if request.method == 'POST':
        if form.validate():
            print('form validated!')
        else:
            print("not valid :|")
            print(form.errors)
    return {'form': form}
