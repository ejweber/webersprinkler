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
    outputFile.close()
    
##### apache configuration
    configOutput = open('../apache2/sprinkler.template', 'r')
    outputString = configOutput.read()
    configOutput.close()
    outputTemplate = string.Template(outputString)
    # TODO: handle stripping of baseUrl more elegantly
    outputString = outputTemplate.substitute(outputTemplate, 
                                             serverName=inputDict['baseUrl'])
    outputFile = open('../apache2/sprinkler.conf', 'w')
    outputFile.write(outputString)
    outputFile.close()
    
if __name__ == '__main__':
    propogate()
