from threading import Thread, Lock, active_count
from sched import scheduler
import time
from sprinklercontrol import *

def schedule_task():
    #print(active_count())
    schedule.run()

def task(number):
    print('Task ' + str(number) + ' Completed')

schedule = scheduler(time.time, time.sleep)
inputlock = Lock()

prepare_relay()

schedule.enter(60, 1, relay_test)
schedule.enter(70, 1, relay_test)

background = Thread(target=schedule.run)

background.start()

for event in schedule.queue:
    schedule.cancel(event)
print(schedule.queue)
background.join()
