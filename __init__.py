import main
import time


def show(name):
    print(f'HELLO {name}')

def greeting(): 
    print('how are you?')


main.every().hour.at(':58').do(show, name = 'javad')


while True:
    main.run_pending()
    time.sleep(1)