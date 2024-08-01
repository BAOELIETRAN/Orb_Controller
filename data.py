#!/usr/bin/env python
# coding: utf-8

# In[1]:


from urllib import request
import numpy
import requests
import logging
import subprocess
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

#get any param from JSON file from device
def get_param(args, ip, paths):
    result = []
    url = f"http://{ip}/json/info"
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()
    for path in paths:
        # Navigate through the JSON structure using each key in the path
        value = json_data
        for key in path:
            value = value.get(key)
            if value is None:
                # If any intermediate key is missing, break and append None
                result.append(None)
                break
        else:
            result.append(value)
    return result

#get each ping -> 1 ping with start time + end time
#will create a dict to store val:
# key: ip
# list of val: get_ping, get_uptime, get_color
def get_ping(args, ip):
    #ping the ip address
    #get the speed, sending time, receiving time
    #if the ping fails, return np.nan
    #--> this will cause a line break in the graph on bokeh
    result = {
        "speed": None,
        "send_time": None,
        "receive_time": None,
    }
    #Record the sending time
    send_time = datetime.now()
    result["send_time"] = send_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    try:
        #Execute the ping command
        ping_command = ["ping"] + ["-n", "1"] + [ip]
        ping_output = subprocess.run(ping_command, capture_output=True, text=True, timeout=5)
        
        #Record the receive time
        receive_time = datetime.now()
        result["receive_time"] = receive_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        
        #Parse the output to get the ping speed
        if ping_output.returncode == 0:
            for line in ping_output.stdout.split('\n'):
                if "time=" in line:
                    speed_str = line.split("time=")[-1].split()[0]
                    result["speed"] = float(speed_str.replace('ms', '').strip())
                    break
        else:
            result["speed"] = numpy.nan
            # result["speed"] = None
    except subprocess.TimeoutExpired:
        # Handle timeout scenario
        result["receive_time"] = (send_time + timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S.%f")
        result["speed"] = numpy.nan
        # result["speed"] = None
    return result
        
def get_name(args, ip):
    name = ""
    try:
        url = f"http://{ip}/json/info"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        name = json_data.get('name')
    except requests.exceptions.RequestException as e:
        _LOGGER.error(f"Error: {ip} : {e}")
        name = None
    return name

def get_uptime(args, ip):
    uptime = 0
    try:
        url = f"http://{ip}/json/info"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        uptime = json_data.get('uptime')
    except request.exceptions.RequestException as e:
        _LOGGER.error(f"Error: {ip} : {e}")
        uptime = None
    return uptime

def get_wled_color(args, ip):
    try:
        # Send GET request to WLED JSON API
        url = f"http://{ip}/json/state"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        json_data = response.json()
        
        # Extract the color values
        color = json_data.get('seg', [])[0].get('col', [[0, 0, 0]])[0]
        
        # Color is typically an RGB value
        r, g, b = color
        return r, g, b
    except Exception as e:
        print(f"Error fetching color: {e}")
        return None

