from engine import console
import os, pathlib, platform, hashlib
from engine.models.client import Accounts, Chats, Avatars, Nicks, Proxys


def md5_hash(file):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def update_servers(chats_list: list):
    chats_processed_list = []
    console.log(text=f'(Client / updating_servers) Начинаю обработку {len(chats_list)} discord сервер-ов!')
    for chat in chats_list:
        name, link = chat.get('name', ''), chat.get('link', '')
        status, captcha, reaction = chat.get('status', False), chat.get('captcha', ''), chat.get('reaction', '')

        chat_data = Chats.select().where(Chats.name == name, Chats.link == link, Chats.status == status,
                                         Chats.captcha == captcha, Chats.reaction == reaction)
        if chat_data.count() == 0:
            chat_data = Chats.create(name=name, link=link, status=status, captcha=captcha, reaction=reaction)
            console.log(text=f'(Client / updating_servers) Сервер "{chat_data.name}" - создан!')

        chats_processed_list.append([name, link, status, captcha, reaction])

    console.log(text=f'(Client / updating_servers) Обработано {len(chats_processed_list)} discord-сервер-ов!')

    chats_data_db = Chats.select()
    if chats_data_db.count() > 0:
        file_exists = False
        console.log(text=f'(Client / updating_servers) Синхронизирую базу аккаунтов с реальностью..')
        for c_db in chats_data_db:
            for cpl in chats_processed_list:
                if ((c_db.name == cpl[0] and c_db.link == cpl[1]) and (c_db.status == cpl[2] and c_db.captcha == cpl[3])) and c_db.reaction == cpl[4]:
                    file_exists = True

            if file_exists is False:
                c_db.delete_instance()

        chats_processed_list.clear()
        console.log(text=f'(Client / updating_servers) Синхронизация базы аккаунтов с реальностью - выполнена!')


def update_accounts(chats_list: list):
    console.log(text=f'(Client / update_accounts) Начинаю обработку аккаунтов с {len(chats_list)} discord сервер-ов!')
    pathlib_path = pathlib.Path(__file__).parent.parent.parent.parent

    path_symb = '/'
    if platform.system() == 'Windows':
        path_symb = '\\'

    accounts_list = []
    for chat in chats_list:
        full_path = f'{pathlib_path}{path_symb}data_client{path_symb}{chat.name}{path_symb}accounts.txt'
        if os.path.exists(full_path):
            try:
                with open(f'{pathlib_path}{path_symb}data_client{path_symb}{chat.name}{path_symb}accounts.txt') as file:
                    accounts_file = file.read().splitlines()
            except:
                accounts_file = None

            if accounts_file is not None:
                for account in accounts_file:
                    accounts_file_data = account.split(':')
                    if len(accounts_file_data) == 3:
                        login, password, token = accounts_file_data[0], accounts_file_data[1], accounts_file_data[2]

                        account_data = Accounts.select().where(Accounts.login == login, Accounts.password == password,
                                                               Accounts.token == token, Accounts.chat == chat)

                        if account_data.count() == 0:
                            account_data = Accounts.create(login=login, password=password, token=token, chat=chat)
                            console.log(text=f'(Client / update_accounts / {chat.name}) Аккаунт "{account_data.login}'
                                             f':{account_data.password}:{account_data.token}" - создана!')

                        accounts_list.append(account)
                    else:
                        console.error(text=f'(Client / update_accounts / {chat.name}) Аккаунт "{account}" указан в не праваильном формате..')
            else:
                console.error(text=f'(Client / update_accounts / {chat.name}) Не удалось прочитать файл с аккауантами!')
        else:
            console.error(text=f'(Client / update_accounts / {chat.name}) Обработать аккаунты с {chat.name} discord сервера не удалось '
                               f'- отсутствует файл с аккаунтами!')

        accounts_data_db = Accounts.select().where(Accounts.chat == chat)
        if accounts_data_db.count() > 0:
            console.log(text=f'(Client / update_accounts / {chat.name}) Синхронизирую базу аккаунтов с реальностью..')
            for a_db in accounts_data_db:
                db_account = f'{a_db.login}:{a_db.password}:{a_db.token}'
                if db_account not in accounts_list:
                    a_db.delete_instance()

            accounts_list.clear()
            console.log(text=f'(Client / update_accounts / {chat.name}) Синхронизация базы аккаунтов с реальностью - выполнена!')

    accounts_data = Accounts.select()
    console.log(text=f'(Client / update_accounts) Ников "{accounts_data.count()}" c "{len(chats_list)}" discord серверов - '
                     f'обработано!')


