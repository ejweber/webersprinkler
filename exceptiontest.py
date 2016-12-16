from sched import scheduler

def test(number):
    print('Number', number)

schedule = scheduler()
A = schedule.enter(5, 1, test, (1,))
B = schedule.enter(30, 1, test, (2,))

try:
    schedule.run()
except KeyboardInterrupt:
    schedule.cancel(A)
    schedule.cancel(B)
    print('failed')
