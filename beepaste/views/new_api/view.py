from pyramid.request import Request
from pyramid.view import view_config, view_defaults
import beepaste.pasteFunctions as func
from beepaste.models.api import API
import json


@view_defaults(route_name="new_api", renderer='json')
class NewAPI():
    def __init__(self, context, request:Request):
        self.request = request
        self.context = context

    @view_config(request_method="GET")
    def get_view(self):
        return {"method": "GET"}

    @view_config(request_method="POST")
    def post_view(self):
        return {"method": "POST"}

    @view_config(request_method="PUT")
    def put_view(self):
        return {"method": "PUT"}

    @view_config(request_method="DELETE")
    def delete_view(self):
        return {"method": "DELETE"}
