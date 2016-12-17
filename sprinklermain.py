# webersprinkler version 1.0
#
# webersprinkler is an amateur attempt to build an irrigation controller out of
# a Raspberry Pi 3 and a Sainsmart 8 channel relay. It is programmed entirely in
# Python (3.4.2) using only the Python standard library installed by default
# with Raspbian.

# In this version, interactions with webersprinkler rely fully on a command line
# interface. A main input loop runs constantly in the 'foreground' thread,
# waiting to accept user queries or commands. A 'background' thread runs in the
# background and uses a scheduler (from the sched module) to wait for scheduled
# times and activate the relay.

# In this version, it is intended for webersprinkler to run constantly on a
# Raspberry Pi 3 located wherever valve wires are accessible and connected to
# local wireless. Interactions with the Raspberry Pi 3 are intended to occur
# over SSH. This functionality has not been tested.

from threading import Thread
from sched import scheduler
from sprinklerdata import *
from sprinklercontrol import prepare_relay

# create global scheduler and background thread for scheduler
schedule = scheduler(time.time, time.sleep)
background = Thread(target=schedule.run)

# main program executable
def main():
    prepare_relay()
    programs = load_programs()
    schedule_stored_datetimes(programs, schedule)
    queue_check(schedule)
    background.start()
    input_loop(programs)
    
# loop that runs indefintely in the foreground, accepting user input
def input_loop(programs):
    stop = False
    while stop == False:
        command = input('\nThe scheduler is running. Type a command: ')
        if command == 'hello':
            help_command()
        elif command == 'queue':    
            display_queue(schedule)
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
            
# print out list of commands that can be run
def help_command():
    command_list = ('\n'
                    'queue: list the events currently in the scheduler queue\n'
                    'display []: display information for program [letter] '
                    'or all programs\n'
                    'valves []: update valve times for [letter]\n'
                    'schedule []: schedule new time for program [letter]\n'
                    'stop: cancel all programs in queue and stop scheduler'
                    '\n'
                    )
    print(command_list)

# excecute main
main()
