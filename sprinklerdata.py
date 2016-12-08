import pickle

# define SprinklerProgram class
class SprinklerProgram:
    def __init__(self, program_letter):
        self.program_letter = program_letter
        self.valve_times = []
        self.run_times = []

# create global sprinkler programs
A = SprinklerProgram('A')
B = SprinklerProgram('B')
C = SprinklerProgram('C')

# modify times for program A, B, or C
def modify_programs(letter):
    global A, B, C
    programs = {'A': A, 'B': B, 'C': C}
    programs[letter].valve_times = []
    for zone in range(1, 6):
        time = input('Enter a time for zone ' + str(zone) + ': ')
        programs[letter].valve_times.append(time)
    save_programs()

# save programs in json format
def save_programs():
    global A, B, C
    file = open('saved_programs.json', 'wb')
    sprinkler_programs = [A, B, C]
    pickle.dump(sprinkler_programs, file)

# load programs from json formatted file
def load_programs():
    global A, B, C
    try:
        file = open('saved_programs.json', 'rb')
    except FileNotFoundError:
        print("No saved programs file found.")
        return False
    sprinkler_programs = pickle.load(file)
    A = sprinkler_programs[0]
    B = sprinkler_programs[1]
    C = sprinkler_programs[2]
    file.close()

# display valve times for program A, B, or C
def display_valve_times(letter):
    global A, B, C
    programs = {'A': A, 'B': B, 'C': C}
    number = 1
    for valve in programs[letter].valve_times:
       print('Valve ' + str(number) + ': ' + valve)
       number += 1
