# Simple MQTT Dashboard

## A simple usage of MQTT and Streamlit to show sensor data in almost real-time
This project is an experimentation of mine, as the first ever usage of MQTT in my own study. This project help me understand the making of a very simple data pipeline that retrieve data from hardware, publish it through a communication protocol, stores it on database, and display it on browser. The features detail is as follow,
- Retrieving data from DHT11 temperature & humidity sensor
- Persistence using SQLite3 database
- Subcribe and Publish on MQTT Communication using public EMQX broker
- A neat simple dashboard using Streamlit to show data metric with graph
- Controllable LED via button on dashboard

## Final Product
<img width="320" height="241" alt="image" src="https://github.com/user-attachments/assets/4512399d-e395-4d16-9fc5-da792852e972" />
<img width="1618" height="1038" alt="Screenshot 2026-03-28 091108" src="https://github.com/user-attachments/assets/95e31657-e85e-4b71-88b2-57e201693b30" />

## Planning Stuff Detail
### Data Flow Diagram
The following are data flow diagram that I use to make this project,
<img width="1725" height="419" alt="image" src="https://github.com/user-attachments/assets/af0bd3b3-df4e-48e9-9f50-85b66a95ae6d" />

### Hardware
#### Components
- Wemos D1 Mini (ESP8266)
- DHT11 Temperature & Humidity Sensor
- LED
- 10K Resistor
- Breadboard
- Some jumper and solid core cables

#### Schematic
<img width="896" height="800" alt="circuit_image_new" src="https://github.com/user-attachments/assets/ebd193f9-41ff-4985-944e-2a5d1035fa55" />

### Dashboard
This is the initial layout design of the dashboard made with Excalidraw on Obsidian,
<img width="751" height="550" alt="image" src="https://github.com/user-attachments/assets/78a7dc54-d3a0-4414-bcfc-291059a5063a" />

The design is mainly made with Streamlit with the help of Streamlit-autorefresh, Altair, and Pandas library.

The choosen layout is the first one. My intention on this design is to make a simple and readable dashboard that shows temperature and humidity data. It shows the current-latest data on the top, and use graph to allow user to see the trend of past data on the bottom. I also just wanted to use the multi-tab feature of Streamlit for a more compact view.

There's also a button to turn ON/OFF LED to also test if Streamlit can also be used to control other component of the project.
## How To Use
### Hardware Side
First, the schematics need to be made on the real components. Then, import the `root/Hardware/Simple MQTT Dashboard Project/` directory to PlatformIO. Simply upload the firmware to the board, and see the Serial Monitor for detailed information on the process. Don't forget to make sure the dependencies is installed. Oh also suit the WiFi SSID and Password to suit yours on `main.cpp`

### Software Side
The following is how to install dependencies and run the dashboard and the backend,
1. Navigate to `root/Software/` directory
2. Create a python virtual environment using `python -m venv .venv`
3. Install dependencies using `pip install -r requirements.txt`. Yes, to see what libraries I use for the software, just open the `requirements.txt` file
4. Navigate to `config.py`
5. Change the MQTT configuration variables to suit your own MQTT broker. Make sure there's 2 distinct topic: `.../sensor` and `.../led`
6. **Running The program**
	1. To run the program, the Hardware need to be ready to use (as in connected to WiFi and suceed on connecting to MQTT broker). See the previous section for hardware side usage
	2. Then run the backend using `python main.py`. It'll start create a `.db` file on `Software/database/` directory (if not already present), and start to subscribe to `.../sensor` MQTT topic
	3. After that run the dashboard using `streamlit run dashboard.py`
7. On the Streamlit Dashboard, you can see the latest temperature & humidity, the delta, and the graph of the past 10 latest data
8. To change the LED state, simply click the LED Button on the third column on the top, it'll show the current LED state too

When you start everything right, and monitor each of the component, there should be three terminal opened: one for PlatformIO, one for backend, and one for dashboard.
### Final File Tree
```tree
.
└── root/
    ├── Software/
    │   ├── .venv/
    │   ├── src/
    │   │   ├── database/
    │   │   │   ├── data.db
    │   │   │   └── db.py
    │   │   └── mqtt/
    │   │       ├── publisher.py
    │   │       └── subscriber.py
    │   ├── .gitignore
    │   ├── config.py
    │   ├── dashboard.py
    │   ├── main.py
    │   └── requirements.py
    ├── Hardware/Simple MQTT Dashboard Project/
    │   ├── lib/
    │   ├── include/
    │   ├── src/
    │   │   └── main.cpp
    │   ├── test/
    │   ├── .gitignore
    │   └── platformio.ini
    └── README.md
```
## Known Issues
1. Sometimes there's a weird sychronization issue on the dataframe retrieval on the dashboard where it seems to retrieve less than 10 piece of record on certain refreshes. It can be seen on the graph itself. Though I'm never checked the dataframe tab when this happens, as it's pretty rare condition
2. WiFi on the ESP8266 MCU only support 2.4 GHz AP Frequency. So if the board having difficulty when searching the WiFi connection, consider configuring your WiFi or Hotspot provider
3. When setting up the project, sometimes the LED doesn't update to its initial state that's given by `main.py` on `publish_init()` function

## Potential Improvement
1. I think it's a good dea to make the hardware portable by using batteries
2. I also think it's a very good idea to make somekind of all-in-one script to set-up everything and also start it. Though, at my current level, I don't know anything about that yet

## Resources
The following are the resources that I used to make and learn this particular project,
- [How to use MQTT in Python - EMQX](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)
- [Paho MQTT's Getting Started](https://pypi.org/project/paho-mqtt/#getting-started)
- [SQLite3 Python API Documentation](https://docs.python.org/3/library/sqlite3.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Autorefresh Component - kmcgrady on Github](https://github.com/kmcgrady/streamlit-autorefresh)
- [DHT Sensor Library - Adafruit on Github](https://github.com/adafruit/dht-sensor-library?tab=readme-ov-file)
- [Arduino JSON](https://arduinojson.org/)
- [PubSubClient Documentation](https://pubsubclient.knolleary.net/)
