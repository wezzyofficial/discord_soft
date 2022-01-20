import sys
from engine import console
from engine.web_server.app import WebServer


def main(args: list):
    arg = 'client'
    if len(args) == 2:
        arg = args[1].lower()

    if arg == 'client':
        console.log_na(text='(MANAGER) › Инициализация процесса "client"!')
    elif arg == 'server' or arg == 'tasker':
        console.log_na(text=f'(MANAGER) › Инициализация процесса "{arg}"!')

        WebServer(program_type=arg)
    else:
        console.error_na(text='(MANAGER) › Неверный аргумент, доступные аргументы: client / server / tasker')


if __name__ == "__main__":
    main(args=sys.argv)