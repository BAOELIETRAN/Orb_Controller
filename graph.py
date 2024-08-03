#!/usr/bin/env python
# coding: utf-8

# In[1]:

from collections import defaultdict
import logging
from datetime import datetime
import numpy as np
import data
import pandas as pd
import webbrowser
import os
import time

bold_red_yellow_bg = "\033[1;31;43m"
reset = "\033[0m"

_LOGGER = logging.getLogger(__name__)

from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource, FixedTicker, PrintfTickFormatter
from bokeh.layouts import gridplot
from bokeh.colors import RGB

data_source = {}

def get_information(args):
    for ip in args.ip_list:
        info_dict = {}
        _LOGGER.info(f"getting name for {ip}")
        info_dict["name"] = data.get_name(args, ip)
        # Ensure the IP key in data_source has both info_dict and an empty ping_dict
        data_source[str(ip)] = {
            "info_dict": info_dict,
            "ping_dict": {}
        }

def get_ping_information(args):
    interval = args.args.interval
    for ip in args.ip_list:
        duration = args.args.time
        start_time = datetime.now()
        time_fly = 0
        ping_count = 0
        ping_dict = data_source[str(ip)]["ping_dict"]
        while (time_fly < duration):
            _LOGGER.info(f"getting ping info for {ip}")
            running_dict = {}
            ping_count += 1
            result = data.get_ping(args, ip)
            running_dict["speed"] = result["speed"]
            running_dict["start_time"] = result["send_time"]
            running_dict["end_time"] = result["receive_time"]  
            uptime = data.get_uptime(args, ip)
            color = data.get_wled_color(args, ip)
            running_dict["color"] = color 
            running_dict["uptime"] = uptime
            ping_dict[f"ping_{ping_count}"] = running_dict
            # Update time_fly to the current elapsed time
            time_fly = (datetime.now() - start_time).total_seconds()
            time.sleep(interval)
            print(time_fly)
        ping_dict["ping_count"] = ping_count
        data_source[str(ip)]["ping_dict"] = ping_dict

def display(args):
    plots = []
    for ip in args.ip_list:
        combined_data = defaultdict(list)

        information_dict = data_source[str(ip)]["info_dict"]
        pinging_dict = data_source[str(ip)]["ping_dict"]
        orb_name = information_dict["name"]
        num_ping = pinging_dict["ping_count"]
        for i in range(1, num_ping + 1):
            start_time = pinging_dict[f"ping_{i}"]["start_time"]
            end_time = pinging_dict[f"ping_{i}"]["end_time"]
            speed = pinging_dict[f"ping_{i}"]["speed"]
            color = pinging_dict[f"ping_{i}"]["color"]
            uptime = pinging_dict[f"ping_{i}"]["uptime"]
            combined_data["IP"].append(str(ip))
            combined_data["ping_count"].append(i)
            combined_data["start_time"].append(start_time)
            combined_data["end_time"].append(end_time)
            combined_data["start_end_time"].append(f"{start_time} -> {end_time}")
            combined_data["speed"].append(0 if np.isnan(speed) else speed)
            combined_data["orb_name"].append(orb_name)
            combined_data["color"].append(color)
            combined_data["uptime"].append(uptime)
            # Set color based on speed
            if np.isnan(speed):
                combined_data["point_color"].append("#FF0000")  # Red color
            else:
                r, g, b = color
                combined_data["point_color"].append(RGB(r, g, b).to_hex())

        combined_data["start_end_time"] = pd.Categorical(combined_data["start_end_time"])
        
        source = ColumnDataSource(data=combined_data)
        
        p = figure(title=f"Ping Speed Graph for IP {ip}", x_axis_label='Ping Count', y_axis_label='Ping Speed (ms)', 
                   x_axis_type='linear')

        # Define tick locations (integers only)
        ticks = list(range(1, num_ping + 1))
        p.xaxis.ticker = FixedTicker(ticks=ticks)
        
        # Format ticks as integers
        p.xaxis.formatter = PrintfTickFormatter(format='%d')

        p.line('ping_count', 'speed', source=source, line_width=2, line_color='blue', legend_label=str(ip))
        p.circle('ping_count', 'speed', size=10, color='point_color', source=source, legend_label=str(ip))


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

        p.legend.title = "IP Address"
        p.legend.label_text_font_size = '10pt'
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        
        plots.append(p)

    # Create a grid layout for the plots
    grid = gridplot([plots], sizing_mode='stretch_both')

    show(grid)  # This will display all graphs arranged in a grid

