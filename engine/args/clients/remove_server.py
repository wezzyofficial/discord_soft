from engine import console
import pathlib, platform, os, shutil
from engine.functions import handler
from engine.models.client import Accounts, Chats, Avatars, Nicks, Proxys
from engine.functions.configs import load_chat_config_file, save_chat_config_file


def server_number_processed(chats_list: list):
    console.log(text='(Client / remove_server) * Укажите номер сервера который необходимо удалить:')

    server_num = input()
    if server_num.isdigit():
        server_num = int(server_num)
        count_servers = len(chats_list)
        if server_num > 0 and server_num <= count_servers:
            return chats_list[server_num - 1]
        else:
            console.log(text=f'(Client / remove_server) Номер Discord-сервера должен быть больше 0 и меньше '
                             f'{count_servers}! Повторите попытку..')
            return server_number_processed(chats_list=chats_list)
    else:
        console.log(text='(Client / remove_server) Номер Discord-сервера должен быть целым числом, повторите попытку..')
        return server_number_processed(chats_list=chats_list)


def server_delete(chats_list: list):
    if len(chats_list) > 0:
        console.log(text='(Client / remove_server) Какой Discord-сервер будем удалять?')

        for num, chat in enumerate(chats_list, start=1):
            name, link = chat['name'], chat['link']
            console.log(text=f'(Client / remove_server) {num}. {name} ({link})')

        console.log(text='(Client / remove_server) * Все данные из указанного сервера будут удалены без возвратно..')

        snp = server_number_processed(chats_list=chats_list)
        server_name = snp['name']
        server_link = snp['link']

        console.log(text=f'(Client / remove_server / {server_name}) Чищу информацию..')
        pathlib_path = pathlib.Path(__file__).parent.parent.parent.parent

        full_path = f'{pathlib_path}/data_client/'
        if platform.system() == 'Windows':
            full_path = f'{pathlib_path}\\data_client\\'

        server_path = f'{full_path}{server_name}'
        if os.path.isdir(server_path):
            shutil.rmtree(server_path)

        if snp in chats_list:
            chats_list.remove(snp)

        save_chat_config_file(program_type='client', chats_data=chats_list)

        console.log(text=f'(Client / remove_server / {server_name}) Обновляю кеш всей базы данных!')

        chats_data_db = Chats.select().where(Chats.name == server_name, Chats.link == server_link)
        if chats_data_db.count() > 0:
            chats_data_db = chats_data_db.get()

            for a_c in Accounts.select().where(Accounts.chat == chats_data_db):
                a_c.delete_instance()

            for a_c in Avatars.select().where(Avatars.chat == chats_data_db):
                a_c.delete_instance()

            for n_c in Nicks.select().where(Nicks.chat == chats_data_db):
                n_c.delete_instance()

            for p_c in Proxys.select().where(Proxys.chat == chats_data_db):
                p_c.delete_instance()

            chats_data_db.delete_instance()

        console.log(text=f'(Client / remove_server / {server_name}) Информация удалена, кэш базы почищен, конфиг обновлен!\n')

        return server_delete(chats_list=chats_list)
    else:
        console.log(text='(Client / remove_server) Discord-серверов нет!')


@handler.arg(name='remove_server', description='Удалить Discord-сервер (клиент).')
def _():
    chat_config = load_chat_config_file(program_type='client')
    chats_list = chat_config['chats']

    server_delete(chats_list=chats_list)