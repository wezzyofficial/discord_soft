from engine import console
import pathlib, platform, os
from engine.functions import handler
from engine.models.client import Chats
from engine.functions.configs import load_chat_config_file, save_chat_config_file


def add_server_cmd(chats_list: list):
    pathlib_path = pathlib.Path(__file__).parent.parent.parent.parent

    full_path = f'{pathlib_path}/data_client/chat_'
    if platform.system() == 'Windows':
        full_path = f'{pathlib_path}\\data_client\\chat_'

    console.log(text='(Client / add_server) укажите ссылку на Discord-сервер?:')
    chat_link = input('')

    console.log(text='(Client / add_server) Создаю файлы для работы..')

    chats_exits = [chat['name'].split('_')[1] for chat in chats_list]
    if len(chats_exits) > 0:
        chats_exits.sort()

    new_num = 0
    for num, chat in enumerate(chats_list, start=1):
        if f'{num}' not in chats_exits:
            new_num = num

    if new_num == 0:
        new_num = len(chats_list) + 1

    new_chat_path = f'{full_path}{new_num}'
    if os.path.isdir(new_chat_path) is False:
        os.mkdir(new_chat_path)

        avatars_path = f'{new_chat_path}/avatars'
        if platform.system() == 'Windows':
            avatars_path = f'{new_chat_path}\\avatars'

        os.mkdir(avatars_path)

        accounts_path = f'{new_chat_path}/accounts.txt'
        if platform.system() == 'Windows':
            accounts_path = f'{new_chat_path}\\accounts.txt'

        with open(accounts_path, mode='a'):
            pass

        accounts_bad_path = f'{new_chat_path}/accounts_bad.txt'
        if platform.system() == 'Windows':
            accounts_bad_path = f'{new_chat_path}\\accounts_bad.txt'

        with open(accounts_bad_path, mode='a'):
            pass

        nicks_path = f'{new_chat_path}/nicks.txt'
        if platform.system() == 'Windows':
            nicks_path = f'{new_chat_path}\\nicks.txt'

        with open(nicks_path, mode='a'):
            pass

        nicks_path = f'{new_chat_path}/proxys.txt'
        if platform.system() == 'Windows':
            nicks_path = f'{new_chat_path}\\proxys.txt'

        with open(nicks_path, mode='a'):
            pass

    console.log(text='(Client / add_server) Обновляю конфиг чатов..')

    chats_list.append({
        'name': f'chat_{new_num}',
        'link': chat_link
    })

    save_chat_config_file(program_type='client', chats_data=chats_list)

    console.log(text=f'(Client / add_server / chat_{new_num}) Кеширую в базу этот чат..\n')
    if Chats.select().where(Chats.name == f'chat_{new_num}', Chats.link == chat_link).count() == 0:
        Chats.create(name=f'chat_{new_num}', link=chat_link)


    return add_server_cmd(chats_list=chats_list)


@handler.arg(name='add_server', description='Добавить Discord-сервер (клиент).')
def _():
    chat_config = load_chat_config_file(program_type='client')
    chats_list = chat_config['chats']

    add_server_cmd(chats_list=chats_list)