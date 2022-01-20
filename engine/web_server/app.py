import asyncio
from aiohttp import web
from engine.web_server.loader import read_handlers
from engine.functions.configs import load_config_file
from engine.functions.requests import processing_request


class WebServer:
    def __init__(self, program_type='tasker'):
        self.__loop = asyncio.get_event_loop()

        self.program_type = program_type
        self.__config = load_config_file()
        self.__token = self.__config.get(f'{program_type}_secret', None)

        web.run_app(self.start())

    async def start(self):
        routes = web.RouteTableDef()
        read_handlers(program_type=self.program_type)

        @routes.get(path='/')
        async def _(request):
            return await processing_request(web=web, request=request, token=self.__token, post=False)

        @routes.post(path='/')
        async def _(request):
            return await processing_request(web=web, request=request, token=self.__token, post=True)

        @routes.get(path='/{data:.+}')
        async def _(request):
            return await processing_request(web=web, request=request, token=self.__token, post=False)

        @routes.post(path='/{data:.+}')
        async def _(request):
            return await processing_request(web=web, request=request, token=self.__token, post=True)

        app = web.Application()
        app.add_routes(routes)

        return app