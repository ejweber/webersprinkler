import sys, subprocess, os, json, runpy
from config import propogate_config
log = open('install_log.txt', 'w')

def shellDo(command):
    try:
        log.write(str(command) + '\n')
        print('Executing {}...'.format(command), end=' ', flush=True)
        output = subprocess.check_output(command, universal_newlines=True, 
                                         stderr=subprocess.STDOUT)
        log.write(output)
        print('[OK]')
        return(output)
    except subprocess.CalledProcessError as error:
        log.write(error.output)
        errorString = ('\nCommand failed with error code {}. See install_log.txt '
                       'for more details. Aborting...')
        print(errorString.format(error.returncode))
        exit()

# ensure script runs as root
if os.geteuid() != 0:
    print('Must run as root. Aborting...')
    exit()

# verify and store user input
if len(sys.argv) != 4:
    print('Usage: python setup.py <base url> <local port> <global port>')
    exit()
baseUrl = sys.argv[1]
localPort = sys.argv[2]
globalPort = sys.argv[3]
print('Server will listen at {} on local port {} and global port {}.'.format(
    baseUrl, localPort, globalPort))

# verify that i2c is enabled
try:
	print('Checking if i2c is enabled...', end=' ', flush=True)
	i2c = open('/dev/i2c-1')
	i2c.close()
	print('[OK]')
except FileNotFoundError as error:
	log.write(error.output)
	print('\ni2c must be enabled using raspi-config. Aborting...')
	exit()

# modify global config
configTemplate = open('config/global_config.template', 'r')
configDict = json.load(configTemplate)
configTemplate.close()
configDict['baseUrl'] = baseUrl
configDict['localPort'] = int(localPort)
configDict['globalPort'] = int(globalPort)
configFile = open('config/global_config.json', 'w')
json.dump(configDict, configFile, indent=4)
configFile.close()

# modify local config
os.chdir('config')
configFile = open('global_config.json', 'r')
propogate_config.propogate(configFile)
os.chdir('..')

# update Apache installation
shellDo(['apt-get', 'install', 'apache2', '-qq'])
shellDo(['apt-get', 'install', 'apache2-dev', '-qq'])

# set permissions for Apache to access GPIO pins and i2c
shellDo(['adduser', 'www-data', 'gpio'])
shellDo(['usermod', '-a', '-G', 'i2c', 'www-data'])

# set permissions for Apache to create and modify logs
shellDo(['chgrp', 'www-data', 'app/log'])
shellDo(['chmod', 'g+w', 'app/log'])

# set permissions for Apache to modify saved programs
shellDo(['cp', 'app/config/saved_programs.default', 'app/config/saved_programs.json'])
shellDo(['chown', 'pi', 'app/config/saved_programs.json'])
shellDo(['chgrp', 'www-data', 'app/config/saved_programs.json'])
shellDo(['chmod', 'g+w', 'app/config/saved_programs.json'])

# install pip
shellDo(['apt-get', 'install', 'python3-pip', '-qq'])

# install required Python modules
shellDo(['pip3', 'install', 'mod_wsgi'])
shellDo(['pip3', 'install', 'bottle'])
shellDo(['pip3', 'install', 'smbus2'])
shellDo(['pip3', 'install', 'RPi.GPIO'])
shellDo(['pip3', 'install', 'requests'])

# overwrite /etc/crontab
shellDo(['mv', 'app/config/crontab.txt', '/etc/crontab'])

# configure Apache virtual host to listen on correct port and run scripts
shellDo(['cp', 'apache2/sprinkler.conf', '/etc/apache2/sites-available'])
shellDo(['a2ensite', 'sprinkler'])

# configure Apache to load mod_wsgi from the correct Python interpreter
output = shellDo(['mod_wsgi-express', 'module-config'])
wsgiLoadFile = open('apache2/wsgi.load', 'w')
wsgiLoadFile.write(output)
wsgiLoadFile.close()
shellDo(['cp', 'apache2/wsgi.load', '/etc/apache2/mods-available'])
shellDo(['a2enmod', 'wsgi'])

# restart Apache so changes can take effect
shellDo(['service', 'apache2', 'restart'])

log.close()
