# import necessary modules
import socket, pickle
from sprinklercontrol import *
from sprinklerdata import *
from threading import Thread
from sched import scheduler

# globally accessible variables
host = '127.0.0.1'
port = 5000

# globally accesible schedule
schedule = scheduler(time.time, time.sleep)

# set up and return socket
def server_setup():
    global host, port
    s = socket.socket()
    s.bind((host, port))
    return s
    
# block until daemon recieves instructions and output as a string
def recieve(s):
    s.listen(1)
    print('listening for instructions')
    c, addr = s.accept()
    data = pickle.loads(c.recv(1024))
    print(str(addr) + ' sent '+ str(data))
    c.send('instructions recieved by server'.encode('utf-8'))
    c.close()
    return data
    
def parse(data, programs):
    if 'run' in data:
        if 'program' in data:
            letter = data[2]
            run_program(programs, letter)
        if 'zone' in data:
            zone = int(data[2])
            time = int(data[3])
            run_manual(zone, time)
    if 'change' in data:
        programs = load_programs()
        schedule_stored_datetimes(programs, schedule)
    if 'queue' in data:
        display_queue()
            
# calculate the time until each event should run next using 'normalized' times
# remove old events from schedule and add new ones
def schedule_stored_datetimes(programs, schedule):
    now = normalize_current_datetime()
    clear_queue(schedule)
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
def program_task(programs, letter, schedule):
    run_program(programs, letter)
    schedule_stored_datetimes(programs, schedule)
                           
# create schedule event that refreshes every five seconds
# ensures new events added to queue will run
# otherwise scheduler waits for current event to run before checking queue
def queue_check():
    check = schedule.enter(5, 2, queue_check)
    
# clear queue of scheduled events
def clear_queue(schedule, stop_scheduler=False):
    # clear only sprinkler programs if schedule will persist
    if stop_scheduler == False:
        for event in schedule.queue:
            if event.priority != 2:
                schedule.cancel(event)
    # clear queue_check too so that background process can stop
    if stop_scheduler == True:
        for event in schedule.queue:
            schedule.cancel(event)
            
# display list of events currently in queue
def display_queue():
    print(schedule.queue)
    for event in schedule.queue:
        # exclude queue_check (to avoid confusing users)
        if event.priority == 1:
            # display program letter and absolute time
            temp_time = time.localtime(event.time)
            letter = event.argument[1]
            print('Program', letter, '-', time.strftime('%A %H:%M', temp_time))
            # calculate time until execution and display
            difference = int(event.time - time.time())
            extra_hours = difference % 86400
            days = int((difference - extra_hours) / 86400)
            extra_minutes = extra_hours % 3600
            hours = int((extra_hours - extra_minutes) / 3600)
            extra_seconds = extra_minutes % 60
            minutes = int((extra_minutes - extra_seconds) / 60)
            print('  -', days, 'days,', hours, 'hours,', minutes, 'minutes')
        
if __name__ == '__main__':
    prepare_relay()
    s = server_setup()
    programs = load_programs()
    background = Thread(target=schedule.run)
    queue_check()
    schedule_stored_datetimes(programs, schedule)
    background.start()
    while True:
        data = recieve(s)
        parse(data, programs)
    s.close()
    cleanup()
    
