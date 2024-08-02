#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Build an args analyzer:
import logging     #used to log messsages (and maybe store that in a file or give it straight to the terminal)
import argparse
import ipaddress

_LOGGER = logging.getLogger(__name__)

def process_ip_from_file(file_name):
    ip_list = []
    with open(file_name,'r') as file:
        for line in file:
            ip_list.append(line.strip())
    print(ip_list)
    #if there is at lease one ip address in the list:
    if not file_name:
        raise argparse.ArgumentTypeError("There needs to be a file of IP address to process")
    if (len(ip_list) == 0):
        raise argparse.ArgumentTypeError("There needs to be at least one IP address")
    #convert each of the ip address in the list to be ip object:
    ip_object = []
    for ip_str in ip_list:
        try:
            ip_object.append(ipaddress.IPv4Address(ip_str.strip()))
        except ipaddress.AddressValueError:
            #raise when there is an error with a value of an ip address
            raise argparse.ArgumentTypeError(f"here is an invalid ip address: {ip_str}")
    #sort the list by the ip address:
    ip_object.sort()
    return ip_object

def process_fields(input_string):
    #split the string by the comma
    tokens = input_string.split(',')
    #replace the spaces with underscores in each token
    processed_tokens = []
    for token in tokens:
        token = token.strip().replace(' ', '_')
        processed_tokens.append(token)
    return processed_tokens

#define an args class:
class Args:
    args = None
    ip_list = None
    param = None
    
    def __init__(self):
        self.parse_args()
        self.ip_list = process_ip_from_file(self.args.filename)
        _LOGGER.info(f"IP addresses are {self.ip_list}")
    
    def parse_args(self):
        parser = argparse.ArgumentParser(
            description = "A Testing method for Orb Restarting"
        )
        parser.add_argument(
            "-f",
            "--file",
            dest = "filename",
            help = "The file that contains the list of IP Address",
            required = True,
            type = str,
        )
        parser.add_argument(
            "-t",
            "--time-period",
            dest = "time",
            help = "Period of time to poll WLED Orbs",
            default = 5,
            type = float,
        )
        # parser.add_argument(
        #     "-r",
        #     "--rollover",
        #     dest = "rollover",
        #     help = "int value to rollover the points default is 20000",
        #     default = 20000,
        #     type = int,
        # )
        # parser.add_argument(
        #     "-g",
        #     "--graph",
        #     dest = "graph",
        #     help = "Display graph of the ping",
        #     action = "store_true",
        # )
        # parser.add_argument(
        #     "-a",
        #     "--table",
        #     dest = "table",
        #     help = "Display table of the dead interval",
        #     action = "store_true",
        # )
        self.args = parser.parse_args()

