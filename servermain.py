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
from tgapp import HTTPServer
from urllib.request import urlopen 

if __name__ == '__main__':
    try:
        sprinklers = SprinklerSystem()
        background = SprinklerSchedule(sprinklers)
        background_thread = Thread(target=background.run)
        tcp_thread = Thread(target=TCPServer, args=(sprinklers, background))
        http_thread = Thread(target=HTTPServer, args=(sprinklers, background))
        background_thread.start()
        tcp_thread.start()
        http_thread.start()
        while not background.shutdown_flag.is_set():
          pass
        urlopen('http://68.102.39.123:5001/shutdown')
        background_thread.join()
        tcp_thread.join()
    except:
        print('')
        background.shutdown()
        
    
    
