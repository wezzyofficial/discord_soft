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


def processing_args(arg_str: str):
    """Функция "processing_commands" - обрабатывает аргументы от Менеджера."""

    for arg in handler.args:
        if arg.name.lower() == arg_str:
            return arg.handle()
    else:
        error_text = '(MANAGER): такого аргумента нет!\n'
        args_list = [[arg.name, arg.description] for arg in handler.args]

        if len(args_list) > 0:
            error_text += '\nДоступные аргументы:'
            for arg in args_list:
                error_text += f'\n{arg[0]} - {arg[1]}'

        error_text += '\n\n* Проверьте правильность написанного аргумента и повторите попытку..'
        console.error(text=error_text)


def processing_commands(command_str: str, first_start: bool):
    """Функция "processing_commands" - обрабатывает аргументы от Менеджера."""

    if command_str == 'menu':
        first_start = True
        command_str = '0'

    if command_str.isdigit():
        for command in handler.commands:
            if command.name.lower() == command_str:
                console.log(text=f'(Client): Инициализация процесса "{command.description}"..')

                command.handle()

                console.log(text=f'(Client): Процесс "{command.description}" выполнен!\n')

                return processing_commands(command_str='0', first_start=True)
        else:
            if first_start is False:
                console.log(text='(CLIENT) Такой команды нет!\n')

            commands_list = [[command.name, command.description] for command in handler.commands]

            if len(commands_list) > 0:
                console.log(text='(Client) Доступные команды:')
                for num, command in enumerate(commands_list, start=1):
                    console.log(text=f'(Client) {command[0]}. {command[1]}')

            if len(commands_list) > 0:
                console.log(text='(Client) Выберите интересующий вас вариант:')
            else:
                console.log(text='(Client) Команд сейчас нет!')

            if len(commands_list) > 0:
                try:
                    command_str = input()
                except:
                    command_str = None

                if command_str is not None:
                    if command_str == '':
                        command_str = '0'

                    return processing_commands(command_str=command_str, first_start=False)
                else:
                    console.log('(Client) Пункт меню должен быть целым числом, повторите попытку еще раз..\n')
                    return processing_commands(command_str='0', first_start=True)
    else:
        console.log('(Client) Пункт меню должен быть целым числом, повторите попытку еще раз..\n')
        return processing_commands(command_str='0', first_start=True)