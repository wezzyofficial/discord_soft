from engine.web_server.assets import Route


routes = ([])


def route(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                routes.append(Route(name=cmd, handler=handler,
                                    auth=(kwargs['auth'] if 'auth' in kwargs else False),
                                    post=(kwargs['post'] if 'post' in kwargs else False),
                                    with_args=(kwargs['with_args'] if 'with_args' in kwargs else False)))
        else:
            return False

    return with_args