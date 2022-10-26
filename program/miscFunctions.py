import json
import os 

def randomCheck(value):
    try:
        if not value.lower() == 'random':
            return False
        return True
    except:
        return False

def readConfig():
    with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json')) as f:
            data = json.load(f)
    return data 

def writeConfig(data):
    with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'),'w') as file:
        json.dump(data, file)
