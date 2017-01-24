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
# over SSH. 'screen' is a program which can be installed on the Pi to keep the
# sprinkler program running in a virtual terminal to be accessed from any
# terminal window.

# import necessary modules
from threading import Thread
from sched import scheduler
from sprinklerdata import *
from sprinklercontrol import prepare_relay, run_program

# create global scheduler and background thread for scheduler
schedule = scheduler(time.time, time.sleep)
background = Thread(target=schedule.run)

# main program executable
# prepare GPIO pins on relay, load programs (if possible), fill schedule queue
# with loaded programs, start schedule running in background, start input loop
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
        print('The scheduler is running in the background.')
        command = input("Type 'help' for a list of commands. Type a command: ")
        if command == 'help':
            help_command()
        elif command == 'queue':    
            display_queue(schedule)
        elif 'valves' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                display_times(programs, command[-1], 'valve')
                modify_programs(programs, command[-1])
            else:
                print('Proper syntax: valves [A,B,C]')
        elif 'display' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                display_times(programs, command[-1])
            else:
                print('Proper syntax: display [A,B,C]')
        elif 'schedule' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                display_times(programs, command[-1], 'run')
                normalize_input_datetime(programs, command[-1])
                schedule_stored_datetimes(programs, schedule)
                display_times(programs, command[-1], 'run')    
            else:
                print('Proper syntax: schedule [A,B,C]')
        elif command == 'stop':
            print('The scheduler is closing. Please wait up to five seconds...')
            cleanup()
            stop = True
            clear_queue(schedule, True)
            background.join()
            print('Shutdown complete.')
        elif 'clear' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                display_times(programs, command[-1], 'run')
                clear_program(programs, command[-1])
                schedule_stored_datetimes(programs, schedule)
            else:
                print('Proper syntax: clear [A, B, C]')
        elif command == 'manual':
            clear_queue(schedule)
            manual_mode(programs)
            schedule_stored_datetimes(programs, schedule)

# print out list of commands that can be run
def help_command():
    command_list = ('help: display list of commands\n'
                    'queue: list the events currently in the scheduler queue\n'
                    'display []: display information for program [A,B,C]\n'
                    'valves []: update valve times for program [A,B,C]\n'
                    'schedule []: schedule new time for program [A,B,C]\n'
                    'stop: cancel all programs in queue and stop scheduler\n'
                    'clear []: clear all run times for program [A,B,C]\n'
                    'manual: enter manual mode to run a program or zone now'
                    )
    print(command_list)

# excecute main
main()
