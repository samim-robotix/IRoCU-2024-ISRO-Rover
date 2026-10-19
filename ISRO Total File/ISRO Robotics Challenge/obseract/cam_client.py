import cv2
import socket
import struct
import pickle
import threading

# Predefined server IP and ports
SERVER_IP = '127.0.0.1'
MESSAGE_PORT = 9998
VIDEO_PORT = 9999

# Messaging
def send_data(client_socket):
    while True:
        message = input("Enter message to send to server: ")
        client_socket.send(message.encode())

def receive_data(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received from server: {message}")
        except:
            break

def start_message_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to message server {server_ip}:{server_port}")

    send_thread = threading.Thread(target=send_data, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    
    send_thread.start()
    receive_thread.start()
    
    send_thread.join()
    receive_thread.join()
    client_socket.close()

# Video Streaming
def receive_video(client_socket):
    data = b""
    payload_size = struct.calcsize("L")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def start_video_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to video server {server_ip}:{server_port}")
    
    receive_thread = threading.Thread(target=receive_video, args=(client_socket,))
    receive_thread.start()
    receive_thread.join()
    client_socket.close()

if __name__ == "__main__":
    threading.Thread(target=start_message_client, args=(SERVER_IP, MESSAGE_PORT)).start()
    threading.Thread(target=start_video_client, args=(SERVER_IP, VIDEO_PORT)).start()
