#conditions: only keep :
#if column=2 is not unknown
#if column=3 < -70

import thingspeak
import time

channel = thingspeak.Channel(id = 1653570, api_key = 'AJ1AH5HRCRTN65SK' )

file = open("problog.csv","r")

#inititalise devices to 0
devices = 0
footprint = 4

#threshold RSSI value
rssi = -85

while True:
    #update on thingspeak
    try:
        channel.update({'field1': devices, 'field2':footprint})
    except:
        pass

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



