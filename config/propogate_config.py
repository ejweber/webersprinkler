import json, time, string

def propogate(configInput=None):
    # load info from global configuration
    if configInput is None:
        configInput = open('global_config.json', 'r')
    inputDict = json.load(configInput)
    configInput.close()

##### sprinkler system configuration    
    
    # load structure from local configuration
    try:
        configOutput = open('../app/config/system_config.json', 'r')
    except FileNotFoundError:
        configOutput = open('../app/config/system_config.template', 'r')
    outputDict = json.load(configOutput)
    configOutput.close()

    # change local configuration paramter
    outputDict['port'] = inputDict['localPort']
    outputFile = open('../app/config/system_config.json', 'w')
    json.dump(outputDict, outputFile, indent=4)
    outputFile.write('\n')
    outputFile.close()
    
##### apache configuration
    
    configOutput = open('../apache2/sprinkler.template', 'r')
    outputString = configOutput.read()
    configOutput.close()
    outputTemplate = string.Template(outputString)
    outputString = outputTemplate.substitute(outputTemplate, 
                                             serverName=inputDict['baseUrl'])
    outputFile = open('../apache2/sprinkler.conf', 'w')
    outputFile.write(outputString)
    outputFile.close()
    
##### swagger configuration

    with open('../swagger/swagger.template') as file:
        outputDict = json.load(file)
    outputDict['host'] = inputDict['baseUrl'] + ':' + str(inputDict['globalPort'])
    with open('../swagger/swagger.json', 'w') as file:
        json.dump(outputDict, file, indent=4)
        file.write('\n')
	
if __name__ == '__main__':
    propogate()
