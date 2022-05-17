#conditions: only keep :
#if column=2 is not unknown
#if column=3 < -70

import thingspeak
import time
from datetime import datetime

channel = thingspeak.Channel(id = 1653570, api_key = 'B0BJI8HGQ4ZXY8DQ' )

file = open("problog.csv","r")

#inititalise devices to 0
devices = 0
footprint = 5

#threshold RSSI value
rssi = -85

while True:
    #update on thingspeak
    

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    try:
        channel.update({'field1': devices, 'field2':footprint, 'field3':current_time})
    except:
        print("update attempt failed\n devices: ",devices)

    #wait footprint minutes
    time.sleep(footprint*60)

    #read file again and update devices
    temp_dev = 0
    temp_table = set()
    lines = file.readlines()
    for line in lines:
        inputs = line.split(";")
        if (inputs[2] != "UNKNOWN") and (int(inputs[3])>rssi) and (inputs[1] not in temp_table):
            temp_table.add(inputs[1])
            temp_dev+=1
            print("added", line)
    devices = temp_dev
    print("devices: ",devices)



