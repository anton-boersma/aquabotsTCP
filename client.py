from socket import socket as Socket
from socket import AF_INET, SOCK_STREAM
HOST = "localhost" # localhost zometeen
PORT = 2345

if __name__ == "__main__":
    with Socket(AF_INET, SOCK_STREAM) as socket:
        print(f"Connecting to {HOST}:{PORT}")
        socket.connect((HOST, PORT))
        print("Connected")
        print("Sending data")
        socket.sendall(b"Hello, World!")
        print("Sent data")
        print("Receiving data")
        data = socket.recv(128);
        content = data.decode("utf-8")
        print(f"Received: {content}")

