# globally accessible variables
host = '127.0.0.1'
port = 5000

import socket, time, pickle
from sprinklerdata import *

# loop that runs indefintely in the foreground, accepting user input
def input_loop(programs):
    stop = False
    while stop == False:
        command = input("Type 'help' for a list of commands. Type a command: ")
        if command == 'help':
            help_command()
        elif command == 'queue':    
            display_queue()
        elif 'valves' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                display_times(programs, command[-1], 'valve')
                modify_programs(programs, command[-1])
                response = communicate('change')
                print(response)
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
                response = communicate('change')
                print(response)
                display_times(programs, command[-1], 'run')    
            else:
                print('Proper syntax: schedule [A,B,C]')
        elif command == 'stop':
            stop_sprinklers()
        elif 'clear' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                display_times(programs, command[-1], 'run')
                clear_program(programs, command[-1])
                response = communicate('change')
                print(response)
            else:
                print('Proper syntax: clear [A, B, C]')
        elif command == 'manual':
            manual_mode(programs)
            
# allow user to specify single program or zone to run immediately
def manual_mode(programs):
    while True:
        command = input("Enter 'program [A,B,C]' or 'zone [1-5] [time]' "
                        "or 'done': ")
        command = command.split(' ')
        # allow for single program to run
        if 'program' in command:
            letter = command[1]
            if letter in 'ABC':
                if programs[letter].valve_times == []:
                    print('Valve times not set for program ' + letter + '.')
                else:
                    print('Instructing server to run program ' + letter + '...')    
                    response = communicate('run program ' + letter)
                    print(response)
                    # allow user to cancel program if necessary
            else:
                print('Proper syntax: program [A, B, C]')
        # allow for single zone to run
        if 'zone' in command:
            split_command = command.split(' ')
            zone = split_command[1]
            run_time = split_command[2]
            try:
                print('Running zone ' + zone + ' for ' + run_time + ' minutes'
                       '...')
                print('Use ^C to cancel if necessary') 
                run_manual(int(zone), int(run_time) * 60)
            except KeyboardInterrupt:
                print('\nZone ' + str(zone) + ' canceled.')
                emergency_stop()
        if 'stop' in command:
            stop_sprinklers()
        if 'done' in command:
            break

# attempt to stop currently running program
def stop_sprinklers():
    print('Requesting that the server stop...')
    response = communicate('stop')
    print(response)
            
# display list of events currently in queue
def display_queue():
    queue = communicate('queue')
    if 'server' in queue:
        print(queue)
        return
    for event in queue:
        # display program letter and absolute time
        event_time = event[1]
        temp_time = time.localtime(event_time)
        letter = event[0]
        print('Program', letter, '-', time.strftime('%A %H:%M', temp_time))
        # calculate time until execution and display
        difference = int(event_time - time.time())
        extra_hours = difference % 86400
        days = int((difference - extra_hours) / 86400)
        extra_minutes = extra_hours % 3600
        hours = int((extra_hours - extra_minutes) / 3600)
        extra_seconds = extra_minutes % 60
        minutes = int((extra_minutes - extra_seconds) / 60)
        print('  -', days, 'days,', hours, 'hours,', minutes, 'minutes')

def communicate(message):
        message = message.split(' ')
        s = socket.socket()   
        s.connect((host, port))
        s.send(pickle.dumps(message))
        response = pickle.loads(s.recv(1024))
        if not response:
            return 'The server did not respond.'
        else:
            return response
    
if __name__ == '__main__':
    programs = load_programs()
    input_loop(programs)
