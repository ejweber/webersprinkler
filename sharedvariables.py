from sprinklerdata import *
from sched import scheduler
import time
from threading import Thread

# create global sprinkler programs
A = SprinklerProgram('A')
B = SprinklerProgram('B')
C = SprinklerProgram('C')

# create global variables
schedule = scheduler(time.time, time.sleep)
queue = {'A': [], 'B': [], 'C': []}
background = Thread(target=schedule.run())
