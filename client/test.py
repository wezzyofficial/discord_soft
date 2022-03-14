import threading, time


def print_console():
    num = 1
    while True:
        num += 1
        print(f'\rCompleted: {num}', end='\n')
        time.sleep(1)


def input_console():
    test = input('')
    if test != '':
        print('пошел нвахнвахнвахнвахнвахнвах')

    return input_console()


thr1 = threading.Thread(target=print_console)
thr1.start()

thr2 = threading.Thread(target=input_console)
thr2.start()