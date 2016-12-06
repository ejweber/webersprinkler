from threading import Thread
from sched import scheduler
import time

def background_tasks():
    schedule.run()

sprinkler_events = {'A': None, 'B': None, 'C': None}

schedule = scheduler(time.time, time.sleep)
sprinkler_events['A'] = schedule.enter(10, 1, print, argument=('first',))
sprinkler_events['B'] = schedule.enter(20, 1, print, argument=('second',))

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
        for name, event in sprinkler_events.items():
            print(event)
            if event != None:
                schedule.cancel(event)

    if 'cancel' in command:
        program_letter = command[-1]
        print('Canceling ' + program_letter)
        schedule.cancel(sprinkler_events[program_letter])
        sprinkler_events[program_letter] = None

background.join()

                    
