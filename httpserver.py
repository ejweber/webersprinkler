from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server
from sprinklercontrol import *
from sprinklerdata import *
from threading import Thread, Event
from sched import scheduler

# globally accesible schedule
schedule = scheduler(time.time, time.sleep)

# global sprinkler control flag
running = Event()

class RootController(TGController):
    @expose()
    def index(self):
        return 'Hello World'
    
    @expose('hello.xhtml')
    def hello(self, person=None):
        return dict(person=person)
        
    @expose()
    def runprogramA(self):
         if not running.is_set():
                running.set()
                control = Thread(target=run_program, args=(programs, 'A',
                                                           running))
                control.start()
                
    @expose()
    def stop(self):
        running.clear()

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
                           argument=(programs, program.letter))
                           
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
    run_program(programs, letter, running)
    schedule_stored_datetimes(programs)
                           
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
        
config = AppConfig(minimal=True, root_controller=RootController())
config.renderers = ['kajiki']
application = config.make_wsgi_app()

prepare_relay()
programs = load_programs()

print('Serving on port 8080...')
httpd = make_server('', 8080, application)
httpd.serve_forever()
