import json
import time
from paho.mqtt import client as mqtt_client


# Configuration
broker = 'your_broker_ip'
# This should match with MQTT broker configuration
port = 8883  
topic = "sensor/data"
client_id = 'pico_unique_id'
# Assuming the path to your JSON file
json_file_path = "variable_data.json"

# Global variable to store the last published data
last_published_data = None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    #dealing with the received data code to be here

def setup_mqtt():
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    # MQTT broker requires username and password
    # client.username_pw_set(username, password)
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def read_json_file(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to read file: {e}")
        return None

def main():
    client = setup_mqtt()
    client.loop_start()

    global last_published_data
    current_data = read_json_file(json_file_path)

    while True:
        if current_data != last_published_data:
            publish(client, topic, json.dumps(current_data))
            last_published_data = current_data
        time.sleep(5)  # Check for updates every 5 seconds

if __name__ == "__main__":
    main()