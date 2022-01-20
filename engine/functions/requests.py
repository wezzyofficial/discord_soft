import json
from engine.web_server import handler


async def processing_request(web, request, token, post=False):
    route = request.path
    headers = request.headers
    query_args = request.rel_url.query

    if route is not None or route != '':
        route_path = route.lower()
        path_args = route_path.split('/')
        processed_name = ''.join(path_args)

        request_data = await request.text()
        try:
            json_data = json.loads(request_data)
        except:
            json_data = None

        for route in handler.routes:
            route_path_correct = False
            if route.with_args:
                if len(path_args) > 0:
                    if path_args[0] == '':
                        path_args.remove('')

                    if path_args[0] == route.name:
                        route_path_correct = True
            else:
                if route.name == processed_name:
                    route_path_correct = True

            if route_path_correct:
                try:
                    return await route.handle(web=web, db=None, request=request, query_args=query_args, path_args=path_args,
                                              json_data=json_data, headers=headers, token=token, post=post)
                except:
                    return web.json_response({'status': False, 'type': 'error', 'text': '500: Server error'})
        else:
            return web.json_response({'status': False, 'type': 'error', 'text': '404: Not found'})
    else:
        return web.json_response({'status': False, 'type': 'error', 'text': '404: Not found'})