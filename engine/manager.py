import pathlib, platform
from engine.functions.loader import read_handlers
from engine.functions.configs import load_config_file
from engine.functions.requests import processing_args


class DSManager:
    def __init__(self, args: list):
        self.__full_path = pathlib.Path(__file__).parent.parent
        self.__config = load_config_file()
        self.__args = args

        path = f'{self.__full_path}/main.py'
        if platform.system() == 'Windows':
            path = f'{self.__full_path}\\main.py'

        if path in self.__args:
            self.__args.remove(path)

        if 'main.py' in self.__args:
            self.__args.remove('main.py')

        self.read_handler_args = read_handlers(program_type='not_server')
        processing_args(args=self.__args)