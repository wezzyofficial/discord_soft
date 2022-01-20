import logging


file_log = logging.FileHandler('dsoft.log')
console_out = logging.StreamHandler()


logging.basicConfig(handlers=(file_log, console_out),
                    format='[%(asctime)s | %(levelname)s] [DISCORD BOT] %(message)s',
                    datefmt='%H:%M:%S, %m.%d.%Y',
                    level=logging.INFO)


async def log(text):
    logging.info(text)


async def error(text):
    logging.error(text)


async def warning(text):
    logging.warning(text)


def log_na(text):
    logging.info(text)


def error_na(text):
    logging.error(text)


def warning_na(text):
    logging.warning(text)