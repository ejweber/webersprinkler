import json

programs = {'A': [], 'B': [], 'C': []}
x = 5

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
def save_programs():
    global programs
    file = open('saved_programs.json', 'w')
    json.dump(programs, file)
    file.close()

# load programs from json formatted file
def load_programs():
    global programs
    try:
        file = open('saved_programs.json', 'r')
    except FileNotFoundError:
        print("No saved programs file found.")
        return False
    programs = json.load(file)
    file.close()
