from threading import Thread, active_count, enumerate
from sched import scheduler
import time
from sprinklerdata import *
from sprinklercontrol import *

# create global variables
schedule = scheduler(time.time, time.sleep)
background = Thread(target=schedule.run)

def queue_check():
    check = schedule.enter(5, 2, queue_check)

# main program executable
def main():
    prepare_relay()
    programs = load_programs()
    schedule_stored_datetimes(programs, schedule)
    queue_check()
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
                print(event[2], time.strftime('%A %H:%M', temp_time))
                print(event.time, time.time())
                print(event.time - time.time())
        elif 'valves' in command:
            display_times(programs, command[-1], 'valve')
            modify_programs(programs, command[-1])
        elif 'display' in command:
            display_times(programs, command[-1])
        elif 'schedule' in command:
            display_times(programs, command[-1], 'run')
            normalize_input_datetime(programs, command[-1])
            schedule_stored_datetimes(programs, schedule)
        elif command == 'stop':
            cleanup()
            stop = True
            clear_queue(schedule, True)
            background.join()
        elif 'cancel' in command:
            program_letter = command[-1]
            print('Canceling ' + program_letter)
            schedule.cancel(sprinkler_events[program_letter])
            sprinkler_events[program_letter] = None
        # DEBUG
        elif command == 'test':
            schedule_stored_datetimes(programs, schedule)
# print out list of commands that can be run
def help_command():
    command_list = ('queue: list the events currently in the queue\n'
                    'cancel []: cancel program indicated by included letter\n'
                    'stop: cancel all programs in queue and stop scheduler'
                    )
    print(command_list)

# excecute main
main()
