#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging
from functools import partial
from datetime import datetime
import time
from threading import Thread, Lock
# import import_ipynb
import data
import webbrowser
import threading
import socket
import pandas as pd

_LOGGER = logging.getLogger(__name__)

from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.palettes import Category10
from bokeh.models import WheelZoomTool, PanTool, Div

data_source = {}
data_lock = Lock()

def get_information(args):
    #with data_lock:
    for ip in args.ip_list:
        info_dict = {}
        _LOGGER.info(f"getting name for {ip}")
        info_dict["name"] = data.get_name(args, ip)
        _LOGGER.info(f"getting color for {ip}")
        info_dict["color"] = data.get_wled_color(args, ip)
        _LOGGER.info(f"getting uptime for {ip}")
        info_dict["uptime"] = data.get_uptime(args, ip)
        
        # Ensure the IP key in data_source has both info_dict and an empty ping_dict
        data_source[str(ip)] = {
            "info_dict": info_dict,
            "ping_dict": {}
        }

def get_ping_information(args):
    for ip in args.ip_list:
        duration = args.args.time
        start_time = datetime.now()
        time_fly = 0
        ping_count = 0
        ping_dict = data_source[str(ip)]["ping_dict"]
        while (time_fly < duration):
            _LOGGER.info(f"getting ping info for {ip}")
            result = data.get_ping(args, ip)
            ping_count += 1
            running_dict = {}
            running_dict["speed"] = result["speed"]
            running_dict["start_time"] = result["send_time"]
            running_dict["end_time"] = result["receive_time"]
            ping_dict[f"ping_{ping_count}"] = running_dict
            # Update time_fly to the current elapsed time
            time_fly = (datetime.now() - start_time).total_seconds()
        ping_dict["ping_count"] = ping_count
        if ip in data_source:
            data_source[str(ip)]["ping_dict"] = ping_dict
        else:
            #if the IP was not added, add it
            data_source[str(ip)] = {
                "info_dict": {},
                "ping_dict": ping_dict
            }

def display(args):
    get_information(args)
    get_ping_information(args)
    for ip in args.ip_list:
        combined_data = {}
        combined_data["IP"] = []
        combined_data["IP"].append(str(ip))
        combined_data["ping_count"] = []
        combined_data["start_end_time"] = []
        combined_data["start_time"] = []
        combined_data["end_time"] = []
        combined_data["speed"] = []
        combined_data["orb_name"] = []
        combined_data["color"] = []
        combined_data["uptime"] = []
        information_dict = data_source[str(ip)]["info_dict"]
        pinging_dict = data_source[str(ip)]["ping_dict"]
        orb_name = information_dict["name"]
        combined_data["orb_name"].append(orb_name)
        color = information_dict["color"]
        combined_data["color"].append(color)
        uptime = information_dict["uptime"]
        combined_data["uptime"].append(uptime)
        num_ping = pinging_dict["ping_count"]
        for i in range(1, num_ping + 1):
            combined_data["ping_count"].append(i)
            start_time = pinging_dict[f"ping_{i}"]["start_time"]
            end_time = pinging_dict[f"ping_{i}"]["end_time"]
            speed = pinging_dict[f"ping_{i}"]["speed"]
            combined_data["start_time"].append(start_time)
            combined_data["end_time"].append(end_time)
            combined_data["start_end_time"].append(f"{start_time} -> {end_time}")
            combined_data["speed"].append(speed)
        # Convert start_end_time to a categorical type
        combined_data["start_end_time"] = pd.Categorical(combined_data["start_end_time"])
        _LOGGER.info(f"getting graph info for {ip}")
        source = ColumnDataSource(data=combined_data)
        p = figure(title="Ping Speed Graph", x_axis_label='Start-End Time', y_axis_label='Ping Speed (ms)', 
                x_range=combined_data["start_end_time"].categories)
        p.circle('start_end_time', 'speed', size=10, color="red", source=source, legend_field='IP')
        
        hover = HoverTool()
        hover.tooltips = [
            ("IP", "@IP"),
            ("Name", "@orb_name"),
            ("Color", "@color"),
            ("Uptime", "@uptime"),
            ("Start Time", "@start_time"),
            ("End Time", "@end_time"),
            ("Start-End Time", "@start_end_time"),
            ("Ping Speed", "@speed ms"),
        ]
        p.add_tools(hover)
        show(p)
#DID:
"""
- Đã lấy được thông tin của mỗi IP
- Đã ping được trong 1 amount of time
- Lưu trữ các thông tin về từng ping một trong dict
"""
#TO-DO:
"""
- Hiển thị data lên bokeh
- Thực hiện flag: -g --> hiển thị graph, -a --> hiển thị table
- Graph sẽ có dạng: x-axis thì là khoảng thời gian 
                    từ lúc gửi đến lúc nhận ping --> string
                    y-axis thì là speed của ping
                    Nếu request timed out --> để là 0 hoặc cái gì đó khác (hiện tại đang để ip nan chưa có mục đích)
                    Point-to-point graph, khi bấm vào (hover) phải hiển thị ra các thông tin khác (ví dụ như trong info_dict)
- Table sẽ có dạng csv, bố cục dict thế nào thì trình bày table như thế
- Sau khi đã xong hết nghiên cứu xem có thể thu được live data không.
"""

