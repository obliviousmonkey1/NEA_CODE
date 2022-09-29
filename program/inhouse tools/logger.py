import os 
from datetime import datetime

# currently only does event logging 
# plan on requiring the user to make a json document in their project folder in order for the module to be more flexible 
# , changable and tailord to the users need

# params which would be specified in the json file
"""
constant variables:

CREDENTIALS # this would be a pointer to an enviromental variable, to make it more secure and make sure no user data is in the code
PATH 
TIME_FORMAT 
"""

class S:
    def __init__(self) -> None:
        pass


# for programs that constantly are running 
class ContinousLog(S):
    # local dump multi file 
    def logLDMF(self, reference:str="", additionalInfo=None, time:str=datetime.now().strftime("%y:%m:%H:%M:%S"), trackingID="add trackingID", path:str="") -> None:
        refTime = datetime.now().strftime("%H:%M:%S")
        f = open(f"{path}{trackingID}{refTime}.log","w")
        f.write(f"{reference}:{additionalInfo}:{time}")
        f.close()


    # local dump single file 
    # need to make it so os.listdir is in reference to a specific path 
    def logLDSF(self, reference:str="", additionalInfo=None, time:str=datetime.now().strftime("%y:%m:%H:%M:%S"), trackingID="add trackingID", path:str=""):
        try:
            all_files = os.listdir()
            fName = [i for i in all_files if trackingID in i and i.endswith('.log')]
            f = open(f"{path}{fName[0]}", "a")
            f.write(f"\n{reference}:{additionalInfo}:{time}")
            f.close()
        except:
            timeRef = datetime.now().strftime("%H:%M:%S")
            f = open(f"{path}{trackingID}-{timeRef}.log", "w")
            f.write(f"{reference}:{additionalInfo}:{time}")
            f.close()


# for programs that have an end
class DiscontinousLog(S):
    def __init__(self) -> None:
        self.holder = ""
    
    
    def log(self, reference:str="", additionalInfo=None, time:str=datetime.now().strftime("%y:%m:%H:%M:%S")) -> None:
        self.holder = self.holder + f"{reference}:{additionalInfo} : {time},"
    

    def localDump(self, trackingID:str, path:str="") -> None:
        f = open(f"{path}{trackingID}.log","w")
        f.write(self.holder[:-1])
        f.close()


if __name__ == "__main__": 
    S()


