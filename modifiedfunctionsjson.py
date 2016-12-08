import json

class SprinklerProgram:
    def __init__(self, program_letter):
        self.program_letter = program_letter
        self.valve_times = []
        self.run_times = []

A = SprinklerProgram('A')
B = SprinklerProgram('B')
C = SprinklerProgram('C')
sprinkler_programs = [A, B, C]

# input times for program A, B, or C
def modify_programs():
    global programs
    program_letter = 'D'
    while program_letter not in 'ABC' or len(program_letter) != 1:
        program_letter = input('Enter a program letter from A to C: ')
    programs[program_letter] = []
    for zone in range(1, 6):
        time = input('Enter a time for zone ' + str(zone) + ': ')
        programs[program_letter].append(time)

# save programs in json format
def save_programs(sprinkler_programs):
    file = open('saved_programs.json', 'w')
    json_dict = {}
    for program in sprinkler_programs:
        json_dict[program.program_letter + '_valve'] = program.valve_times
        json_dict[program.program_letter + '_run'] = program.run_times
    json.dump(json_dict, file)

# load programs from json formatted file
def load_programs(sprinkler_programs):
    try:
        file = open('saved_programs.json', 'r')
    except FileNotFoundError:
        print("No saved programs file found.")
        return False
    json_dict = json.load(file)
    for program in sprinkler_programs:
        json_dict    
    file.close()

save_programs(sprinkler_programs)
