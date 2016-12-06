from threading import Thread
from sched import scheduler
import time

def background_tasks():
    schedule.run()

schedule = scheduler(time.time, time.sleep)
A = schedule.enter(10, 1, print, argument=('first',))
B = schedule.enter(20, 1, print, argument=('second',))

background = Thread(target=background_tasks)
background.start()

stop = False
while(stop != True):

    command = input('The scheduler is running. Type a command: ')

    if command == 'help':
        print('queue: list the current queue of events')

    if command == 'queue':    
        for event in schedule.queue:
            print(event.time, event.argument)

    if command == 'stop':
        stop = True
        schedule.cancel(A)
        schedule.cancel(B)

    # does not work because 'A' is not the same thing as A
    # need to create a data structure that holds event name (A) and string for
    # user to type when cancelling 
    if 'cancel' in command:
        event = command[-1]
        print('Canceling ' + event)
        schedule.cancel(event)

background.join()

                    
