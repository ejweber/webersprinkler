import pickle
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta

# define SprinklerProgram class
# must be instantiated inside SprinklerSystem class to operate correctly
class SprinklerProgram:
    def __init__(self, letter, pump, zones, total_zones):
        self.valve_times = []
        self.run_times = []
        self.letter = letter
        self.pump = pump
        self.zones = zones
        self.total_zones = total_zones
        
    # run program according to valve times
    def run(self, flag=None):   
        GPIO.output(self.pump, GPIO.LOW)
        for zone in range(0, self.total_zones):
            start_time = time.time()
            run_time = self.valve_times[zone]
            if flag:
                while(time.time() - start_time) < run_time and flag.is_set():
                    GPIO.output(self.zones[zone], GPIO.LOW)
            else:
                while (time.time() - start_time) < run_time:
                    GPIO.output(self.zones[zone], GPIO.LOW)
            GPIO.output(self.zones[zone], GPIO.HIGH)
        GPIO.output(self.pump, GPIO.HIGH)
        if flag:
            flag.clear()
    
    # insert new run_time into sorted list of run_times
    def store_time(self, datetime_tuple):
        normalized = self.normalize_datetime(datetime_tuple)
        self.run_times.append(normalized)
        self.run_times.sort()
    
    # take tuple of the form (day, hour:minute) and normalize it to the week of
    # 5/1/16 for comparison
    def normalize_datetime(self, datetime_tuple):
        temp_day = self.index_day(datetime_tuple[0])
        temp_time = datetime.strptime(datetime_tuple[1], '%H:%M')
        normalized = datetime(2016, 5, 1 + temp_day,)
        offset = timedelta(hours=temp_time.hour, minutes=temp_time.minute)
        normalized += offset
        return normalized

    # take current time and 'normalize' week beggining 5/1/16
    def normalize_current_datetime(self):
        now = datetime.now()
        day = datetime.strftime(now, '%w')
        stored_datetime = datetime(2016, 5, 1 + int(day),
                          now.hour, now.minute, now.second, now.microsecond)
        return(stored_datetime)
        
    # return integer from 0-6 based on day input by user
    def index_day(self, day):
        return {'Sunday': 0,
                'Monday': 1,
                'Tuesday': 2,
                'Wednesday': 3,
                'Thursday': 4,
                'Friday': 5,
                'Saturday': 6
                }[day]
                
    # calculate time to next run for each stored run_time
    def next_times(self):
        now = self.normalize_current_datetime()
        next_times = []
        for entry in self.run_times:
            difference = entry - now
            if difference < timedelta():
                difference += timedelta(7)
            difference = difference.total_seconds()
            next_times.append(difference)
        return next_times
        
    # output stored run_times in display friendly list
    def list_times(self):
        formatted_times = []
        for entry in self.run_times:
            formatted_time = datetime.strftime(entry, '%A %H:%M')
            formatted_times.append(formatted_time)
        return formatted_times

# define SprinklerSystem class
class SprinklerSystem:
    def __init__(self):
        self.pump = 9
        self.zones = [10, 22, 27, 17, 4, 3, 2]
        self.total_zones = 5
        self.prepare_relay()
        self.load()
        
    def load(self):
        # load programs from pickle formatted file
        try:
            file = open('saved_programs.p', 'rb')
            sprinkler_programs = pickle.load(file)
            self.A = sprinkler_programs[0]
            self.B = sprinkler_programs[1]
            self.C = sprinkler_programs[2]
            file.close()
        # create new programs if no saved programs are found
        except FileNotFoundError:
            print("No saved programs file found.")
            self.A = SprinklerProgram('A', self.pump, self.zones, 
                                      self.total_zones)
            self.B = SprinklerProgram('B', self.pump, self.zones, 
                                      self.total_zones)
            self.C = SprinklerProgram('C', self.pump, self.zones, 
                                      self.total_zones)
        self.programs = {'A': self.A, 'B': self.B, 'C': self.C}
            
    # save programs in pickle formatted file
    def save(self):
        file = open('saved_programs.p', 'wb')
        sprinkler_programs = [self.A, self.B, self.C]
        pickle.dump(sprinkler_programs, file)
        
    # prepare relay for GPIO
    def prepare_relay(self):
        # disable GPIO warnings from improper shutdown
        GPIO.setwarnings(False)
        # set GPIO mode
        GPIO.setmode(GPIO.BCM)
        # set up GPIO pins for output
        chan_list = self.zones + [self.pump]
        GPIO.setup(chan_list, GPIO.OUT, initial = GPIO.HIGH)
        
    # stop pump and all zones
    def emergency_stop():
        chan_list = self.zones + [self.pump]
        GPIO.output(chan_list, GPIO.HIGH)

    # cleanup GPIO for program exit
    def cleanup(self):
        GPIO.cleanup()
        
    # test relay for effective operation
    def relay_test(self):
        sleep_time = 1.5
        for zone in self.zones:
            pump_zone = self.pump, zone
            GPIO.output(pump_zone, GPIO.LOW)
            time.sleep(sleep_time)
            GPIO.output(pump_zone, GPIO.HIGH)
            
    # run zone manually for specified amount of time
    def run_zone(self, zone, run_time, flag=None):
        start_time = time.time()
        if flag:
            while(time.time() - start_time) < run_time and flag.is_set():
                GPIO.output(self.pump, GPIO.LOW)
                GPIO.output(self.zones[zone], GPIO.LOW)
        if not flag:
            while (time.time() - start_time) < run_time:
                GPIO.output(self.pump, GPIO.LOW)
                GPIO.output(self.zones[zone], GPIO.LOW)
        GPIO.output(self.pump, GPIO.HIGH)
        GPIO.output(self.zones[zone], GPIO.HIGH)
        if flag:
            flag.clear()

if __name__ == '__main__':
    sprinklers = SprinklerSystem()

