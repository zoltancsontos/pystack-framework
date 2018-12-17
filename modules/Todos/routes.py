from modules.Todos.Todos_resource import TodosResource

routes = [
    # Todos api routes
    {'url': '/v1/todos', 'controller': TodosResource()},
    {'url': '/v1/todos/{uid}', 'controller': TodosResource()}
]
