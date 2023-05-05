import main
import time


def show(name):
    print(f'HELLO {name}')

def greeting(): 
    print('how are you?')


main.every().second.do(show, name = 'javad')
main.every(4).seconds.do(greeting)


while True:
    main.run_all(1)
    print(main.next_run())
    time.sleep(1)