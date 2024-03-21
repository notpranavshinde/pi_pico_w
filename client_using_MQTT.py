import json
import time
import ssl
from paho.mqtt import client as mqtt_client

# looad configuration from external file
def load_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        return json.load(file)

config = load_config()

# declaring global variable to store the last published data
last_published_data = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

def setup_mqtt(config):
    client = mqtt_client.Client(config["client_id"])
    client.on_connect = on_connect
    client.on_message = on_message
    
    # setting TLS for secure connection
    client.tls_set(ca_certs=config["ca_cert_path"], tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)  # currently insecure, for testing. set to false to confirm certifications.
    
    client.connect(config["broker"], config["port"])
    return client

#publishing the data to the server.
def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

#reading the json fie of variables.
def read_json_file(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to read file: {e}")
        return None

def main():
    client = setup_mqtt(config)
    client.loop_start()

    global last_published_data

    while True:
        current_data = read_json_file(config["json_file_path"])
        if current_data != last_published_data:
            publish(client, config["topic"], json.dumps(current_data))
            last_published_data = current_data
        time.sleep(5)  # Check for updates every 5 seconds

if __name__ == "__main__":
    main()
