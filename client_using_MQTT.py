import json
import time
import ssl

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import CallbackAPIVersion


# looad configuration from external file
def load_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        return json.load(file)

config = load_config()

# declaring global variable to store the last published data
last_published_data = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection Extablished")
    else:
        print(f"Failed to connect, return code {rc}\n")
    client.subscribe(config['topic'])

def on_message(client, userdata, msg):
    for i in range(101): print("_", end="")
    print(f"""
          Received:
           MESSAGE: `{msg.payload.decode()}`
            TOPIC: `{msg.topic}`""")
    for i in range(101): print("_", end="")

    # Decode the message payload
    message_data = msg.payload.decode()

    # Assuming message_data is a JSON string, load it into a Python dictionary
    try:
        data = json.loads(message_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Write the data to variable_data.json
    try:
        with open("variable_data.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Data written to variable_data.json")
    except Exception as e:
        print(f"Error writing to file: {e}")

def setup_mqtt(config):
    #client = mqtt_client.Client(config["client_id"])
    """This is a TEMPORARY PATCH, as the updated library would require a lot of rewriting to move to version 2.0"""
    client = mqtt_client.Client(client_id=config["client_id"], callback_api_version=CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message
    """
    # setting TLS for secure connection
    client.tls_set(ca_certs=config["ca_cert_path"], tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)  # currently insecure, for testing. set to false to confirm certifications.
    """
    client.connect(config["broker"], config["port"])
    return client

#publishing the data to the server.
def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        for i in range(101): print("_", end="")
        print(f"""
              Messsage Sent LOG.
              TOPIC: {topic}
              MESSAGE: {msg}
              """)
        for i in range(11): print("______", end="X")
        print("")
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
        time.sleep(2)  # Check for updates every 5 seconds

if __name__ == "__main__":
    main()
