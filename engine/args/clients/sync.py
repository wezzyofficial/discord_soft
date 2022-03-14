import requests
from engine import console
from engine.functions import handler
from engine.functions.configs import load_chat_config_file
from engine.models.client import Chats, Accounts, Avatars, Nicks, Proxys
from engine.functions.client.caches import update_servers, update_accounts, update_avatars, update_nicks, update_proxys


@handler.arg(name='sync_client', description='Полная синхронизация.')
def _():
    chat_config = load_chat_config_file(program_type='client')
    chats_list = chat_config.get('chats', [])

    if len(chats_list) > 0:
        # chats_list = chat_config['chats']
        # update_servers(chats_list=chats_list)
        #
        # chats_data = [chat for chat in Chats.select()]
        #
        # update_accounts(chats_list=chats_data)
        # update_avatars(chats_list=chats_data)
        # update_nicks(chats_list=chats_data)
        # update_proxys(chats_list=chats_data)

        json_data = {}
        chats_db = Chats.select()
        for chat in chats_db:
            accounts_list = [{'login': account.login, 'password': account.password, 'token': account.token}
                             for account in Accounts.select().where(Accounts.chat == chat)]

            avatars_list = [{'name': avatars.name, 'hash': avatars.hash}
                            for avatars in Avatars.select().where(Avatars.chat == chat)]

            nicks_list = [{'name': nick.name} for nick in Nicks.select().where(Nicks.chat == chat)]

            proxys_list = [{'login': proxy.login, 'password': proxy.password, 'ip': proxy.ip, 'port': proxy.port,
                            'p_type': proxy.p_type} for proxy in Proxys.select().where(Proxys.chat == chat)]

            json_data[chat.name] = {
                'settings': {
                    'link': chat.link,
                    'status': chat.status,
                    'captcha': chat.captcha,
                    'reaction': chat.reaction
                },
                'data': {
                    'accounts': accounts_list,
                    'avatars': avatars_list,
                    'nicks': nicks_list,
                    'proxys': proxys_list
                }
            }

            print(json_data)
            break
    else:
        console.log(text=f'(Client / sync_client_full) Нет данных о серверах! Синхронизация не удалась..')