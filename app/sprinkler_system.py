import RPi.GPIO as GPIO
from threading import Timer
import lcd_functions as lcd
import logging as log
import json, time, requests
import atexit

config_file = '/home/pi/webersprinkler/app/config/system_config.json'

# stop sprinklers and reset LCD if webersprinkler ends abrubtly
@atexit.register
def emergency_stop():
    LCD.idle()
    GPIO.cleanup()

class Sprinklers(Timer):
    
    def __init__(self, time_until, program, status, stop):
        try:
            Timer.__init__(self, time_until, self.thread_task)
            self.program = program
            self.stop = stop
            self.stop.clear()
            self.status = status
            config = self.read_system_config()
            self.zones = config['zones']
            self.pump = config['pump']
            self.port = config['port']
            self.prepare_relay(self)
            message = ('Sprinkler thread started for {} with {} zone '
                       'times'.format(program['name'], program['zone_times']))
            log.info(message)
        except KeyError:
            log.exception('Unable to initialize sprinklers correctly.')

    def thread_task(self):
        log.debug('sprinklers.thread_task() called')
        self.recalculate()
        self.run_program()
        self.cleanup()
        log.info('Sprinkler thread ended')

    @staticmethod
    def read_system_config():
        log.debug('sprinklers.read_system_config() called')
        try:
            with open(config_file) as file:
                config = json.load(file)
                log.info('System config file loaded successfully.')
        except FileNotFoundError:
            log.warning('System config file not found.')
            config = {}
        return config

    @staticmethod
    def prepare_relay(self):
        log.debug('sprinklers.prepare_relay() called')
        # disable GPIO warnings from improper shutdown
        GPIO.setwarnings(False)
        # set GPIO mode
        GPIO.setmode(GPIO.BCM)
        # set up GPIO pins for output)
        chan_list = self.zones + [self.pump]
        GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)

    def run_program(self):
        log.debug('sprinklers.run_program() called')
        GPIO.output(self.pump, GPIO.LOW)
        self.status['program'] = self.program['name']
        # CHANGE LCD DISPLAY HERE
        zone_times = self.program['zone_times']
        for zone in range(0, len(zone_times)):
            if zone_times[zone] > 0:
                self.status['zone'] = 'Zone ' + str(zone + 1)
                start_time = time.time()
                run_time = zone_times[zone] * 60
                remaining = int(run_time - (time.time() - start_time))
                GPIO.output(self.zones[zone], GPIO.LOW)
                while remaining > 0 and not self.stop.is_set():
                    remaining = int(run_time - (time.time() - start_time))
                    m, s = divmod(remaining, 60)
                    self.status['time'] = '{:02}:{:02}'.format(m, s)
                    lcd_status = (self.status['program'],
                        self.status['zone'] + ' ' + self.status['time'])
                    LCD.display(lcd_status)
                if self.stop.is_set():
                    break

            if zone_times[zone] < 0:
                self.status['zone'] = 'Zone ' + str(zone + 1)
                GPIO.output(self.zones[zone], GPIO.LOW)
                self.status['time'] = 'Indef'
                self.stop.wait()
            GPIO.output(self.zones[zone], GPIO.HIGH)

    def cleanup(self):
        self.status['time'] = None
        self.status['program'] = None
        self.status['zone'] = None
        LCD.idle()
        GPIO.cleanup()
        if not self.stop.is_set(): # only reschedule if thread stops on own
            self.reschedule()

    def recalculate(self):
        log.debug('sprinklers.recalculate() called')
        url = 'http://localhost:{}/api/recalculate'.format(self.port)
        if requests.post(url).status_code != 200:
            log.warning('Request to recalculate next task failed')

    def reschedule(self):
        log.debug('sprinklers.reschedule() called')
        url = 'http://localhost:{}/api/reschedule'.format(self.port)
        if requests.post(url).status_code != 200:
            log.warning('Request to schedule next task failed')


class LCD():
	
    @staticmethod
    def idle():
        idle_status = ('webersprinkler', 'Ready...')
        LCD.display(idle_status)
    
    @staticmethod
    def display(message):
        padded_message = []
        for line in message:
            for x in range(16 - len(line)):
                line = line + ' '
            padded_message.append(line)
        try:
            lcd.write(0, 0, padded_message[0])
            lcd.write(0, 1, padded_message[1])
        except OSError as error:
            log.error(error.strerror)
            
    @staticmethod
    def initialize():
        try:
            lcd.init(0x27, 1)
            LCD.idle()
        except OSError as error:
            log.error(error.strerror)

