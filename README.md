# webersprinkler

webersprinkler is an amateur attempt to build an irrigation controller out of a Raspberry Pi 2 and a Sainsmart 8 channel relay. It is programmed entirely in Python (3.4.2) using only the Python standard library installed by default with Raspbian.

In this version, control over the relay is relegated to a daemon running in the background of the Raspberry Pi. This allows for the creation of multiple interfaces. Each interface can communicate with the server and request that programs be run, but ultimately a single script has control over the relay.

servermain.py
servermain.py is the primary thread to be run on the Raspberry Pi. It initializes the relay that controls the sprinklers, starts a background scheduling thread, a thread to respond to TCP requests, and a thread to respond to HTTP requests. servermain.py should be run in the background using the following terminal command: nohup python3 servermain.py > log.txt & (nohup overrides the exit signal upon terminal exit, > log.txt pipes output to a log file, and & allows servermain.py to run in the background). servermain.py can be safely shutdown from either existing client using the "shutdown" command.

sprinklersystem.py
sprinklersystem.py is the only module intended to take direct control over the GPIO pins on the Raspberry Pi. It defines a SprinklerSystem class using information about how the various zones and pump are connected to the relay and a SprinklerProgram class that remembers times and dates for each zone. Instantiating a SprinkleSystem object also creates three associated SprinklerProgram object. A SprinklerProgram object is passed between all threads running in servermain.py and its methods are used to control the relay.