import cv2
import socket
import struct
import pickle
import threading

# Predefined ports
MESSAGE_PORT = 9998
VIDEO_PORT = 9999

# Messaging
def handle_client_message(client_socket):
    send_thread = threading.Thread(target=send_data_to_client, args=(client_socket,))
    send_thread.start()

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received from client: {message}")
            if message == "0000":
                print("Closing connection upon client's request...")
                break
        except:
            break

    send_thread.join()
    client_socket.close()

def send_data_to_client(client_socket):
    while True:
        try:
            response = input("Enter response for client: ")
            client_socket.send(response.encode())
        except:
            break

def start_message_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Message server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted message connection from {addr}")
        client_handler = threading.Thread(target=handle_client_message, args=(client_socket,))
        client_handler.start()

# Video Streaming
def send_video_to_client(client_socket):
    cap = cv2.VideoCapture(0)  # Open the default webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        data = pickle.dumps(frame)
        message_size = struct.pack("L", len(data))
        try:
            client_socket.sendall(message_size + data)
        except:
            break
    cap.release()

def start_video_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Video server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted video connection from {addr}")
        video_handler = threading.Thread(target=send_video_to_client, args=(client_socket,))
        video_handler.start()

if __name__ == "__main__":
    threading.Thread(target=start_message_server, args=(MESSAGE_PORT,)).start()
    threading.Thread(target=start_video_server, args=(VIDEO_PORT,)).start()
