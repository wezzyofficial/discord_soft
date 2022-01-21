from engine import console
from engine.functions import handler


@handler.arg(name='server', description='Запускаем процесс "сервер" (на сервере).')
def _():
    console.log('(MANAGER): Инициализация процесса "сервер"..')