def update_avatars(chats_list: list):
    console.log(text=f'(Client / update_avatars) Начинаю обработку аватарок с {len(chats_list)} discord сервер-ов!')
    pathlib_path = pathlib.Path(__file__).parent.parent.parent.parent

    path_symb = '/'
    if platform.system() == 'Windows':
        path_symb = '\\'

    files_name_hash_data = []
    for chat in chats_list:
        full_path = f'{pathlib_path}{path_symb}data_client{path_symb}{chat.name}{path_symb}avatars'
        files = os.listdir(full_path)

        console.log(text=f'(Client / update_avatars) Сервер "{chat.name}" - обрабатываем {len(files)} шт аватарку(-ок/-ки)!')

        for file in files:
            try:
                with open(f'{full_path}{path_symb}{file}', "rb") as file_load:
                    try:
                        hash = md5_hash(file=file_load)
                    except:
                        hash = None

                    file_load.close()
                file_open = True
            except:
                file_open = None

            if file_open is not None:
                if hash is not None:
                    avatars_data = Avatars.select().where(Avatars.name == file, Avatars.hash == hash,
                                                          Avatars.chat == chat)
                    if avatars_data.count() == 0:
                        avatars_data = Avatars.create(name=file, hash=hash, chat=chat)
                        console.log(text=f'(Client / update_avatars / {chat.name}) Аватарка "{avatars_data.name}" - создана!')

                else:
                    console.error(text=f'(Client / update_avatars / {chat.name}) Не удалось получить хеш аватарки - "{file}"!')
            else:
                console.error(text=f'(Client / update_avatars / {chat.name}) Не удалось открыть аватарку - "{file}"!')

            files_name_hash_data.append([file, hash if hash is not None else '0'])

        console.log(text=f'(Client / update_avatars / {chat.name}) Аватарок "{len(files_name_hash_data)}" - обработано!')

        avatars_data_db = Avatars.select().where(Avatars.chat == chat)
        if avatars_data_db.count() > 0:
            console.log(text=f'(Client / update_avatars / {chat.name}) Синхронизирую базу аватарок с реальностью..')

            file_exists = False
            for a_db in avatars_data_db:
                for fnhd in files_name_hash_data:
                    if fnhd[0] == a_db.name and fnhd[1] == a_db.hash:
                        file_exists = True

                if file_exists is False:
                    a_db.delete_instance()

            files_name_hash_data.clear()
            console.log(text=f'(Client / update_avatars / {chat.name}) Синхронизация базы аватарок с реальностью - '
                             f'выполнена!')

    avatars_data = Avatars.select()
    console.log(text=f'(Client / update_avatars) Аватарок "{avatars_data.count()}" c "{len(chats_list)}" discord '
                     f'серверов - обработано!')


def update_nicks(chats_list: list):
    console.log(text=f'(Client / update_nicks) Начинаю обработку ников с {len(chats_list)} discord сервер-ов!')
    pathlib_path = pathlib.Path(__file__).parent.parent.parent.parent

    path_symb = '/'
    if platform.system() == 'Windows':
        path_symb = '\\'

    nicks_list = []
    for chat in chats_list:
        full_path = f'{pathlib_path}{path_symb}data_client{path_symb}{chat.name}{path_symb}nicks.txt'
        if os.path.exists(full_path):
            try:
                with open(f'{pathlib_path}{path_symb}data_client{path_symb}{chat.name}{path_symb}nicks.txt') as file:
                    nicks_file = file.read().splitlines()
            except:
                nicks_file = None

            if nicks_file is not None:
                for nick in nicks_file:
                    nick_data = Nicks.select().where(Nicks.name == nick, Nicks.chat == chat)

                    if nick_data.count() == 0:
                        nick_data = Nicks.create(name=nick, chat=chat)
                        console.log(text=f'(Client / update_nicks / {chat.name}) Ник "{nick_data.name}" - создан!')

                    nicks_list.append(nick)
            else:
                console.error(text=f'(Client / update_nicks / {chat.name}) Не удалось прочитать файл с никами!')
        else:
            console.error(text=f'(Client / update_nicks / {chat.name}) Обработать ники с {chat.name} discord сервера не удалось '
                               f'- отсутствует файл с никами!')

        nicks_data_db = Nicks.select().where(Nicks.chat == chat)
        if nicks_data_db.count() > 0:
            console.log(text=f'(Client / {chat.name}) Синхронизирую базу ников с реальностью..')
            for n_db in nicks_data_db:
                if n_db.name not in nicks_list:
                    n_db.delete_instance()

            nicks_list.clear()
            console.log(text=f'(Client / update_nicks / {chat.name}) Синхронизация базы ников с реальностью - выполнена!')

    nicks_data = Nicks.select()
    console.log(text=f'(Client / update_nicks) Ников "{nicks_data.count()}" c "{len(chats_list)}" discord серверов - обработано!')


