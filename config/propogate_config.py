import json

# load info from global configuration
configInput = open('global_config.json', 'r')
print(configInput.read())
inputDict = json.load(configInput)
configInput.close()

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
outputFile.close