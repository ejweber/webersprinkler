from threading import Thread
from sched import scheduler
import time
from sprinklerdata import *

# create global variables
schedule = scheduler(time.time, time.sleep)
sprinkler_events = {'A': None, 'B': None, 'C': None}
background = Thread(target=schedule.run())

# main program executable
def main():
    load_programs()
    load_events()
    background.start()
    input_loop()
    
# loop that runs indefintely in the foreground, accepting user input
def input_loop():
    stop = False
    while stop == False:
        command = input('The scheduler is running. Type a command: ')
        if command == help:
            help_command()
        elif command == 'queue':    
            for event in schedule.queue:
                print(event.time, event.argument)
        elif 'modify' in command:
            modify_programs(command[-1])
        elif 'display' in command:
            display_valve_times(command[-1])
        elif command == 'stop':
            stop = True
            for name, event in sprinkler_events.items():
                if event != None:
                    schedule.cancel(event)
        elif 'cancel' in command:
            program_letter = command[-1]
            print('Canceling ' + program_letter)
            schedule.cancel(sprinkler_events[program_letter])
            sprinkler_events[program_letter] = None

# print out list of commands that can be run
def help_command():
    command_list = ('queue: list the events currently in the queue\n'
                    'cancel []: cancel program indicated by included letter\n'
                    'stop: cancel all programs in queue and stop scheduler'
                    )
    print(command_list)

# initiate dictionary and fill with upcoming events
# TODO - make this function general
def load_events():
    sprinkler_events['A'] = schedule.enter(10, 1, print, argument=('first',))
    sprinkler_events['B'] = schedule.enter(20, 1, print, argument=('second',))

# excecute main
main()
