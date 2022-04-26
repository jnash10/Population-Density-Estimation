import time

from queue import Queue

import logging

import thingspeak


from csv_logger import CsvLogger
q = []


start_time = time.time()


count_hash = {}

logfile = open('probemon.log','r')



def get_macs(lines):
    macs = []
    for line in lines:
        macs.append(line.strip("\n")[27:])
    return macs

unique=0


def add_new(curtime):
    added = 0
    newlines = logfile.readlines()
    macs = get_macs(newlines)

    for mac in macs:
        if mac in count_hash:
            count_hash[mac]+=1
        else:
            count_hash[mac]=1
        #print(count_hash[mac])
        if count_hash[mac]==1:
            added +=1
        q.append((mac,curtime))
    return added


def remove_old(curtime):
    removed = 0
    while True:
        try:
            top = q[0]
            if curtime - top[1] > footprint:
                count_hash[top[0]]-=1
                q.pop(0)
                if count_hash[top[0]]==0:
                    removed+=1
            else:

                return removed
                break
        except:
            return 0

footprint = 60*7

logging.basicConfig(filename='unqiuedevs.log', format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

channel = thingspeak.Channel(id = 1653570, api_key = 'AJ1AH5HRCRTN65SK' )




### setting up the csv logger 
filename = "log.csv"
level = logging.INFO
fmt = '%(asctime)s,%(message)s'
datefmt = '%Y/%m/%d %H:%M:%S'
custom_additional_level = ['agam']
header = ['date','devices','added','removed']

##creating the logger
csv_logger = CsvLogger(filename=filename, level= level, fmt=fmt, datefmt=datefmt,header=header,add_level_names=custom_additional_level)


while True:
    time.sleep(15)
    print("queue length",len(q))
    curtime = time.time()
    added = add_new(curtime)
    removed = remove_old(curtime)
    
    unique = unique + added - removed
    print("unique: ",unique,"added: ",added, "removed: ", removed)
    logger.info("unique devices: "+str(unique))

    csv_logger.agam([unique,added,removed])

    scaled = (100/320)(unique-40)    
    try:
        channel.update({'field1': scaled, 'field2':footprint})
    except:
        time.sleep(15)
        

