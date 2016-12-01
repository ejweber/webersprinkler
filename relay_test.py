# webersprinkler version 0.1
#
# The purpose of this version is to test the basic ability to control various
# sprinkler zones with Python code.
#
# The Sainsmart 8 channel relay used for this project is reversed. For this
# version of the code, GPIO.HIGH turns the relay off and GPIO.LOW turns the
# relay on. This behavior may change in future versions of the code, as the
# system could be wired in such a way that a circuit would connect in the off
# state and disconnect in the on state.

# import modules
import RPi.GPIO as GPIO
import time

# set GPIO mode
GPIO.setmode(GPIO.BCM)

# map pump and pin numbers to commonly understood zone names
pump = 9
zones = {1: 10, 2:22, 3:27, 4:17, 5:4, 6:3, 7:2}

# set up GPIO pins for output
chan_list = list(zones.values()) + [pump]
GPIO.setup(chan_list, GPIO.OUT, initial = GPIO.HIGH)

# cycle through zones, ensuring the pump is on for each zone
sleep_time = 1.5
for zone in zones:
    pump_zone = pump, zones[zone]
    GPIO.output(pump_zone, GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pump_zone, GPIO.HIGH)

# cleanup GPIO
GPIO.cleanup()




