# pi_pico_w
code for raspberry pi pico w

server.py ad client.py is using basic http

to use client using mqtt protocol, a cloud or self hosted server is to be set up. for more info go the official website for mosquitto protocol.

INSTRUCTIONS FOR NETWORKING AND RUNNING THE CODE TO CONTROL THE ROBOT:

Install Mosquitto MQTT Broker
Download Mosquitto: Go to the official Mosquitto website and download the latest version for your operating system.

Install Mosquitto: Follow the installation instructions on the website for your operating system. On Windows, this typically involves running the installer. On a Raspberry Pi (or any Debian-based system), you can install Mosquitto using:sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
Configure Mosquitto
Create a custom configuration file for Mosquitto, named mosquitto.conf, and insert the following configuration:
# Set the listener to port 1883 for MQTT (unencrypted)
listener 1883

# Allow anonymous connections
allow_anonymous true

# Enable verbose logging to the console/terminal
log_type all

# Specify the log file location (optional)
#log_dest file /path/to/mosquitto.log

# To also log to the terminal (optional)
#log_dest stdout


Run Mosquitto Server
Start the Mosquitto Server: Use the custom configuration file to start the server. On Windows or Linux, navigate to the directory where you've saved mosquitto.conf and run:
mosquitto -c mosquitto.conf
Network Configuration
Ensure the Raspberry Pi and the server running Mosquitto are on the same network.

Check the Server's IP Address: On a Windows machine, use:
ipconfig
Note the IP address for later use.

Update Client Configuration
Update config.json for client_using_MQTT.py: Ensure this file contains the correct IP address of the server and the port number (default 1883).
Run the MQTT Client
Open another terminal on your Windows machine and run:
python client_using_MQTT.py
This step assumes Python is installed and the script is ready to execute. The client will connect to the Mosquitto server and start sending updates based on variable_data.json.
Run Controller Code
In a separate terminal, run the controller code that updates variable_data.json to control the robot.
Prepare the Raspberry Pi
Ensure the Pi is on the same network.

SSH into the Pi:
ssh pi@<pi-ip-address>
Replace <pi-ip-address> with the actual IP address of your Raspberry Pi.

Update config.json on the Pi: Make sure it has the correct server IP and port number.

Navigate to your code directory on the Pi:
using cd commands
Activate Python Virtual Environment (if you're using one):
source myvenv/bin/activate
Ensure the config.json file on the Pi has a unique ID different from the client running on your Windows machine.

Run Your Robot Control Code
Finally, run the scripts that depend on variable_data.json to control the robot:
python robot_control_script.py
IMOORTANT STUFF:Double-check all network configurations, IP addresses, and port numbers to ensure connectivity.
Any deviation from the steps or errors in configuration files may result in failure to control the robot as intended.
It's crucial to have all devices on the same network to ensure seamless communication.
