from sched import scheduler
from threading import Thread, Event
import time

class SprinklerSchedule(scheduler):
    def __init__(self, sprinklers):
        scheduler.__init__(self, time.time, time.sleep)
        self.sprinklers = sprinklers
        self.running = Event()
        self.shutdown_flag = Event()
        self.control = None
        self.queue_check()
        self.schedule_stored_datetimes()
        
    # calculate the time until each event should run next using 'normalized' times
    # remove old events from schedule and add new ones
    def schedule_stored_datetimes(self):
        self.clear_queue()
        for program in [self.sprinklers.A, self.sprinklers.B, self.sprinklers.C]:
            for time in program.next_times():
                self.enter(time, 1, self.program_task,
                               argument=(program,))
    
    # actual task to be run by scheduler
    # run progam and update queue so program runs again in a week
    def program_task(self, program):
        if not self.running.is_set():
            self.running.set()
            self.control = Thread(target=program.run, args=(self.running,))
            self.control.start()
        else:
            print('Scheduled program deferred to manual program.')
        self.schedule_stored_datetimes()
                           
    # create schedule event that refreshes every five seconds
    # ensures new events added to queue will run
    # otherwise scheduler waits for current event to run before checking queue
    def queue_check(self):
        check = self.enter(5, 2, self.queue_check)
    
    # set shutdown flag and fully clear queue so that background thread can stop
    def shutdown(self):
        self.running.clear()
        self.control.join()
        self.sprinklers.cleanup()
        self.shutdown_flag.set()
        self.clear_queue()
    
    # clear queue of scheduled events
    def clear_queue(self):
        # clear only sprinkler programs if schedule will persist
        if not self.shutdown_flag.is_set():
            for event in self.queue:
                if event.priority != 2:
                    self.cancel(event)
        # clear queue_check too so that background process can stop
        else:
            for event in self.queue:
                self.cancel(event)
            
    # return a list of events, each a named tuple with letter and time attributes
    def return_queue(self):
        queue = []
        for event in self.queue:
            # exclude queue_check (to avoid confusing users)
            if event.priority == 1:
                letter = event.argument[0].letter
                time = event.time
                queue.append((letter, time))
        return queue
