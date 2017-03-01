def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/') # TODO: add csrf
    config.add_route('about', '/about')
    config.add_route('test', '/test/{pasteID}')
    config.add_route('qrcode', '/qrcode/{uri}')
    config.add_route('view_raw', '/view/raw/{pasteID}')
    config.add_route('view_embed', '/view/embed/{pasteID}')
    config.add_route('view_paste', '/view/{pasteID}')
    config.add_route('register', '/users/register') # register, forgotpassword, signin, signout
    config.add_route('forgot', '/users/forgot') # register, forgotpassword, signin, signout
    config.add_route('signin', '/users/signin') # register, forgotpassword, signin, signout
    config.add_route('signout', '/users/signout') # register, forgotpassword, signin, signout
    config.add_route('reset_password', '/users/reset/{resetToken}')
    config.add_route('schedeuled_remove', '/cron/{cronkey}')
    config.add_route('api_create', '/api/create/{apiID}') # gets post method!
    config.add_route('api_get', '/api/view/{pasteID}') # returns json data!
    config.add_route('api_langs', '/api/langs') # returns supported langs in json
    config.add_route('api', '/api') # returns supported langs in json
