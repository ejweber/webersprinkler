import sched, time, datetime

# example of using a the scheduler to priortize tasks
def print_delayed_times():
    background = sched.scheduler(time.time, time.sleep)
    print(time.time())
    background.enter(10, 1, print, argument=('last',))
    background.enter(5, 2, print, argument=('middle',))
    background.enter(5, 1, print, argument=('first',))
    background.run()

# example of using a scheduler to start tasks at specific times
def print_time():
    t = time.ctime()
    print(t)

def print_absolute_times():
    background = sched.scheduler(time.time, time.sleep)
    time1 = datetime.datetime.now().timestamp()
    time2 = time1 + 5
    time3 = time1 + 10
    background.enterabs(time2, 1, print_time)
    background.enterabs(time3, 1, print_time)
    print(time.ctime())
    background.run()

print_absolute_times()
