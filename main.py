import paho.mqtt.client as mqtt  # make sure to use version 1.6.1
import csv
from time import time, strftime
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# MQTT settings
mqtt_broker = "aquabots.tech"  # MQTT broker address
mqtt_username = "jan"  # MQTT username
mqtt_password = "welkom01"  # MQTT password
mqtt_client_id = "Anton"  # MQTT client-id
mqtt_port = 1883  # port used for MQTT broker
mqtt_keepalive = 60  # duration in [s] before connection is closed


topics = [
    "aquastorm/eindmaas/modules/Rudder/0/outputs/button"  # button on rudder module
]  # add topics in this list

# logging to CSV file
timestamp = strftime("%Y%m%d%H%M%S")
csv_filename = f"mqtt_data_{timestamp}.csv"


# MQTT methods
def transfer_message(topic, message):
    print(f"The value of {topic} is {message}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        for topic in topics:
            client.subscribe(topic)
    else:
        print(f"Failed to connect to MQTT broker with code {rc}")


def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    timestamp = int(time() * 1000)

    transfer_message(topic, payload)

    # write to CSV
    # with open(csv_filename, mode='a', newline='') as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     csv_writer.writerow([timestamp, topic, payload])
    #     print(f"Logged: {timestamp}, {topic}, {payload}")


if __name__ == '__main__':
    client = mqtt.Client(client_id=mqtt_client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    # Set username and password for MQTT authentication
    client.username_pw_set(username=mqtt_username, password=mqtt_password)

    client.connect(mqtt_broker, mqtt_port, mqtt_keepalive)

    # Create CSV file with header if it doesn't exist
    #     with open(csv_filename, mode='a', newline='') as csv_file:
    #         csv_writer = csv.writer(csv_file)
    #         csv_writer.writerow(["Timestamp", "Topic", "Value"])

    try:
        while True:
            client.loop_forever()
    except KeyboardInterrupt:
        print("disconnecting")
        client.disconnect()
        exit()

