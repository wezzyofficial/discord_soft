from engine import console
from engine.functions import handler
from engine.manager import DSManager


@handler.arg(name='client', description='Запускаем процесс "клиент".')
def _():
    console.log('(MANAGER): Инициализация процесса "клиент"..\n')
    DSManager(args=['client_commands'])