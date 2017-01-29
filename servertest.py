'''
# REFERENCE CODE FOR A SERVER THAT WORKS
import socket, time

def Main():
    host = '127.0.0.1'
    port = 5000
    
    s = socket.socket()
    s.bind((host, port))
    
    s.listen(1)
    c, addr = s.accept()
    print('Connection from: ' + str(addr))
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        print('From connected user: ' + data)
        data = data.upper()
        print('Sending: ' + str(data))
        c.send(data.encode('utf-8'))
    c.close()
    
if __name__ == '__main__':
    Main()
'''

# import necessary modules
import socket, pickle
from sprinklercontrol import *
from sprinklerdata import load_programs, SprinklerProgram

# globally accessible variables
host = '127.0.0.1'
port = 5000

# set up and return socket
def server_setup():
    global host, port
    s = socket.socket()
    s.bind((host, port))
    return s
    
# block until daemon recieves instructions and output as a string
def recieve(s):
    s.listen(1)
    print('listening for instructions')
    c, addr = s.accept()
    data = pickle.loads(c.recv(1024))
    print(str(addr) + ' sent '+ str(data))
    c.send('instructions recieved by server'.encode('utf-8'))
    c.close()
    return data
    
def parse(data, programs):
    if 'run' in data:
        if 'program' in data:
            letter = data[2]
            run_program(programs, letter)
        if 'zone' in data:
            zone = int(data[2])
            time = int(data[3])
            run_manual(zone, time)
        
if __name__ == '__main__':
    prepare_relay()
    s = server_setup()
    programs = load_programs()
    try:
        while True:
            data = recieve(s)
            parse(data, programs)
    except:
        s.close()
    cleanup()
    
