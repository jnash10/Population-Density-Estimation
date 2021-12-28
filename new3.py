import time

from queue import Queue

import logging

import thingspeak

q = []


start_time = time.time()


count_hash = {}

logfile = open('wifiscanner.log','r')



def get_macs(lines):
    macs = []
    for line in lines:
        macs.append(line.strip("\n")[52:69])
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
        top = q[0]
        if curtime - top[1] > footprint:
            count_hash[top[0]]-=1
            q.pop(0)
            if count_hash[top[0]]==0:
                removed+=1
        else:

            return removed
            break

footprint = 60*7

logging.basicConfig(filename='unqiuedevs.log', format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

channel = thingspeak.Channel(id = 1618535, api_key = 'B0BJI8HGQ4ZXY8DQ' )

while True:
    time.sleep(1)
    print("queue length",len(q))
    curtime = time.time()
    added = add_new(curtime)
    removed = remove_old(curtime)
    
    unique = unique + added - removed
    print("unique: ",unique,"added: ",added, "removed: ", removed)
    logger.info("unique devices: "+str(unique))
    channel.update({'field1': unique, 'field2':footprint})

