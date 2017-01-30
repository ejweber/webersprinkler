# import necessary modules
import RPi.GPIO as GPIO
import time

# make zone pin numbers globally available
# only this block of code should change if relay rewired
pump = 9
zones = [10, 22, 27, 17, 4, 3, 2]
total_zones = 5

# prepare relay for GPIO
def prepare_relay():
    # set GPIO mode
    GPIO.setmode(GPIO.BCM)

    # set up GPIO pins for output
    chan_list = zones + [pump]
    GPIO.setup(chan_list, GPIO.OUT, initial = GPIO.HIGH)

# cycle through zones, ensuring the pump is on for each zone
# for debug purposes (not called by sprinklermain)
def relay_test():
    sleep_time = 1.5
    for zone in zones:
        pump_zone = pump, zone
        GPIO.output(pump_zone, GPIO.LOW)
        time.sleep(sleep_time)
        GPIO.output(pump_zone, GPIO.HIGH)

# run pump and zones for times specified by SprinklerProgram.run_times 
def run_program(programs, letter, flag=None):   
    GPIO.output(pump, GPIO.LOW)
    for zone in range(0, total_zones):
        start_time = time.time()
        run_time = programs[letter].valve_times[zone]
        while (time.time() - start_time) < run_time and (flag.is_set() or
                                                          not flag):
            GPIO.output(zones[zone], GPIO.LOW)
        GPIO.output(zones[zone], GPIO.HIGH)
    GPIO.output(pump, GPIO.HIGH)

# run specified pump and zone for specified time
def run_manual(zone, run_time):
    GPIO.output(pump, GPIO.LOW)
    GPIO.output(zones[zone], GPIO.LOW)
    time.sleep(run_time)
    GPIO.output(pump, GPIO.HIGH)
    GPIO.output(zones[zone], GPIO.HIGH)

# stop pump and all zones
def emergency_stop():
    chan_list = zones + [pump]
    GPIO.output(chan_list, GPIO.HIGH)

# cleanup GPIO     
def cleanup():
    GPIO.cleanup()
    
if __name__ == "__main__":
    prepare_relay()
    relay_test()
    cleanup()
    

