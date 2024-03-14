import json

class SensorDataHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def publish_sensor_data(self):
        
        sensor_data = {
            "joystick": 22.5,
            "lineear seitch": 60,
            "joystick y": 101.3
        }
        # conversion the sensor data to a JSON string
        sensor_data_json = json.dumps(sensor_data)
        
        # Publish the sensor data to the MQTT broker
        self.mqtt_client.publish("sensor/data", sensor_data_json)
