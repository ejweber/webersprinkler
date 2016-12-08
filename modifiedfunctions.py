import pickle

class SprinklerProgram:
    def __init__(self, program_letter):
        self.program_letter = program_letter
        self.valve_times = []
        self.run_times = []

A = SprinklerProgram('A')
B = SprinklerProgram('B')
C = SprinklerProgram('C')

# input times for program A, B, or C
def modify_programs():
    global A, B, C
    programs = {'A': A, 'B': B, 'C': C}
    program_letter = 'D'
    while program_letter not in 'ABC' or len(program_letter) != 1:
        program_letter = input('Enter a program letter from A to C: ')
    for zone in range(1, 6):
        time = input('Enter a time for zone ' + str(zone) + ': ')
        programs[program_letter].valve_times.append(time)

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

modify_programs()
save_programs()
