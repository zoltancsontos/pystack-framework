from modules.Token.Token_resource import TokenResource

routes = [
    # Token api routes
    {'url': '/token', 'controller': TokenResource()},
    {'url': '/token/{uid}', 'controller': TokenResource()}
]
