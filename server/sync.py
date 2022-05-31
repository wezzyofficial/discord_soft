from engine.functions import handler
from engine.models.server import Settings


@handler.route(name='sync', auth=True)
async def _(web, db, request, query_args, path_args, json_data):
    if json_data is not None:
        chats_list = json_data['chats'] if json_data.get('chats', None) is not None else []

        if len(chats_list) > 0:
            settings_data = Settings.select().where(Settings.uid == 1)
            if settings_data.count() > 0:
                settings_data = settings_data.get()
            else:
                settings_data = Settings.create(sync=True)

            settings_data.sync = True
            settings_data.save()

            for chat in chats_list:
                print(chat)
        else:
            return web.json_response({'status': False, 'type': 'error.sync.json_data', 'text': 'Chats: Data not request'})
    else:
        return web.json_response({'status': False, 'type': 'error.sync.json_data', 'text': 'JSON: Data not found'})
    
    # by wezzyofficial
