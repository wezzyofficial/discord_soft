import json, secrets, os, pathlib, platform


def create_config_file(path: str):
    """Функция "create_config_file" - создает новый конфиг."""
    data = {
        'server_secret': secrets.token_urlsafe(12),
        'servers': []
    }

    with open(path, 'w', encoding='utf-8') as new_config:
        json.dump(data, new_config, indent=4)

    return data


def load_config_file():
    """Функция "load_config_file" - читает конфиг, если его нет - создает новый."""
    pathlib_path = pathlib.Path(__file__).parent.parent.parent
    path = f'{pathlib_path}/config.json'
    if platform.system() == 'Windows':
        path = f'{pathlib_path}\\config.json'

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as config_file:
            data = json.load(config_file)
    else:
        data = create_config_file(path=path)

    return data


def create_chat_config_file(path: str):
    """Функция "create_config_file" - создает новый конфиг."""
    data = {
        'chats': [{}]
    }

    with open(path, 'w', encoding='utf-8') as new_config:
        json.dump(data, new_config, indent=4)

    return data


def load_chat_config_file(program_type: str):
    """Функция "load_chat_config_file" - читает конфиг чатов, если его нет - создает новый."""
    pathlib_path = pathlib.Path(__file__).parent.parent.parent
    path = f'{pathlib_path}/data_{program_type}/chats.json'
    if platform.system() == 'Windows':
        path = f'{pathlib_path}\\data_{program_type}\\chats.json'

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as config_file:
            data = json.load(config_file)
    else:
        data = create_chat_config_file(path=path)

    return data


def save_chat_config_file(program_type: str, chats_data: list):
    """Функция "save_chat_config_file" - сохраняет конфиг чатов, если его нет - создает новый."""
    pathlib_path = pathlib.Path(__file__).parent.parent.parent
    path = f'{pathlib_path}/data_{program_type}/chats.json'
    if platform.system() == 'Windows':
        path = f'{pathlib_path}\\data_{program_type}\\chats.json'

    if os.path.exists(path):
        data = {
            'chats': chats_data
        }

        with open(path, 'w', encoding='utf-8') as new_config:
            json.dump(data, new_config, indent=4)

        return data
    else:
        data = create_chat_config_file(path=path)

    return data