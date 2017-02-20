from sched import scheduler, Event
import time

class SprinklerSchedule(scheduler):
    def __init__(sprinklers):
        scheduler.__init__(time.time, time.sleep)
        self.sprinklers = sprinklers
        self.running = Event()
        self.control
        
    # calculate the time until each event should run next using 'normalized' times
    # remove old events from schedule and add new ones
    def schedule_stored_datetimes():
        self.clear_queue()
        for program in [self.sprinklers.A, self.sprinklers.B, self.sprinklers.C]:
            for time in program.next_times():
                schedule.enter(time, 1, program_task,
                               argument=(program,))
    
    # actual task to be run by scheduler
    # run progam and update queue so program runs again in a week
    def program_task(program):
        if not self.running.is_set():
            self.running.set()
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
