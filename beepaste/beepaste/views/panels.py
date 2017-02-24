from pyramid_layout.panel import panel_config
from os.path import join
from ..models.users import Users

@panel_config(name='navbar', renderer='templates/panels/navbar.jinja2')
def navbar(context, request):
    return {}

@panel_config(name='footer', renderer='templates/panels/footer.jinja2')
def footer(context, request):

    with open(join(base, 'VERSION.txt')) as f:
        version = f.read()
    return {'version': version}


@panel_config(name='menu', renderer='templates/panels/menu.jinja2')
def menu(context, request):
    def nav_item(name, path, items=[]):
        active = any([item['active'] for item in items]) if items else request.path == path

        item = dict(
            name=name,
            path=path,
            active=active,
            items=items
            )

        return item

    items = []
    # items.append(nav_item('resume', '#', [nav_item(name, request.route_path(name)) for name in ['resume_list','resume_edit']]))
    items.append(nav_item('<i class="fa fa-plus-circle" aria-hidden="true"></i> Create Paste', request.route_path('home')))
    items.append(nav_item('<i class="fa fa-cogs" aria-hidden="true"></i> API', request.route_path('api')))
    items.append(nav_item('<i class="fa fa-info" aria-hidden="true"></i> About Us', request.route_path('about')))
    if not request.authenticated_userid:
        items.append(nav_item('<i class="fa fa-sign-in" aria-hidden="true"></i> Signin', request.route_path('signin')))
        items.append(nav_item('<i class="fa fa-pencil-square-o"></i> Signup', request.route_path('signout')))
    else:
        items.append(nav_item('Signout {}'.format(Users.objects(userID=request.authenticated_userid).first().username),
                              request.route_path('signout')) )

    return {'items': items}
