from pyramid.response import Response
from pyramid.view import view_config
from beepaste.langs import languagesList
from beepaste.models.pastes import Pastes

import string
#import unicode
from random import *

import datetime
import colander
import deform
from deform.exception import ValidationFailure

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    class createPaste(colander.Schema):
        expireTimes = (
            (0, 'Keep Forever'),
            (300, '5 Minutes'),
            (3600, '1 Hour'),
            (86400, '1 Day'),
            (604800, '1 Week')
        )
        encryptionMethods = (
            ('no', 'No Encryption'),
            ('passwd', 'Encrypt with Password'),
            ('pgp', 'Encrypt with PGP Keys')
        )
        pasteTitle = colander.SchemaNode(colander.String(), title="Title")
        pasteAuthor = colander.SchemaNode(colander.String(), title="Author")
        pasteLanguage = colander.SchemaNode(colander.String(), default="text", widget=deform.widget.SelectWidget(values=languagesList), Title="Languages")
        pasteExpire = colander.SchemaNode(colander.String(), default=-1, widget=deform.widget.SelectWidget(values=expireTimes), Title="Expire On")
        pasteRaw = colander.SchemaNode(colander.Integer(), widget=deform.widget.HiddenWidget())
        encryption = colander.SchemaNode(colander.String(), validator=colander.OneOf([x[0] for x in encryptionMethods]), widget=deform.widget.RadioChoiceWidget(values=encryptionMethods), title='Encryption')
        #encryption = colander.SchemaNode(colander.String(), widget=deform.widget.RadioChoiceWidget(values=encryptionMethods), title='Encryption')


    class MainSchema(colander.MappingSchema):
        createpaste = createPaste(title='pasteForm')

    def validator(node, appstruct):
        return True

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

    schema = MainSchema(validator=validator)
    schema = schema.bind(request=request)
    form = deform.Form(schema, use_ajax=False, action=request.route_url('home'))
    form.buttons.append(deform.Button(name='submitBtn', title='Create Paste!'))


    if request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except ValidationFailure as e:
            #appstruct = None
            print('error')
            return {'error' : e}
            appstruct = None;
        if appstruct:
            pasteURI = generateURI()
            while pasteExists(pasteURI):
                pasteURI = generateURI()
            newPaste = Pastes()
            newPaste.pasteURI = pasteURI
            if appstruct['createpaste']['pasteTitle']:
                newPaste.title = appstruct['createpaste']['pasteTitle']
            else:
                newPaste.title = 'Untitled Paste'
            if appstruct['createpaste']['pasteAuthor']:
                newPaste.name = appstruct['createpaste']['pasteAuthor']
            else:
                newPaste.name = "Anonymous"
            newPaste.lang = appstruct['createpaste']['pasteLanguage']
            newPaste.text = appstruct['createpaste']['pasteRaw']
            if appstruct['createpaste']['pasteExpire'] != "0":
                newpaste.toexpire = 1
                newpaste.expire = datetime.datetime.utcnow + int(appstruct['createpaste']['pasteExpire'])
            newPaste.encryption = appstruct['createpaste']['encryption']
            newPaste.save()

            return HTTPFound(location='/view/raw/' + pasteURI, headers=headers)
    return {'form': form}
