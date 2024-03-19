from umqtt.simple import MQTTClient
import network
import ujson as json
import time
import secrets

#configuring settings
ssid = secrets.ssid
password = secrets.password

mqtt_broker = 'your_broker_ip'
client_id = 'pico_unique_id'  # unique for each device
topic = 'sensor/data'  # publishing topic

#a variable to store last published data so that the same data is not published without any changes.


last_published_data = None
# connecting to wifi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())


# Setup for MQTT client and connection
def setup_mqtt():
    client = MQTTClient(client_id, mqtt_broker)
    client.set_callback(sub_callback)
    client.connect()
    client.subscribe(topic.encode())  # Ensure topic is a byte string
    print(f"Connected to {mqtt_broker}, subscribed to {topic} topic")
    return client

# MQTT callback function
def sub_callback(topic, msg):
    print(f"Received message on topic {topic}: {msg}")
    try:
        # Deserializing the JSON data
        data = json.loads(msg)
        print("Sensor Data:", data)
        # logic to handle the sensor data to be added here
    except Exception as e:
        print("Error processing message:", e)

# a function to open a json file and read the data in it. 
def read_json_file(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
        return data
    except OSError as e:
        print("Failed to read file:", e)
        return None
    
# a function to check if the data in the json file has changed from the last time it was published.
def has_data_changed(new_data, last_data):
    return new_data != last_data


#a function to publish new data if there is any
def publish_data(client, data):
    data_json = json.dumps(data)
    client.publish(topic.encode(), data_json.encode())
    print("Published new data.")


def main():
    connect_to_wifi(ssid, password)
    client = setup_mqtt()
    global last_published_data

    while True:
        #reading the json file
        current_data = read_json_file("variable_data")
        #checking for updates in data and publishing if any
        if current_data is not None and has_data_changed(current_data, last_published_data):
            publish_data(client, current_data)
            last_published_data = current_data
        time.sleep(5)

if __name__ == "__main__":
    main()
