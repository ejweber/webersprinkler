# import necessary modules
import socket, pickle
from sprinklercontrol import *
from sprinklerdata import *
from threading import Thread, Event
from sched import scheduler
import sys
from collections import namedtuple

# globally accessible network variables
host = '127.0.0.1'
port = 5000

# globally accesible schedule
schedule = scheduler(time.time, time.sleep)

# global sprinkler control flag
running = Event()

# set up and return socket
def server_setup():
    global host, port
    s = socket.socket()
    s.bind((host, port))
    return s
    
# block until daemon recieves instructions and output as a string
def info_recieve(s):
    s.listen(1)
    print('listening for instructions')
    c, addr = s.accept()
    data = pickle.loads(c.recv(1024))
    print(str(addr) + ' sent '+ str(data))
    return c, data
    
def info_send(c, response):
    c.send(pickle.dumps(response))
    c.close()
    
def parse(data, programs):
    if 'run' in data:
        if 'program' in data:
            letter = data[2]
            if not running.is_set():
                running.set()
                control = Thread(target=run_program, args=(programs, letter,
                                                           running))
                control.start()
                return 'The server has agreed to run program ' + letter + '.'
        if 'zone' in data:
            zone = int(data[2])
            time = int(data[3])
            run_manual(zone, time)
    if 'change' in data:
        programs = load_programs()
        schedule_stored_datetimes(programs)
        return 'The server is aware of the change.'
    if 'queue' in data:
        queue = return_queue()
        if not queue:
            queue = 'The server is not aware of any upcoming events.'
        return queue
    if 'stop' in data:
        if running.is_set():
            running.clear()
            return 'The server has agreed to stop the controller.'
        if not running.is_set():
            return 'The server reports that the controller was not running.'
        
            
# calculate the time until each event should run next using 'normalized' times
# remove old events from schedule and add new ones
def schedule_stored_datetimes(programs):
    now = normalize_current_datetime()
    clear_queue()
    for letter, program in programs.items():
        for normal_time in program.run_times:
            difference = normal_time - now
            if difference < timedelta():
                difference += timedelta(7)
            difference = difference.total_seconds()
            schedule.enter(difference, 1, program_task,
                           argument=(programs, program.letter, schedule))
                           
# actual task to be run by scheduler
# run progam and update queue so program runs again in a week
def program_task(programs, letter):
    if not running.is_set():
        running.set()
        control = Thread(target=run_program, args=(programs, letter,
                                                   running))
        control.start()
    else:
        print('unable to run scheduled program')
    run_program(programs, letter)
    schedule_stored_datetimes(programs, schedule)
                           
# create schedule event that refreshes every five seconds
# ensures new events added to queue will run
# otherwise scheduler waits for current event to run before checking queue
def queue_check():
    check = schedule.enter(5, 2, queue_check)
    
# clear queue of scheduled events
def clear_queue(stop_scheduler=False):
    # clear only sprinkler programs if schedule will persist
    if stop_scheduler == False:
        for event in schedule.queue:
            if event.priority != 2:
                schedule.cancel(event)
    # clear queue_check too so that background process can stop
    if stop_scheduler == True:
        for event in schedule.queue:
            schedule.cancel(event)
            
# return a list of events, each a named tuple with letter and time attributes
def return_queue():
    queue = []
    for event in schedule.queue:
        # exclude queue_check (to avoid confusing users)
        if event.priority == 1:
            letter = event.argument[1]
            time = event.time
            queue.append((letter, time))
    return queue
        
if __name__ == '__main__':
    prepare_relay()
    s = server_setup()
    programs = load_programs()
    background = Thread(target=schedule.run)
    queue_check()
    schedule_stored_datetimes(programs)
    background.start()
    try:
        while True:
            c, data = info_recieve(s)
            response = parse(data, programs)
            info_send (c, response)
    except KeyboardInterrupt:
        print('')
        pass
    clear_queue(True)
    s.close()
    cleanup()
    
