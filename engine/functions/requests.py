import json
from engine import console
from engine.functions import handler


async def processing_request(web, request, token, post=False):
    """Функция "processing_request" - обрабатывает текущий запрос на Веб-сервер от клиента."""
    route_path = request.path
    headers = request.headers
    query_args = request.rel_url.query

    if route_path is not None or route_path != '':
        route_path = route_path.lower()
        path_args = route_path.split('/')
        processed_name = ''.join(path_args)

        request_data = await request.text()
        try:
            json_data = json.loads(request_data)
        except:
            json_data = None

        for route in handler.routes:
            route_path_correct = False
            if route.with_args:
                if len(path_args) > 0:
                    if path_args[0] == '':
                        path_args.remove('')

                    if path_args[0] == route.name:
                        route_path_correct = True
            else:
                if route.name == processed_name:
                    route_path_correct = True

            if route_path_correct:
                try:
                    return await route.handle(web=web, db=None, request=request, query_args=query_args, path_args=path_args,
                                              json_data=json_data, headers=headers, token=token, post=post)
                except:
                    return web.json_response({'status': False, 'type': 'error', 'text': '500: Server error'})
            else:
                return web.json_response({'status': False, 'type': 'error', 'text': '404: Not found'})
        else:
            return web.json_response({'status': False, 'type': 'error', 'text': '404: Not found'})
    else:
        return web.json_response({'status': False, 'type': 'error', 'text': '404: Not found'})


def processing_args(args):
    """Функция "processing_commands" - обрабатывает аргументы от Менеджера."""

    if len(args) == 0:
        args.append('menu')

    for arg in handler.args:
        args_path_correct = False
        if arg.with_args:
            if args[0] == arg.name:
                args_path_correct = True
        else:
            if arg.name == args[0]:
                args_path_correct = True

        if args_path_correct:
            return arg.handle()
    else:
        error_text = '(MANAGER): такого аргумента нет!\n'
        args_list = [[arg.name, arg.description] for arg in handler.args]

        if len(args_list) > 0:
            error_text += '\nДоступные аргументы:'
            for arg in args_list:
                error_text += f'\n{arg[0]} - {arg[1]}'

        error_text += '\n\n* Проверьте правильность написанного аргумента и повторите попытку..'
        error_text += '\n* Использование: python main.py [аргумент]'
        console.error(text=error_text)