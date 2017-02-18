# serverdaemon version 1.0

# serverdaemon is intended to be run entirely in the background of the
# Raspberry Pi 3 on which webersprinkler is implemented. It listens for specific
# commands via a network socket and controls the actions of the Sainsmart 8 
# channel relay as appopriate.

# A main loop listens on the socket, while the scheduler runs in the background
# to wait for scheduled times to activate the relay. When it is time to run
# a sprinkler program, either because of the schedule or manual network command, 
# serverdaemon runs the program in another separate thread. This thread
# constantly listens for the command to terminate early and will do so if 
# necessary.

# The current version outputs recieved commands to standard output. Future
# versions will output to a log file.

# import necessary modules
import socket, pickle, time
from sprinklersystem import SprinklerSystem, SprinklerProgram
from threading import Thread, Event
from sched import scheduler

# globally accessible network variables
host = '192.168.1.3'
port = 5000

# globally accesible schedule
schedule = scheduler(time.time, time.sleep)

# global sprinkler control flag
running = Event()

# global sprinkler system
sprinklers = SprinklerSystem()

# global control thread identifier
control = None

# set up and return socket
def server_setup():
    global host, port
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    
# analyze recieved command and execute necessary function
def parse(data):
    if 'run' in data:
        global control
        r_string = ''
        if running.is_set():
            r_string = ('The controller was already running and had to be '
                        'stopped.\n')
            running.clear()
            control.join()
        if 'program' in data:
            letter = data[2]
            programmed_valves = len(sprinklers.programs[letter].valve_times)
            if programmed_valves == 0:
                r_string = (r_string + 'No valve times have been set for '
                            'program ' + letter + '.')
                return r_string
            running.set()
            control = Thread(target=sprinklers.programs[letter].run, 
                             args=(running,))
            control.start()
            r_string = (r_string + 'The server has agreed to run program ' +
                        letter + '.')
            return r_string
        if 'zone' in data:
            zone = int(data[2])
            run_time = int(data[3])
            run_minutes = str(int(run_time / 60))
            if not running.is_set():
                running.set()
                control = Thread(target=sprinklers.run_zone, args=(zone, 
                                 run_time, running))
                control.start()
                r_string = (r_string + 'The server has agreed to run zone ' + 
                            str(zone) + ' for ' + run_minutes + ' minutes.')
                return r_string
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
    if 'display' in data:
        letter = data[1]
        information = {'valve_times': sprinklers.programs[letter].valve_times,
                       'run_times': sprinklers.programs[letter].list_times()
                      }
        return information
    if 'valves' in data:
        letter = data[1]
        new_times = data[2]
        sprinklers.programs[letter].valve_times = new_times
        sprinklers.save()
        return 'The server has made the change.'
    if 'schedule' in data:
        letter = data[1]
        new_time = (data[2], data[3])
        sprinklers.programs[letter].store_time(new_time)
        schedule_stored_datetimes()
        sprinklers.save()
        return 'The server has made the change.'
    if 'clear' in data:
        letter = data[1]
        sprinklers.programs[letter].valve_times = []
        sprinklers.programs[letter].run_times = []
        return 'The server has made the change.'
            
# calculate the time until each event should run next using 'normalized' times
# remove old events from schedule and add new ones
def schedule_stored_datetimes():
    clear_queue()
    for program in [sprinklers.A, sprinklers.B, sprinklers.C]:
        for time in program.next_times():
            schedule.enter(time, 1, program_task,
                           argument=(program,))
                           
# actual task to be run by scheduler
# run progam and update queue so program runs again in a week
def program_task(program):
    if not running.is_set():
        running.set()
        control = Thread(target=program.run, args=(running,))
        control.start()
    else:
        print('unable to run program')
    schedule_stored_datetimes()
                           
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
            letter = event.argument[0].letter
            time = event.time
            queue.append((letter, time))
    return queue
        
if __name__ == '__main__':
    sprinklers.prepare_relay()
    s = server_setup()
    background = Thread(target=schedule.run)
    queue_check()
    schedule_stored_datetimes()
    background.start()
    try:
        while True:
            c, data = info_recieve(s)
            response = parse(data)
            info_send (c, response)
    except KeyboardInterrupt:
        print('')
        pass
    clear_queue(True)
    s.close()
    sprinklers.cleanup()
    
