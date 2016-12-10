from threading import Thread
from sched import scheduler
import time
from sprinklerdata import *

# create global variables
schedule = scheduler(time.time, time.sleep)
queue = {}
background = Thread(target=schedule.run())

# main program executable
def main():
    programs = load_programs()
    schedule_stored_datetimes(programs, schedule, queue)
    background.start()
    input_loop(programs)
    
# loop that runs indefintely in the foreground, accepting user input
def input_loop(programs):
    stop = False
    while stop == False:
        command = input('The scheduler is running. Type a command: ')
        if command == help:
            help_command()
        elif command == 'queue':    
            for event in schedule.queue:
                temp_time = time.localtime(event.time)
                print(event.argument, time.strftime('%A %H:%M', temp_time))
        elif 'valves' in command:
            display_times(programs, command[-1], 'valve')
            modify_programs(programs, command[-1])
        elif 'display' in command:
            display_times(programs, command[-1])
        elif 'schedule' in command:
            display_times(programs, command[-1], 'run')
            normalize_input_datetime(programs, command[-1])
        elif command == 'stop':
            stop = True
            for program, event_list in queue.items():
                for event in event_list:
                    schedule.cancel(event)
        elif 'cancel' in command:
            program_letter = command[-1]
            print('Canceling ' + program_letter)
            schedule.cancel(sprinkler_events[program_letter])
            sprinkler_events[program_letter] = None
        # DEBUG
        elif command == 'test':
            schedule_stored_datetimes(programs, schedule, queue)

# print out list of commands that can be run
def help_command():
    command_list = ('queue: list the events currently in the queue\n'
                    'cancel []: cancel program indicated by included letter\n'
                    'stop: cancel all programs in queue and stop scheduler'
                    )
    print(command_list)

# excecute main
main()
