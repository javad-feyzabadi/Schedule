import main
import time


def show(name):
    print(f'HELLO {name}')

def greeting(): 
    print('how are you?')


main.every(6).seconds.do(show, name = 'javad')
main.every(4).seconds.do(greeting)


while True:
    main.run_pending()
    print(main.idle_seconds())
    time.sleep(1)