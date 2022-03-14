from engine import console
from engine.functions import handler
from engine.web_server import WebServer


@handler.arg(name='server', description='Запускаем процесс "сервер" (на сервере).')
def _():
    console.log('(MANAGER): Инициализация процесса "сервер"..')

    WebServer()