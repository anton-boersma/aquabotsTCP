# This file is used as a base for the TCP server, Wessel provided this file

from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
HOST = ""
PORT = 2345

# multi threading, 1 voor MQTT, 1 voor TCP
# per thread lezen en wegschrijven
# voorbeeldnaam mqtt_tcp_relay

if __name__ == "__main__":
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
                    data = connection.recv(4)
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
