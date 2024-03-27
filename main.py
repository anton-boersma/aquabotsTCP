import paho.mqtt.client as mqtt
import csv
from time import time, strftime
from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading

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

# TCP variables
HOST = ""  # intentionally left blank, functions as a filter
PORT = 2345  # port used to communicate over
message_length = 128  # length of message in ASCII characters


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


def mqtt_thread():
    # Setup MQTT client
    client = mqtt.Client(client_id=mqtt_client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    # Set username and password for MQTT authentication
    client.username_pw_set(username=mqtt_username, password=mqtt_password)

    client.connect(mqtt_broker, mqtt_port, mqtt_keepalive)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("disconnecting")
        client.disconnect()
        exit()


def tcp_thread():
    # Setup TCP server
    with Socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Listening on port {PORT}")
        while True:
            connection, address = server_socket.accept()
            with connection:
                print(f"Connected to {address}")
                while True:
                    data = connection.recv(message_length)
                    if not data:
                        print("Disconnected")
                        break
                    content = data.decode("utf-8")
                    # parts = content.split(":")
                    # topic = parts[0]
                    # value = parts[1]
                    print(f"Received: {content}")
                    connection.sendall(data)
                    print("Responded")


if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=mqtt_thread)
    tcp_thread = threading.Thread(target=tcp_thread)

    mqtt_thread.start()
    tcp_thread.start()

    mqtt_thread.join()
    tcp_thread.join()
