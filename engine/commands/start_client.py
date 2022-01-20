from engine import console
from engine.functions import handler


@handler.command(name='client', description='Запускаем процесс "клиент".')
def _():
    console.log('(MANAGER): Инициализация процесса "клиент"..')