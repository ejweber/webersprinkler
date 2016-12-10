import pickle
from datetime import datetime, timedelta

# define SprinklerProgram class
class SprinklerProgram:
    def __init__(self, letter):
        self.letter = letter
        self.valve_times = []
        self.run_times = []

# modify times for program A, B, or C
def modify_programs(programs, letter):
    programs[letter].valve_times = []
    for zone in range(1, 6):
        time = input('Enter a time for zone ' + str(zone) + ': ')
        programs[letter].valve_times.append(time)
    save_programs(programs)

# save programs in pickle formatted file
def save_programs(programs):
    file = open('saved_programs.p', 'wb')
    sprinkler_programs = [programs['A'], programs['B'], programs['C']]
    pickle.dump(sprinkler_programs, file)

# load programs from pickle formatted file
def load_programs():
    try:
        file = open('saved_programs.p', 'rb')
        sprinkler_programs = pickle.load(file)
        A = sprinkler_programs[0]
        B = sprinkler_programs[1]
        C = sprinkler_programs[2]
        file.close()
    except FileNotFoundError:
        print("No saved programs file found.")
        A = SprinklerProgram('A')
        B = SprinklerProgram('B')
        C = SprinklerProgram('C')
    programs = {'A': A, 'B': B, 'C': C}
    return programs

# display valve and/or run times for programs A, B, or C
def display_times(programs, letter, option='all'):
    if option == 'all' or option == 'valve':
        number = 1
        for valve in programs[letter].valve_times:
           print('Valve ' + str(number) + ': ' + valve)
           number += 1
    if option == 'all' or option == 'run':
        for entry in programs[letter].run_times:
            print(datetime.strftime(entry, '%A %H:%M'))

# take day and time input by user and 'normalize' to week beggining 5/1/16
def normalize_input_datetime(programs, letter):
    raw_input = input('Enter weekday and time for program to run: ')
    split_input = raw_input.split(' ')
    temp_day = index_day(split_input[0])
    temp_time = datetime.strptime(split_input[1], '%H:%M')
    stored_datetime = datetime(2016, 5, 1 + temp_day,)
    offset = timedelta(hours=temp_time.hour, minutes=temp_time.minute)
    stored_datetime += offset
    programs[letter].run_times.append(stored_datetime)
    save_programs(programs)

# calculate the time until each event should run next using 'normalized' times
# remove old events from schedule and add new ones

def schedule_stored_datetimes(programs,schedule, queue):
    now = normalize_current_datetime()
    for letter, program in programs.items():
        for normal_time in program.run_times:
            difference = normal_time - now
            if difference < timedelta():
                difference += timedelta(7)
            difference = difference.total_seconds()
            scheduled_event = schedule.enter(difference, 1, print, argument=
                                             program.letter)
            number = 1
            queue[program.letter + str(number)] = scheduled_event
            number += 1

# take current time and 'normalize' week beggining 5/1/16
def normalize_current_datetime():
    now = datetime.now()
    day = datetime.strftime(now, '%w')
    stored_datetime = datetime(2016, 5, 1 + int(day),
                           now.hour, now.minute, now.second)
    return(stored_datetime)
    
# return integer from 0-6 based on day input by user
def index_day(day):
    return {'Sunday': 0,
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6
            }[day]
