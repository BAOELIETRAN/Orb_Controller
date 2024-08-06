<p align="center">
  <img src="https://capsule-render.vercel.app/api?text=Orb%20Controller!🕹&animation=twinkling&type=waving&color=gradient&height=150"/>
  <b>Graph that display the testing pings on Orb 006</b>
</p>


# Orb_Controller
## Background:
Faculty at Oberlin College developed the “Environmental Orb”, a colored light that glows different colors depending how much electricity and water are being used in buildings in which it is installed.  Essentially the colors and pulsing patterns of lights displayed on the orb at a given time communicate how much electricity or water is being used by a building at the present time relative to typical use at this time of day. The orb was designed to display two are two color spectra:  red → yellow → green for electricity and pink → purple → aqua for water.  Each minute, the orb receives two numbers through wifi, one for electricity and one for water,  each with one of five values: 0, 1, 2, 3, or 4.   So, for example, if electricity use in the building were at the lowest possible level of use and water consumption was at the highest possible use, the orb would be send a 0 for electricity and a 4 for water.  The orb would respond by alternating between displaying a slowly pulsing green pattern (= lowest level of electricity use) and a rapidly pulsing aqua color (= highest level of water use).  To help distinguish between the two resources, electricity is represented by a heartbeat type of pulsing pattern and water by a shimmering type of pulse.  Over the years we have used several different types of hardware devices to convert the data signal into colored lights.  
## Status:
The Environmental Dashboard team is currently in the process of replacing Arduino-based hardware that controlled individually colored LED bulbs with ESP32 based hardware that controls strips of LED bulbs. Thus far, they have developed a program that uses an ESP32 board and the open-source WLED program to control and change the colors of WS2812B LED lights based on the stream of data that we send it over a network each minute. They can successfully send data to the LED lights. 
## Issues:
With the previous version of WLED, when the Orbs were restarted, they would be disconnected from the Internet. In order to connect them back to the Internet, Oberlin College faculty needed to do that manually, which was obviously time-consuming and labor-consuming. Therefore, the Environmental Dashboard team is installing a new version of WLED (WLED v2.0), which is believed to make the Orb connect back to the Internet automatically after restarting itself. 
According to the programmer of WLED v2.0, the Orbs that are installed with this program will be restarted after every 6 hours. Therefore, the team needs a tool that can help them monitor the Orbs to make sure that after 6 hours, the Orbs will be restarted and then reconnected to the Internet.
## General:
In order to test the Orb, I think the most optimized method is sending consecutive pings to the Orbs to monitor their status. If the Orbs are restarted and then reconnected to the Internet, the pings can not reach to the Orbs for a while, and then it can function normally.
And, of course, to ensure the test is successful, I think I need to visualize it in both ways, graph and table:
- In terms of the graph, I will visualize all the pings on the coordinate axes, with the y-axis being the speed of each ping, and the x-axis being the count of each ping.
- In terms of the table, I will take all the data of the pings and put that into a table.
## Implementation:
- Leveraging Poetry to generate a virtual environment and manage dependencies for this project.
- Utilizing Python and its libraries to send pings with a user-defined interval between each ping in a user-defined amount of time.
    - Each Ping will be displayed as a node on a graph using Bokeh.
    - By requesting JSON from the Orb, the node will have the color of the current Orbs' color.
    - If the Orbs are restarted --> they are disconnected from the Internet --> the Ping will be dead --> that Ping will be displayed with speed = 0 and as a red node on the Graph.
    - If the Orbs are reconnected to the Internet --> the color of the Orb will be orange, and the uptime field in the JSON file will be smaller.
    - Generating warnings every time the Orb can not be reached by ping and storing them in a log file named Error Log.
- Using HTML and CSS to display all of the Pings data for each IP on a table, coloring the Pings with abnormal activity.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d992b8f1-89d9-4a1a-b39f-66b832498676">
</p><br/>

## Set Up:
**Highly Recommended**: Installing Poetry to create a virtual environment and manage dependencies.
```bash
pip install poetry
```
```bash
poetry init
```
Create a virtual environment:
```bash
poetry install
```
To read the information about the virtual environment:
```bash
poetry env info
```
To bring the virtual environment into the current project folder:
- Delete the virtual environment at the following path:
  ```bash
  poetry env info -p
  ```
- Add the virtual environment into the folder:
  ```bash
  poetry config virtualenvs.in-project true
  poety install
  ```
- Run the virtual environment:
  ```bash
  poetry shell
  ```
  or
  ```bash
  .\venv\Scripts\activate
  ```
## Execution:
After installing poetry and generating the virtual environment, we execute the program:
```bash
python main.py -f file_name -t time_period -i interval -g isGraph? -a isTable?
```
-f --file: File that contains IP Addresses of testing Orbs<br/>
-t --time-period: Amount of time for pinging<br/>
-i --interval: Interval between each ping<br/>
-g --graph: Display the ping information on a graph<br/>
-a --table: Display the ping information on a table<br/>

After executing the code with the corresponding flags, the graph (or table) will be displayed on a browser. <br/>
**Remember**: Check the Error Log file to see the abnormalities of the pings.

## Further Implementation:
- Trying to collect and display live data.
- Using AI to scan for the data and notify users about ping abnormalities.
