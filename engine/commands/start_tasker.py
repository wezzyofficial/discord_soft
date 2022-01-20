from engine import console
from engine.functions import handler
from engine.web_server import WebServer


@handler.command(name='tasker', description='Запускаем процесс "контроль задач" (на сервере).')
def _():
    console.log('(MANAGER): Инициализация процесса "контроль задач"..')

    WebServer()