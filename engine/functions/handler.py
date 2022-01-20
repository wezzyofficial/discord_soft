from engine.functions.assets import Route, Command


routes, commands = ([], [],)


def route(**kwargs):
    """Функция "route" - используется как декоратор - хендлер."""
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


def command(**kwargs):
    """Функция "command" - используется как декоратор - хендлер."""
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            if not isinstance(kwargs['name'], list):
                kwargs['name'] = [kwargs['name']]
            for cmd in kwargs['name']:
                commands.append(Command(name=cmd, handler=handler,
                                        description=(kwargs['description'] if 'description' in kwargs else 'Нет описания')))
        else:
            return False

    return with_args