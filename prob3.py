import time
import datetime
import argparse
import netaddr
from OuiLookup import OuiLookup

import sys
import logging

from scapy.all import *

from pprint import pprint


#from logging.handler import RotatingFileHandler
from logging.handlers import RotatingFileHandler

NAME = 'probemon'
DESCRIPTION = "a command line tool for logging 802.11 probe request frames"

DEBUG = True

def build_packet_callback(time_fmt, logger, delimiter, mac_info, ssid, rssi):
    def packet_callback(packet):
        
        if not packet.haslayer(Dot11):
            print("some other signal")

            return

        # we are looking for management frames with a probe subtype
        # if neither match we are done here
        if (packet.type != 0) or (packet.subtype != 0x04):
            print("other type of frame")
            return

        # list of output fields
        fields = []

        # determine preferred time format 
        log_time = str(int(time.time()))
        if time_fmt == 'iso':
            log_time = datetime.now().isoformat()

        

        

        # parse mac address and look up the organization from the vendor octets
        if mac_info:
            parsed_mac = netaddr.EUI(packet.addr2)
            #parsed_mac.dialect = mac_unix
        
            try:
                man = list(OuiLookup().query(str(packet.addr2))[0].values())[0]
                fields.append(log_time)
                # append the mac address itself
                fields.append(packet.addr2)
                if man is not None:
                    fields.append(man)
                else:
                    fields.append("UNKNOWN")
            except :
                fields.append('UNKNOWN')
                       
            # man = list(OuiLookup().query(str(packet.addr2))[0].values())[0]
            # fields.append(log_time)
            # # append the mac address itself
            # fields.append(packet.addr2)
            # fields.append(man)


        # include the SSID in the probe frame
        if ssid:
            fields.append(packet.info)
            
        if rssi:
    
            rssi_val = -(256-ord(packet.notdecoded[-2:-1]))
            #rssi_val = " ".join([str(ord(x)) for x in packet.notdecoded])

            fields.append(str(rssi_val))
            

        logger.info(delimiter.join(fields))

    return packet_callback

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-i', '--interface', help="capture interface")
    parser.add_argument('-t', '--time', default='iso', help="output time format (unix, iso)")
    parser.add_argument('-o', '--output', default='probemon.log', help="logging output location")
    parser.add_argument('-b', '--max-bytes', default=5000000, help="maximum log size in bytes before rotating")
    parser.add_argument('-c', '--max-backups', default=99999, help="maximum number of log files to keep")
    parser.add_argument('-d', '--delimiter', default='\t', help="output field delimiter")
    parser.add_argument('-f', '--mac-info', action='store_true', help="include MAC address manufacturer")
    parser.add_argument('-s', '--ssid', action='store_true', help="include probe SSID in output")
    parser.add_argument('-r', '--rssi', action='store_true', help="include rssi in output")
    parser.add_argument('-D', '--debug', action='store_true', help="enable debug output")
    parser.add_argument('-l', '--log', action='store_true', help="enable scrolling live view of the logfile")
    args = parser.parse_args()

    if not args.interface:
        print ("error: capture interface not given, try --help")
        sys.exit(-1)
    
    DEBUG = args.debug

    # setup our rotating logger
    logger = logging.getLogger(NAME)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(args.output, maxBytes=args.max_bytes, backupCount=args.max_backups)
    logger.addHandler(handler)
    if args.log:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    built_packet_cb = build_packet_callback(args.time, logger, 
        args.delimiter, args.mac_info, args.ssid, args.rssi)
    sniff(iface=args.interface, prn=built_packet_cb, store=0)

if __name__ == '__main__':
    main()