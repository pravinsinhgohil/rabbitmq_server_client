import paho.mqtt.client as mqtt
import random
import time

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "status_topic"

client = mqtt.Client()


def connect_func(client, userdata, flags, rc):
    print("Connected" + str(rc))


client.connect_func = connect_func

client.connect(MQTT_HOST, MQTT_PORT, 60)

try:
    while True:
        status_value = random.randint(0, 6)
        message = {"status": status_value}
        client.publish(MQTT_TOPIC, str(message))
        print(f"Sent msg: {message}")
        time.sleep(1)
except KeyboardInterrupt:
    pass

client.disconnect()