def display_table(args):
    # Initialize the HTML string with table headers
    html_content = """
    <html>
    <head>
        <title>Data Table of IP</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .nan-speed {
                color: red;
                background-color: yellow;
                font-weight: bold;
                font-size: 1.2em;  /* Increase font size */
            }
        </style>
    </head>
    <body>
        <h2>Data Table</h2>
        <table>
            <tr>
                <th>IP</th>
                <th>Info</th>
                <th>Ping Data</th>
            </tr>
    """

    # Iterate over each IP in the data_source
    for ip in args.ip_list:
        info_dict = data_source[str(ip)]["info_dict"]
        ping_dict = data_source[str(ip)]["ping_dict"]

        # Prepare the info string from info_dict
        info_str = f"Name: {info_dict['name']}"

        # Prepare the ping data string from ping_dict
        ping_data_rows = []
        for i in range(1, ping_dict.get("ping_count", 0) + 1):
            ping_info = ping_dict.get(f"ping_{i}", {})
            speed = ping_info.get('speed', 'N/A')
            if isinstance(speed, float) and pd.isna(speed):  # Check if speed is np.nan
                row_class = 'nan-speed'
                speed = 'N/A'
            else:
                row_class = ''
                
            ping_data_row = f"""
                <tr class="{row_class}">
                    <td>Ping {i}</td>
                    <td>Speed={speed}, Start={ping_info.get('start_time', 'N/A')}, End={ping_info.get('end_time', 'N/A')}, Uptime={ping_info.get('uptime', 'N/A')}, Color={ping_info.get('color', 'N/A')}</td>
                </tr>
            """
            ping_data_rows.append(ping_data_row)
        # Add the rows to the HTML table
        html_content += f"""
            <tr>
                <td rowspan="{len(ping_data_rows) + 1}">{ip}</td>
                <td rowspan="{len(ping_data_rows) + 1}">{info_str}</td>
            </tr>
        """
        html_content += "\n".join(ping_data_rows)
    
    # Close the table and HTML tags
    html_content += """
        </table>
    </body>
    </html>
    """

    # Write HTML content to a file
    file_path = "data_table.html"
    with open(file_path, "w") as file:
        file.write(html_content)

    # Open the HTML file in the default web browser
    webbrowser.open(f"file://{os.path.abspath(file_path)}")


def warning(args):
    for ip in args.ip_list:
        ping_dict = data_source[str(ip)]["ping_dict"]
        ping_count = ping_dict["ping_count"]
        for num in range(1, ping_count+1):
            uptime_cur = ping_dict[f"ping_{num}"]["uptime"]
            color_cur = ping_dict[f"ping_{num}"]["color"]
            speed_ping = ping_dict[f"ping_{num}"]["speed"]
            cur_start_time = ping_dict[f"ping_{num}"]["start_time"]
            cur_end_time = ping_dict[f"ping_{num}"]["end_time"]
            if uptime_cur == None or color_cur == None or np.isnan(speed_ping) :
                # Trigger the flickering warning
                log = (f"Warning: Uptime and color difference detected for IP {ip} "
                           f"from {cur_start_time} to {cur_end_time}")
                message = (f"{bold_red_yellow_bg}Warning: Uptime and color difference detected for IP {ip} {reset}"
                           f"{bold_red_yellow_bg}from {cur_start_time} to {cur_end_time} {reset}")
                with open("Error Log.log", "a") as file:
                    file.write(log)
                    file.write("\n-------------------------------------------------------------------------------\n")
                print(message)    

