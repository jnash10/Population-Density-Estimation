import subprocess
import os 
import time

while True:
    #subprocess.Popen(['rm','wifiscanner.log'])
    scanner = subprocess.Popen(['python3','start.py'])
    time.sleep(4)
    updater = subprocess.Popen(['python3','new3.py'])

    time.sleep(20*60)
    scanner.terminate()
    #updater.terminate()
