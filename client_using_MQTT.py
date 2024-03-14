from umqtt.simple import MQTTClient
import network
import ujson as json
import time

# Configuration
ssid = 'your_ssid'
password = 'your_password'
mqtt_broker = 'your_broker_ip'
client_id = 'pico_unique_id'  # unique for each device
topic = 'sensor/data'  # publishing topic

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

# Setup for MQTT client and connection
def setup_mqtt():
    client = MQTTClient(client_id, mqtt_broker)
    client.set_callback(sub_callback)
    client.connect()
    client.subscribe(topic.encode())  # Ensure topic is a byte string
    print(f"Connected to {mqtt_broker}, subscribed to {topic} topic")
    return client

# Main function
def main():
    connect_to_wifi(ssid, password)
    client = setup_mqtt()

    while True:
        # this is the place to publish data if this client acts as a sensor node
        # Example: client.publish(topic.encode(), json.dumps({"temperature": 22.5}).encode())
        
        # checking for new messages on subscribed topics
        client.check_msg()
        time.sleep(5)

if __name__ == "__main__":
    main()
