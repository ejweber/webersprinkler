import json, time, logging.handlers, os, string, random
import logging as log
from threading import Event
from sprinkler_system import Sprinklers, LCD

def set_up_logs():
    debug_file = '/home/pi/webersprinkler/app/log/debug.log'
    info_file = '/home/pi/webersprinkler/app/log/info.log'

    root_log = logging.getLogger()
    root_log.setLevel(logging.DEBUG)

    debug_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    debug_handler = logging.handlers.RotatingFileHandler(debug_file, mode='w',
                                                         backupCount=5,
                                                         delay=True)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(debug_format)
    root_log.addHandler(debug_handler)
    if os.path.isfile(debug_file):
        debug_handler.doRollover()

    info_format = logging.Formatter('%(asctime)s: %(message)s')
    info_handler = logging.handlers.RotatingFileHandler(info_file, mode='w',
                                                        backupCount=5,
                                                        delay=True)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(info_format)
    root_log.addHandler(info_handler)
    if os.path.isfile(info_file):
        info_handler.doRollover()


class API(object):
  
    idle_status = ('webersprinkler', 'Ready...')

    def __init__(self):
        self.programs = self.read_program_file()
        self.stop = Event()
        self.status = {
            'program': None,
            'zone': None,
            'time': None,
            'next': {}
        }
        self.sprinkler_thread = None
        self.schedule_next_program()
        LCD.initialize()
        LCD.display(API.idle_status)
        log.info('Main program initialized successfully')

    @staticmethod
    def read_program_file():
        try:
            with open(
                    '/home/pi/webersprinkler/app/saved_programs.json') as file:
                programs = json.load(file)
                log.info('Saved program file loaded successfully')
        except FileNotFoundError:
            log.warning('Saved program file not found')
            programs = {}
        return programs

    def run_program(self, time_until=0, program=None):
        log.debug('api.run_program() called')
        self.stop_sprinklers()
        log.debug(program)
        self.sprinkler_thread = Sprinklers(time_until, program, self.status,
                                           self.stop)
        self.sprinkler_thread.start()
        # wait to pass control back to web api until status updates
        if time_until == 0:
            while self.status['program'] is None:
                pass

    def stop_sprinklers(self, reschedule=False):
        log.debug('api.stop_sprinklers() called')
        log.debug(self.sprinkler_thread)
        if self.sprinkler_thread is not None:
            log.debug(self.sprinkler_thread.is_alive())
        if (self.sprinkler_thread is not None and
                self.sprinkler_thread.is_alive()):
            self.stop.set()
            self.sprinkler_thread.cancel() # if program is waiting to run
            self.sprinkler_thread.join()
            # only reschedule if standalone stop called
            if reschedule is True:
                self.schedule_next_program()
            log.info('Sprinklers stopped on command')
        else:
            log.info('Sprinklers did not need to be stopped')

    def run_manual(self, zone, time):
        zone_times = []
        for zone_time in range(0, zone):
            zone_times.append(0)
        zone_times.append(int(time))
        program = {
            'name': 'Manual',
            'zone_times': zone_times
        }
        self.run_program(program=program)

    # input: time list in the format [day, hour, minute] where Monday-Sunday
    # corresponds to 0-6 and hour corresponds to 0-23
    # output: time in seconds until run_time
    @staticmethod
    def parse_run_time(string_time):
        weekdays = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                    'Friday': 4, 'Saturday': 5, 'Sunday': 6}
        split_time = string_time.split()
        day = weekdays[split_time[0]]
        hour, minute = split_time[1].split(':')
        hour = int(hour)
        minute = int(minute)
        log.debug('{} {} {}'.format(day, hour, minute))
        run_time = (day * 24 * 60 + hour * 60 + minute) * 60
        current_time_struct = time.localtime()
        current_day = current_time_struct.tm_wday
        current_hour = current_time_struct.tm_hour
        current_minute = current_time_struct.tm_min
        current_second = current_time_struct.tm_sec
        current_time = ((current_day * 24 * 60 + current_hour * 60 +
                         current_minute) * 60 + current_second)
        relative_time = (run_time - current_time) % (7 * 24 * 60 * 60)
        log.debug('Returned relative time: {}'.format(relative_time))
        return relative_time

    # modify status['next'] and choose next program to run
    # input: list of programs
    # output: next_program tuple with (program, time until program should run)
    def choose_next_program(self):
        log.debug('api.choose_next_program() called')
        next_program = None
        list_time = []
        for program in self.programs:
            log.debug(program)
            for run_time in program['run_times']:
                parsed_time = self.parse_run_time(run_time)
                # only schedule program as next if it occurs later than now
                if next_program is None or (parsed_time < next_program[1]
                                            and parsed_time != 0):
                    next_program = (program, parsed_time)
                    list_time = run_time
        log.debug ('Next program: {}'.format(next_program))
        if next_program:
            self.status['next'] = {'name': next_program[0]['name'],
                                   'run_time': list_time}
        else:
            self.status['next'] = {'name': None, 'run_time': None}
        return next_program

    def schedule_next_program(self):
        log.debug('api.schedule_next_program() called')
        next_program = self.choose_next_program()
        log.debug(next_program)
        if next_program:
            self.run_program(time_until=next_program[1], program=next_program[0])

    def add_or_update(self, request, program_id):
        if program_id is None:
            program_id = self.get_new_id()
            temp_program = {'name': 'Program ' + program_id,
                            'run_times': [],
                            'zone_times': [0, 0, 0, 0, 0],
                            'description': '',
                            'recurring': True}
        else:
            temp_program = self.get_program_by_id(program_id)
        for key, value in request.items():
            if key == 'run_times':
                temp_program['run_times'] = value
                # subtract next run time from Monday 0:00
                # the smallest positive difference is first in the week to run
                temp_program['run_times'].sort(key=lambda x: 
                    ((self.parse_run_time(x) - 
                      self.parse_run_time('Monday 0:00')) % (60 * 60 * 24 * 7)))
            else:
                temp_program[key] = value
        if self.validate_program(temp_program) is True:
            self.add_or_replace(temp_program)
            return True
        else:
            return False

    def choose_next_letter(self):
        current_list = list(self.programs.keys())
        current_list.sort()
        next_letter = chr(ord(current_list.pop()) + 1)
        return next_letter

    @staticmethod
    def validate_program(temp_program):
        log.debug('temp_program: {}'.format(temp_program))
        log.debug(temp_program)
        for key, value in temp_program.items():
            if key == 'recurring':
                if value is not True and value is not False:
                    log.debug('Invalid recurring state')
                    return False
                break
            if key == "zone_times":
                for number in value:
                    if not isinstance(number, int):
                        log.debug('Invalid zone time')
                        return False
                if len(value) < 1:
                    log.debug('No zone time')
                    return False
                if len(value) > 5:
                    log.debug('Too many zone times')
                    return False
                break
            if key == "run_times":
                for entry in value:
                    split = entry.split()
                    if split[0] not in ['Monday', 'Tuesday', 'Wednesday',
                                        'Thursday', 'Friday', 'Saturday',
                                        'Sunday']:
                        log.debug('Invalid run day')
                        return False
                    if ':' not in split[1]:
                        log.debug('No comma in run time')
                        return False
                    split = split[1].split(':')
                    if not split[0].isdigit() or not split[1].isdigit():
                        log.debug('Invalid run time')
                        return False
                break
            if key == 'id':
                if not value.isalnum():
                    log.debug('Invalid key characters')
                    return False
                if len(value) is not 8:
                    log.debug('Incorrect key length')
                    return False
                break
            if key == 'description' or key == 'name':
                break
            else:
                log.debug('Bad key: ' + key)
                return False
        return True
    
    # delete either a program or a specified run time
    # an attempt to delete a non-existent program raises a KeyError
    # an attempt to delete a non-existent run time rasies a ValueError
    def delete(self, program_id, run_time):
        if not run_time:
            del self.programs[program_id]
        else:
            self.programs[program_id]['run_times'].remove(run_time)

    def get_program_by_id(self, program_id):
        for program in self.programs:
            if program['id'] == program_id:
                return program
        return None

    def add_or_replace(self, new_program):
        for old_program in self.programs:
            if old_program['id'] == new_program['id']:
                old_program = new_program
                return
        self.programs.append(new_program)

    @staticmethod
    def get_new_id():
        char_number = 8
        all_char = string.ascii_letters + string.digits
        new_id = ''
        for x in range(0, char_number):
            new_id += all_char(random.randint)
        return new_id
