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

schedule.enter(10, 1, relay_test)
schedule.enter(20, 1, relay_test)

background = Thread(target=schedule.run)

background.start()

#while True:
#    try:
#        time.sleep(1)
#    except KeyboardInterrupt:
#        input('input loop: ')

while True:
    why = input('input loop: ')
    print(schedule.queue)