def update_proxys(chats_list: list):
    console.log(text=f'(Client / update_proxys) Начинаю обработку прокси с {len(chats_list)} discord сервер-ов!')
    pathlib_path = pathlib.Path(__file__).parent.parent.parent.parent

    path_symb = '/'
    if platform.system() == 'Windows':
        path_symb = '\\'

    proxys_list = []
    for chat in chats_list:
        full_path = f'{pathlib_path}{path_symb}data_client{path_symb}{chat.name}{path_symb}proxys.txt'
        if os.path.exists(full_path):
            try:
                with open(f'{pathlib_path}{path_symb}data_client{path_symb}{chat.name}{path_symb}proxys.txt') as file:
                    proxys_file = file.read().splitlines()
            except:
                proxys_file = None

            if proxys_file is not None:
                for proxy in proxys_file:
                    proxy_file_data = proxy.split(':')
                    if len(proxy_file_data) == 3:
                        login, password, address, port, p_type = '', '', proxy_file_data[1], proxy_file_data[2], \
                                                                  proxy_file_data[0]
                        proxy_text = f'{proxy_file_data[0]}:{proxy_file_data[1]}:{proxy_file_data[2]}'
                        proxy_args = True
                    elif len(proxy_file_data) == 5:
                        login, password, address, port, p_type = proxy_file_data[1], proxy_file_data[2], \
                                                                 proxy_file_data[3], proxy_file_data[4], \
                                                                 proxy_file_data[0]

                        proxy_text = f'{proxy_file_data[0]}:{proxy_file_data[1]}:{proxy_file_data[2]}' \
                                     f':{proxy_file_data[3]}:{proxy_file_data[4]}'
                        proxy_args = True
                    else:
                        login, password, address, port, p_type = None, None, None, None, None
                        proxy_args = False
                        proxy_text = ''

                    if proxy_args:
                        if p_type in ['http', 'https']:
                            proxy_data = Proxys.select().where(Proxys.login == login, Proxys.password == password,
                                                               Proxys.ip == address, Proxys.port == port,
                                                               Proxys.chat == chat, Proxys.p_type == p_type)

                            if proxy_data.count() == 0:
                                Proxys.create(login=login, password=password, ip=address, port=port, chat=chat, p_type=p_type)
                                console.log(text=f'(Client / update_proxys / {chat.name}) Прокси "{proxy_text}" - создан!')

                            proxys_list.append(proxy_text)
                        else:
                            console.error(text=f'(Client / update_proxys / {chat.name}) Прокси "{proxy}" - не '
                                               f'поддерживается!')
                    else:
                        console.error(text=f'(Client / update_proxys / {chat.name}) Прокси "{proxy}" - в '
                                           f'неправильном формате!')
            else:
                console.error(text=f'(Client / update_proxys / {chat.name}) Не удалось прочитать файл с прокси!')
        else:
            console.error(text=f'(Client / update_proxys / {chat.name}) Обработать проски с {chat.name} discord сервера '
                               f'не удалось - отсутствует файл с прокси!')

        proxys_data_db = Proxys.select().where(Proxys.chat == chat)
        if proxys_data_db.count() > 0:
            console.log(text=f'(Client / update_proxys / {chat.name}) Синхронизирую базу прокси с реальностью..')
            for p_db in proxys_data_db:
                if p_db.login == '' or p_db.password == '':
                    proxy_text = f'{p_db.p_type}:{p_db.ip}:{p_db.port}'
                else:
                    proxy_text = f'{p_db.p_type}:{p_db.login}:{p_db.password}:{p_db.ip}:{p_db.port}'

                if proxy_text not in proxys_list or proxy_text not in proxys_list:
                    p_db.delete_instance()

            proxys_list.clear()

            console.log(text=f'(Client / update_proxys / {chat.name}) Синхронизация базы прокси с реальностью - выполнена!')

    proxy_data = Proxys.select()
    console.log(text=f'(Client / update_proxys) Прокси "{proxy_data.count()}" c "{len(chats_list)}" discord серверов - обработаны!')