'''
# REFERENCE CODE FOR A SERVER THAT WORKS
import socket, time

def Main():
    host = '127.0.0.1'
    port = 5000
    
    s = socket.socket()
    s.connect((host, port))
    
    message = input('-> ')
    while message != 'q':
        s.send(message.encode('utf-8'))
        data = s.recv(1024)
        data = data.decode('utf-8')
        print('Recieved from server: ' + data)
        message = input('-> ')
    s.close()
    
if __name__ == '__main__':
    Main()
'''    

import socket, time, pickle

def Main():
    host = '127.0.0.1'
    port = 5000
    
    while True:
        message = input('-> ')
        if message == 'q':
            break
        message = message.split(' ')
        s = socket.socket()   
        s.connect((host, port))
        s.send(pickle.dumps(message))
        response = s.recv(1024).decode('utf-8')
        if not response:
            print('no response from server')
        else:
            print(response)
        s.close()
    
if __name__ == '__main__':
    Main()
