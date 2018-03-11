import subprocess
import os
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

if os.geteuid() != 0:
    print('Must run as root. Aborting...')
    exit()
        
# update Apache installation
shellDo(['apt-get', 'install', 'apache2', '-qq'])
shellDo(['apt-get', 'install', 'apache2-dev', '-qq'])

# set permissions for Apache to access GPIO pins
shellDo(['adduser', 'www-data', 'gpio'])

# install required Python modules
shellDo(['pip3', 'install', 'mod_wsgi'])
shellDo(['pip3', 'install', 'bottle'])

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
