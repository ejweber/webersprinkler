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
import pickle, time
from sprinklersystem import SprinklerSystem, SprinklerProgram
from threading import Thread, Event
from sched import scheduler
from tcpserver import TCPSprinklerServer

# globally accesible schedule
schedule = scheduler(time.time, time.sleep)

# global sprinkler system
sprinklers = SprinklerSystem()

# global control thread identifier
control = None
            

                           


if __name__ == '__main__':
    sprinklers.prepare_relay()
    Thread(target=TCPSprinklerServer, args=(sprinklers, running, control)).start()
    time.sleep(5000)
    '''
    background = Thread(target=schedule.run)
    queue_check()
    schedule_stored_datetimes()
    background.start()
    clear_queue(True)
    s.close()
    sprinklers.cleanup()
    '''
    
