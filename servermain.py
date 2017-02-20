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
from sprinklersystem import SprinklerSystem
from sprinklerschedule import SprinklerSchedule
from tcpserver import TCPServer
from threading import Thread
import time

if __name__ == '__main__':
    try:
        sprinklers = SprinklerSystem()
        background = SprinklerSchedule(sprinklers)
        background_thread = Thread(target=background.run)
        TCP_thread = Thread(target=TCPServer, args=(sprinklers, background))
        background_thread.start()
        TCP_thread.start()
        background_thread.join()
        TCP_thread.join()
    except:
        print('')
        background.shutdown()
        #sprinklers.cleanup()
        
    
    
