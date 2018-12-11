from modules.ExampleApi.ExampleApi_resource import ExampleApiResource

routes = [
    # ExampleApi api routes
    {'url': '/v1/example-api', 'controller': ExampleApiResource()},
    {'url': '/v1/example-api/{uid}', 'controller': ExampleApiResource()}
]
