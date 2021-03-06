import traceback, sys


class Route:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name'].lower()
        self.__handler = kwargs['handler']

        self.auth = kwargs['auth']
        self.post = kwargs['post']

        self.with_args = kwargs['with_args']


    async def handle(self, web, db, request, query_args, path_args, json_data, headers, token, post):
        """Функция "handle" - помогает в обработке полученного запроса и отлова ошибок."""
        request_token = headers.get('Authorization', None)

        try:
            if self.post and post is False:
                return web.json_response({'status': False, 'type': 'error', 'text': '405: Method Not Allowed'})

            if self.auth:
                if token != request_token:
                    return web.json_response({'status': False, 'type': 'error', 'text': '403: Forbiden (Invalid API Key!)'})

            return await self.__handler(web=web, db=db, request=request, query_args=query_args, path_args=path_args,
                                        json_data=json_data)
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(ex, traceback.format_tb(tb))
            return None


class Arg:
    def __init__(self, **kwargs):
        if not kwargs.keys() & {'name', 'handler', 'admin'}:
            raise Exception('Not enough arguments to create command object')
        self.name = kwargs['name'].lower()
        self.description = kwargs['description']

        self.__handler = kwargs['handler']

        self.with_args = kwargs['with_args']


    def handle(self):
        """Функция "handle" - помогает в обработке аргументов "Manager" и отлова ошибок."""

        try:
            self.__handler()
            return True
        except Exception:
            ex_type, ex, tb = sys.exc_info()
            print(ex, traceback.format_tb(tb))
            return False