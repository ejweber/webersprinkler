import sys, os
sys.path.append(os.path.dirname(__file__))

import bottle
import web_framework

bottle.debug(True)
application = bottle.default_app()