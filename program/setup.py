import sys
import subprocess

modules = ['sqlite3','random','threading','pandas','matplotlib','itertools']

# need to find the module pip names  
for module in modules:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','sqlite3'])
    except:
        pass

