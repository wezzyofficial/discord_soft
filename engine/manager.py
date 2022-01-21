from engine.functions.loader import read_handlers
from engine.functions.configs import load_config_file
from engine.functions.requests import processing_args, processing_commands


class DSManager:
    def __init__(self, args: list):
        self.__config = load_config_file()
        self.__args = args

        self.arg = None
        self.read_args = None
        self.read_commands = None

        if self.__args[0] == 'client_commands':
            self.read_commands = read_handlers(program_type='client_commands')
            processing_commands(command_str='menu', first_start=True)
        else:
            self.arg = self.__args[1] if len(args) == 2 else 'client'
            self.read_args = read_handlers(program_type='manager')
            processing_args(arg_str=self.arg)