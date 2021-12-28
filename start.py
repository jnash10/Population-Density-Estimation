import os

os.system("sudo rm wifiscanner.log")
os.system("sudo airmon-ng start wlan1")
os.system("sudo python3 scanner.py")

