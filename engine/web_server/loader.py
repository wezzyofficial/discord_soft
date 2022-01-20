import os, importlib, pathlib, platform


def read_handlers(program_type):
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