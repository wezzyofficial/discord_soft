import pathlib, platform
from peewee import SqliteDatabase


class DSDatabases:
    def __init__(self, program_type: str):
        self.program_type = program_type
        self.db_path = self.path_constructor()
        self.db = SqliteDatabase(self.db_path)


    def path_constructor(self):
        """Функция "path_constructor" - позволяет собрать путь до BD."""
        self.temp_path = pathlib.Path(__file__).parent.parent.parent

        path = f'{self.temp_path}/data_{self.program_type}/{self.program_type}.db'
        if platform.system() == 'Windows':
            path = f'{self.temp_path}\\data_{self.program_type}\\{self.program_type}.db'

        return path


    def init_db(self):
        """Функция "init_db" - возвращает объект базы данных."""
        return self.db