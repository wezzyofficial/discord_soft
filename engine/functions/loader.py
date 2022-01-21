import os, importlib, pathlib, platform


def read_handlers(program_type):
    """Функция "read_handlers" - импортирует Python файлы в проект."""
    if program_type == 'manager':
        program_type = 'engine/args'
        if platform.system() == 'Windows':
            program_type = 'engine\\args'
    elif program_type == 'client_commands':
        program_type = 'engine/commands'
        if platform.system() == 'Windows':
            program_type = 'engine\\commands'

    pathlib_path = pathlib.Path(__file__).parent.parent.parent

    path = f'{pathlib_path}/{program_type}'
    if platform.system() == 'Windows':
        path = f'{pathlib_path}\\{program_type}'


    for root, dirs, files in os.walk(path):
        check_extension = filter(lambda x: x.endswith('.py'), files)
        for command in check_extension:
            path = os.path.join(root, command)
            spec = importlib.util.spec_from_file_location(command, os.path.abspath(path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)