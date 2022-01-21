from engine import console


def menu():
    console.log(text='(Client) доступные варианты работы:')

    console.log('(Client) 1. Синхронизировать аккаунты')
    console.log('(Client) 2. Синхронизировать прокси')
    console.log('(Client) 3. Синхронизировать логи')
    console.log('(Client) 4. Наблюдать за процессом')
    console.log('(Client) 5. Настройки')

    console.log('(Client) Выберите интересующий вас вариант:')

    menu_value = input()
    if menu_value.isdigit():
        menu_value = int(menu_value)
        if menu_value == 1:
            console.log('(Client) Пошла жара..')
        else:
            console.error('(Client) Такого пункта меню нет, повторите попытку еще раз..')
            return menu()
    else:
        console.error('(Client) Пункт меню должен быть целым числом, повторите попытку еще раз..')
        return menu()


def main():
    menu()