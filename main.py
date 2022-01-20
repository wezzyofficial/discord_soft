import sys
from engine.manager import DSManager


def main(args: list):
    """Функция "main" - для инициализации менеджера команд."""
    DSManager(args=args)


if __name__ == "__main__":
    main(args=sys.argv)