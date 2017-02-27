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
        #pasteTitle = colander.SchemaNode(colander.String(), title="Title")
        pasteTitle = TextField('Title', [validators.Length(min=0, max=255)])
        #pasteAuthor = colander.SchemaNode(colander.String(), title="Author")
        pasteAuthor = TextField('Author', [validators.Length(min=0, max=255)])
        #pasteLanguage = colander.SchemaNode(colander.String(), default="text", widget=deform.widget.SelectWidget(values=languagesList), Title="Languages")
        pasteLanguage = SelectField('Syntax Highlighting', choices=languagesList)
        #pasteExpire = colander.SchemaNode(colander.String(), default=-1, widget=deform.widget.SelectWidget(values=expireTimes), Title="Expire On")
        pasteExpire = SelectField('Expire On', choices=expireTimes)
        #pasteRaw = colander.SchemaNode(colander.Integer(), widget=deform.widget.HiddenWidget())
        pasteRaw = TextField('Raw Text', [validators.Required()])
        #encryption = colander.SchemaNode(colander.String(), validator=colander.OneOf([x[0] for x in encryptionMethods]), widget=deform.widget.RadioChoiceWidget(values=encryptionMethods), title='Encryption')
        pasteEncryption = RadioField('Paste Encryption', choices=encryptionMethods)

    def generateURI():
        min_char = 6
        max_char = 6
        allchar = string.ascii_letters + string.digits
        password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        return password

    def pasteExists(uri):
        old_uris = Pastes.objects(pasteURI=uri)
        if old_uris:
            return True
        return False

    form = createPaste(request.POST)

    if request.method == 'POST':
        if form.validate():
            print('form validated!')
        else:
            print("not valid :|")
            
    return {'form': form}
