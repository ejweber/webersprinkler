# webersprinkler textclient version 1.0

# textclient is an adaptation of the original webersprinkler script, which ran
# as a single process accessible via SSH and 'screen.' Programs can be modified,
# and sprinkler programs and individual zones can be run via command line
# interface.

# Commands that modifiy programs load and modifify saved_programs.p directly and
# then communicate to the server so that it will load in the most recent
# changes. Manual commands are sent directly to the server for execution.

# globally accessible network variables
host = '192.168.1.3'
port = 5000

import socket, time, pickle

# loop that runs indefintely in the foreground, accepting user input
def input_loop():
    stop = False
    while stop == False:
        command = input("Type 'help' for a list of commands. Type a command: ")
        if command == 'help':
            help_command()
        elif command == 'queue':    
            display_queue()
        elif 'valves' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                letter = command[-1]
                display_times(letter, 'valve')
                new_times = modify_programs()
                response = communicate(('valves', letter, new_times))
                print(response)
                display_times(letter, 'valve')
            else:
                print('Proper syntax: valves [A,B,C]')
        elif 'display' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                letter = command[-1]
                display_times(letter)
            else:
                print('Proper syntax: display [A,B,C]')
        elif 'schedule' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                letter = command[-1]
                display_times(letter, 'run')
                new_time = input('Enter weekday and time for program to run: ')
                split_input = tuple(new_time.split(' '))
                response = communicate(('schedule', letter) + split_input)
                print(response)
                display_times(letter, 'run')   
            else:
                print('Proper syntax: schedule [A,B,C]')
        elif command == 'stop':
            stop_sprinklers()
        elif 'clear' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                letter = command[-1]
                confirm = input('Type yes to clear schedule for program ' + 
                                  letter + ': ')
                if confirm == 'yes':
                    response = communicate(('clear', letter))
                    print(response)
            else:
                print('Proper syntax: clear [A, B, C]')
        elif command == 'manual':
            manual_mode()
        elif command == 'exit':
            break
        # REMOVE FROM FINAL BUILD
        elif command == 'test':
            response = communicate('test')
            print(response)
            
# allow user to specify single program or zone to run immediately
def manual_mode():
    while True:
        command = input("Enter 'program [A,B,C]' or 'zone [1-5] [time]' "
                        "or 'done': ")
        command = command.split(' ')
        # allow for single program to run
        if 'program' in command:
            letter = command[1]
            if letter in 'ABC':
                print('Instructing the server to run program ' + letter + 
                       '...')    
                response = communicate(('run', 'program', letter))
                print(response)
            else:
                print('Proper syntax: program [A, B, C]')
        # allow for single zone to run
        if 'zone' in command:
            number = command[1]
            run_time = command[2]
            run_seconds = str(int(run_time) * 60)
            print('Instructing server to run zone ' + number + ' for ' 
                   + run_time + ' minutes...')
            response = communicate(('run', 'zone', number, run_seconds))
            print(response)
        # allow user to cancel program if necessary
        if 'stop' in command:
            stop_sprinklers()
        # break from manual input loop
        if 'done' in command:
            break

# attempt to stop currently running program
def stop_sprinklers():
    print('Requesting that the server stop...')
    response = communicate('stop')
    print(response)
    
# display valve and/or run times for programs A, B, or C
def display_times(letter, option='all'):
    response = communicate(('display', letter))
    valve_times = response['valve_times']
    run_times = response['run_times']
    # display valve times
    if option == 'all' or option == 'valve':
        number = 1
        print('Valve times:')
        if valve_times == []:
            print('  No valve times')
        for valve in valve_times:
            print('  Valve ' + str(number) + ': ' + '{0:g}'.format(valve / 60))
            number += 1
    # display run times
    if option == 'all' or option == 'run':
        print('Run times:')
        if run_times == []:
            print('  No run times')
        for run_time in run_times:
            print('  ' + run_time)
            
# prompt user for input regarding valve times
def modify_programs():
    new_times = []
    for zone in range(1, 6):
        time = input('Enter a time (in minutes) for zone ' + str(zone) + ': ')
        new_times.append(int(time) * 60)
    return new_times
            
# display list of events currently in server queue
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

# send message to server and recieve response
def communicate(message):
        s = socket.socket()   
        s.connect((host, port))
        s.send(pickle.dumps(message))
        response = pickle.loads(s.recv(1024))
        if not response:
            return 'The server did not respond.'
        else:
            return response
            
# print out list of commands that can be run
def help_command():
    command_list = ('help: display list of commands\n'
                    'queue: list the events currently in the scheduler queue\n'
                    'display []: display information for program [A,B,C]\n'
                    'valves []: update valve times for program [A,B,C]\n'
                    'schedule []: schedule new time for program [A,B,C]\n'
                    'stop: stop running program or zone\n'
                    'clear []: clear all run times for program [A,B,C]\n'
                    'manual: enter manual mode to run a program or zone now'
                    )
    print(command_list)
    
if __name__ == '__main__':
    input_loop()
