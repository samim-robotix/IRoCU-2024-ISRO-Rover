import socket
import threading

host = "192.168.1.20"
message_port = 9996
telemetry_port = 9997
webcam_port = 9998
depthcam_part = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

message_socket = server_socket.bind((host, message_port))

server_socket.listen(0)

print(f"Message server listening on port {message_port}")


def server_init():
    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepeted client on addr {client_address}")

    return client_socket
    
def send_message(client_socket, message):
    print(f"Message sent: \n{message}")
    client_socket.send(message.encode())
    
def receive_data(client_socket):
    while True:
        received_data = client_socket.recv(1024)
        print("Received:\n", received_data.decode())
        if(received_data == "exit"): client_socket.close()
        if received_data : return str(received_data.decode()).upper()

