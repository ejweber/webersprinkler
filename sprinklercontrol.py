# import modules
import RPi.GPIO as GPIO
import time

# make zone pin numbers globally available
pump = 9
zones = [10, 22, 27, 17, 4, 3, 2]
total_zones = 5

def prepare_relay():
    # set GPIO mode
    GPIO.setmode(GPIO.BCM)

    # set up GPIO pins for output
    chan_list = zones + [pump]
    GPIO.setup(chan_list, GPIO.OUT, initial = GPIO.HIGH)

# cycle through zones, ensuring the pump is on for each zone
def relay_test():
    sleep_time = 1.5
    for zone in zones:
        pump_zone = pump, zone
        GPIO.output(pump_zone, GPIO.LOW)
        time.sleep(sleep_time)
        GPIO.output(pump_zone, GPIO.HIGH)

def run_program(programs, letter):
    #DEBUG
    f = open('test.txt', w)
    print('program runs', file=f)
    f.close()
    
    GPIO.output(pump, GPIO.LOW)
    for zone in range(0, total_zones):
        GPIO.output(zones[zone], GPIO.LOW)
        print(programs[letter].valve_times[zone])
        time.sleep(programs[letter].valve_times[zone])
        GPIO.output(zones[zone], GPIO.HIGH)
    GPIO.output(pump, GPIO.HIGH)
        
def cleanup():
    # cleanup GPIO
    GPIO.cleanup()
