# This file is used as a base for the MQTT connection, Jan provided this file

import paho.mqtt.client as mqtt  # make sure to use version 1.6.1
# import csv
from time import time, strftime

# MQTT settings
broker_address = "aquabots.tech"  # Replace with your MQTT broker's address
mqtt_username = "jan"  # Replace with your MQTT username
mqtt_password = "welkom01"  # Replace with your MQTT password
topics = [
    "aquastorm/eindmaas/modules/Rudder/0/outputs/button"  # knop van roer
]  # Replace with the topics you want to subscribe to

# Generate a unique filename based on a timestamp
timestamp = strftime("%Y%m%d%H%M%S")
# csv_filename = f"mqtt_data_{timestamp}.csv"


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
    
#     print(topic)
#     print(payload)
    transfer_message(topic, payload)

    # Write to CSV
#     with open(csv_filename, mode='a', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow([timestamp, topic, payload])
#         print(f"Logged: {timestamp}, {topic}, {payload}")


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Set username and password for MQTT authentication
    client.username_pw_set(username=mqtt_username, password=mqtt_password)

    client.connect(broker_address, 1883, 60)

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

    
    

