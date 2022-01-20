import json, secrets, os, pathlib, platform


def create_config_file(path: str):
    data = {
        'server_secret': secrets.token_urlsafe(12),
        'tasker_secret': secrets.token_urlsafe(12),
    }

    with open(path, 'w', encoding='utf-8') as new_config:
        json.dump(data, new_config, indent=4)

    return data

def load_config_file():
    pathlib_path = pathlib.Path(__file__).parent.parent.parent
    path = f'{pathlib_path}/config.json'
    if platform.system() == 'Windows':
        path = f'{pathlib_path}\\config.json'

    if os.path.exists(path):
        with open('config.json', 'r', encoding='utf-8') as config_file:
            data = json.load(config_file)
    else:
        data = create_config_file(path=path)

    return data