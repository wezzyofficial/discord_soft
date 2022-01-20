from engine.web_server import handler


@handler.route(name='test', auth=True, with_args=False)
async def _(web, db, request, query_args, path_args, json_data):
    return web.json_response({'status': True, 'type': 'answer'})