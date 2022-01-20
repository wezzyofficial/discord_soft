from engine.functions.loader import read_handlers
from engine.functions.configs import load_config_file
from engine.functions.requests import processing_commands


class DSManager:
    def __init__(self, args: list):
        self.__config = load_config_file()

        self.__args = args
        self.arg = self.__args[1] if len(args) == 2 else 'client'

        self.read_commands = read_handlers(program_type='manager')

        processing_commands(command_name=self.arg)