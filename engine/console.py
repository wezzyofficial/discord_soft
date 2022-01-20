import logging


file_log = logging.FileHandler('dsoft.log')
console_out = logging.StreamHandler()


logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s] [DISCORD BOT] %(message)s',
                    datefmt='%H:%M:%S, %m.%d.%Y',
                    level=logging.INFO)


def log(text):
    """Функция "log" - создает сообщение об информации."""
    logging.info(text)


def error(text):
    """Функция "error" - создает сообщение о ошибке."""
    logging.error(text)


def warning(text):
    """Функция "warning" - создает сообщение о предупреждение."""
    logging.warning(text)