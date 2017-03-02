import pickle, socket
from threading import Thread

# create server class with appropriate functions inherited from socket.socket
class TCPServer(socket.socket):
    def __init__(self, sprinklers, background):
        socket.socket.__init__(self)
        self.host = '192.168.1.3'
        self.port = 5000
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.settimeout(5)
        self.bind((self.host, self.port))
        print('The TCP server is set up and listening for instructions...')
        self.server_loop(sprinklers, background)
        
    # block until server recieves instructions and output as a tuple
    def info_recieve(self):
        self.listen(1)
        c, addr = self.accept()
        data = pickle.loads(c.recv(1024))
        print(str(addr) + ' sent '+ str(data) + ' to the TCP server.')
        return c, data
  
        
    # send response string to client
    def info_send(self, c, response):
        c.send(pickle.dumps(response))
        c.close()
    
    # analyze recieved command and execute necessary function
    def parse(self, data, sprinklers, background):
        if 'run' in data:
            r_string = ''
            if background.running.is_set():
                r_string = ('The controller was already running and had to be '
                            'stopped.\n')
                background.running.clear()
                background.control.join()
            if 'program' in data:
                letter = data[2]
                programmed_valves = len(sprinklers.programs[letter].valve_times)
                if programmed_valves == 0:
                    r_string = (r_string + 'No valve times have been set for '
                                'program ' + letter + '.')
                    return r_string
                background.running.set()
                background.control = Thread(target=sprinklers.programs[letter].run, 
                                 args=(background.running,))
                background.control.start()
                r_string = (r_string + 'The server has agreed to run program ' +
                            letter + '.')
                return r_string
            if 'zone' in data:
                zone = int(data[2])
                run_time = int(data[3])
                run_minutes = str(int(run_time / 60))
                if not background.running.is_set():
                    background.running.set()
                    background.control = Thread(target=sprinklers.run_zone, args=(zone, 
                                     run_time, background.running))
                    background.control.start()
                    r_string = (r_string + 'The server has agreed to run zone ' + 
                                str(zone) + ' for ' + run_minutes + ' minutes.')
                    return r_string
        if 'change' in data:
            programs = load_programs()
            schedule_stored_datetimes(programs)
            return 'The server is aware of the change.'
        if 'queue' in data:
            queue = background.return_queue()
            if not queue:
                queue = 'The server is not aware of any upcoming events.'
            return queue
        if 'stop' in data:
            if background.running.is_set():
                background.running.clear()
                return 'The server has agreed to stop the controller.'
            if not background.running.is_set():
                return 'The server reports that the controller was not running.'
        if 'display' in data:
            letter = data[1]
            information = {'valve_times': sprinklers.programs[letter].valve_times,
                           'run_times': sprinklers.programs[letter].list_times()
                          }
            return information
        if 'valves' in data:
            letter = data[1]
            new_times = data[2]
            sprinklers.programs[letter].valve_times = new_times
            sprinklers.save()
            return 'The server has made the change.'
        if 'schedule' in data:
            letter = data[1]
            new_time = (data[2], data[3])
            sprinklers.programs[letter].store_time(new_time)
            background.schedule_stored_datetimes()
            sprinklers.save()
            return 'The server has made the change.'
        if 'clear' in data:
            letter = data[1]
            sprinklers.programs[letter].valve_times = []
            sprinklers.programs[letter].run_times = []
            return 'The server has made the change.'
        if 'shutdown' in data:
            background.shutdown()
            return 'The server is shutting down.'
        # TAKE OUT OF FINAL BUILD!
        if 'test' in data:
            return('The TCP server is capable of a response.')
            
    # listen for and respond to requests indefinitely
    def server_loop(self, sprinklers, background):
        while not background.shutdown_flag.is_set():
            try:
                c, data = self.info_recieve()
                response = self.parse(data, sprinklers, background)
                self.info_send (c, response)
            except socket.timeout:
                pass
            
if __name__ == '__main__':
    tcp_sprinkler_server = TCPSprinklerServer()
