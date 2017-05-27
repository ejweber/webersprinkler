from tg import expose, TGController, AppConfig
import webhelpers2
import webhelpers2.text
from wsgiref.simple_server import make_server
from threading import Thread

class RootController(TGController):
    def __init__(self, sprinklers, background):
        self.sprinklers = sprinklers
        self.background = background
    
    @expose('index.xhtml')
    def index(self):
        return self.index_dict('The server is ready for input.')
        
    @expose('index.xhtml')
    def run(self, letter):
        sprinklers = self.sprinklers
        background = self.background
        r_string = ''
        if background.running.is_set():
            r_string = ('The controller was already running and had to be '
                        'stopped.\n')
            background.running.clear()
            background.control.join()
        programmed_valves = len(sprinklers.programs[letter].valve_times)
        if programmed_valves == 0:
            r_string = (r_string + 'No valve times have been set for '
                        'program ' + letter + '.')
            return dict(response=r_string)
        background.running.set()
        background.control = Thread(target=sprinklers.run, 
                         args=(letter, background.running,))
        background.control.start()
        r_string = (r_string + 'The server has agreed to run program ' +
                    letter + '.')
        return self.index_dict(r_string)
        
    @expose('index.xhtml')
    def stop(self):    
        background = self.background
        if background.running.is_set():
                background.running.clear()
                r_string = 'The server has agreed to stop the controller.'
        else:
            r_string = ('The server reports that the controller was not '
                        'running.')
        return self.index_dict(r_string)
        
    @expose('index.xhtml')
    def shutdown(self):
        self.background.shutdown()
        r_string = ('The server is shutting down. This page will become '
                    'unavailable.')
        return self.index_dict(r_string)
    
    def index_dict(self, r_string):
        xhtml_data = dict(response=r_string,
                          status0=self.sprinklers.status[0],
                          status1=self.sprinklers.status[1])
        return xhtml_data

def HTTPServer(sprinklers, background):
    root = RootController(sprinklers, background)
    config = AppConfig(minimal=True, root_controller=root)
    config.renderers = ['kajiki']
    config['helpers'] = webhelpers2
    application = config.make_wsgi_app()
    print('Serving on port 5001...')
    httpd = make_server('', 5001, application)
    while not background.shutdown_flag.is_set():
        httpd.handle_request()
