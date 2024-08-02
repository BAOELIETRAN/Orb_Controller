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

_LOGGER = logging.getLogger(__name__)

from bokeh.plotting import figure, show, output_file, save
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Panel, Tabs, Div, Button, CustomJS
from bokeh.layouts import column, row

data_source = {}

def get_information(args):
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
        data_source[str(ip)]["ping_dict"] = ping_dict

def display(args):
    get_information(args)
    get_ping_information(args)

    for ip in args.ip_list:
        combined_data = defaultdict(list)

        information_dict = data_source[str(ip)]["info_dict"]
        pinging_dict = data_source[str(ip)]["ping_dict"]
        orb_name = information_dict["name"]
        color = information_dict["color"]
        uptime = information_dict["uptime"]
        num_ping = pinging_dict["ping_count"]

        for i in range(1, num_ping + 1):
            start_time = pinging_dict[f"ping_{i}"]["start_time"]
            end_time = pinging_dict[f"ping_{i}"]["end_time"]
            speed = pinging_dict[f"ping_{i}"]["speed"]

            combined_data["IP"].append(str(ip))
            combined_data["ping_count"].append(i)
            combined_data["start_time"].append(start_time)
            combined_data["end_time"].append(end_time)
            combined_data["start_end_time"].append(f"{start_time} -> {end_time}")
            combined_data["speed"].append(0 if np.isnan(speed) else speed)
            combined_data["orb_name"].append(orb_name)
            combined_data["color"].append(color)
            combined_data["uptime"].append(uptime)
            combined_data["point_color"].append('red' if np.isnan(speed) else "orange")

        # Convert start_end_time to a list of unique values
        combined_data["start_end_time"] = pd.Categorical(combined_data["start_end_time"])
        _LOGGER.info(f"Getting graph info for {ip}")

        source = ColumnDataSource(data=combined_data)

        p = figure(title="Ping Speed Graph", x_axis_label='Start-End Time', y_axis_label='Ping Speed (ms)', 
                x_range=list(combined_data["start_end_time"].categories))

        # Add both lines and points to the plot
        p.line('start_end_time', 'speed', source=source, line_width=2, line_color='blue', legend_field='IP')
        p.circle('start_end_time', 'speed', size=10, color='point_color', source=source, legend_field='IP')

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

def display_table(args):
    get_information(args)
    get_ping_information(args)

    # Initialize the HTML string with table headers
    html_content = """
    <html>
    <head>
        <title>Data Table</title>
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
        info_str = f"Name: {info_dict['name']}, Color: {info_dict['color']}, Uptime: {info_dict['uptime']}"

        # Prepare the ping data string from ping_dict
        ping_data_str = ""
        for i in range(1, ping_dict.get("ping_count", 0) + 1):
            ping_info = ping_dict.get(f"ping_{i}", {})
            ping_data_str += f"Ping {i}: Speed={ping_info.get('speed', 'N/A')} ms, " \
                             f"Start={ping_info.get('start_time', 'N/A')}, " \
                             f"End={ping_info.get('end_time', 'N/A')}\n"

        # Add a row to the HTML table
        html_content += f"""
            <tr>
                <td>{ip}</td>
                <td>{info_str}</td>
                <td><pre>{ping_data_str.strip()}</pre></td>
            </tr>
        """

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

#DID:
"""
- Đã lấy được thông tin của mỗi IP
- Đã ping được trong 1 amount of time
- Lưu trữ các thông tin về từng ping một trong dict
- Đã vẽ được graph cho từng IP một với y-axis là speed của từng ping,
    x-axis là thời gian đi và đến của từng ping
"""
#TO-DO:
"""
- Hiển thị data của nhiều ping lên bokeh bằng nhiều graph (khả năng cái này được rồi)
- Đổi size của plot:
https://www.youtube.com/watch?v=rHtQDLRb5O8#:~:text=Bokeh's%20Plot%20objects%20have%20various,calling%20the%20figure()%20function.
- Thực hiện flag: -g --> hiển thị graph, -a --> hiển thị table
- Table sẽ có dạng csv, bố cục dict thế nào thì trình bày table như thế
- Sau khi đã xong hết nghiên cứu xem có thể thu được live data không.
- Dùng poetry
"""

