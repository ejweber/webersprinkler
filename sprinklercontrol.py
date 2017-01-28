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
def run_program(programs, letter):   
    GPIO.output(pump, GPIO.LOW)
    for zone in range(0, total_zones):
        GPIO.output(zones[zone], GPIO.LOW)
        time.sleep(programs[letter].valve_times[zone])
        GPIO.output(zones[zone], GPIO.HIGH)
    GPIO.output(pump, GPIO.HIGH)

# allow user to specify single program or zone to run immediately
def manual_mode(programs):
    while True:
        command = input("Enter 'program [A,B,C]' or 'zone [1-5] [time]' "
                        "or 'done': ")
        # allow for single program to run
        if 'program' in command:
            if command[-1] in 'ABC' and command[-2] == ' ':
                if programs[command[-1]].valve_times == []:
                    print('Valve times not set for program ' + command[-1] + '.')
                else:
                    try:
                        print('Running program ' + command[-1] + '...')
                        print("Use ^C to cancel if necessary.")    
                        run_program(programs, command[-1])
                    # allow user to cancel program if necessary
                    except KeyboardInterrupt:
                        print('\nProgram ' + command[-1] + ' canceled.')
                        emergency_stop()
        # allow for single zone to run
        if 'zone' in command:
            split_command = command.split(' ')
            zone = split_command[1]
            run_time = split_command[2]
            try:
                print('Running zone ' + zone + ' for ' + run_time + ' minutes'
                       '...')
                print('Use ^C to cancel if necessary') 
                run_manual(int(zone), int(run_time) * 60)
            except KeyboardInterrupt:
                print('\nZone ' + str(zone) + ' canceled.')
                emergency_stop()
        if command == 'done':
            break

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
    

