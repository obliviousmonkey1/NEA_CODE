import json
import os 


# checks if the value passed is equal to the word random
def randomCheck(value):
    try:
        if not value.lower() == 'random':
            return False
        return True
    except:
        return False


# reads a data from a json file
def readConfig():
    with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json')) as f:
            data = json.load(f)
    return data 


# writes data to a json file
def writeConfig(data):
    with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'),'w') as file:
        json.dump(data, file)
