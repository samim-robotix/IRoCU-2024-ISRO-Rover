import cv2
import socket
import struct
import threading

# Predefined server IP and ports
SERVER_IP = '127.0.0.1'
MESSAGE_PORT = 9998
VIDEO_PORT = 9999

class CommunicationClient:
    def __init__(self, server_ip, message_port, video_port):
        self.server_ip = server_ip
        self.message_port = message_port
        self.video_port = video_port

    def start(self):
        threading.Thread(target=self.start_message_client).start()
        threading.Thread(target=self.start_video_client).start()

    def start_message_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.message_port))
        print(f"Connected to message server {self.server_ip}:{self.message_port}")

        send_thread = threading.Thread(target=self.send_data, args=(client_socket,))
        receive_thread = threading.Thread(target=self.receive_data, args=(client_socket,))
        
        send_thread.start()
        receive_thread.start()
        
        send_thread.join()
        receive_thread.join()
        client_socket.close()

    def send_data(self, client_socket):
        while True:
            message = input("Enter message to send to server: ")
            client_socket.send(message.encode())

    def receive_data(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Received from server: {message}")
            except:
                break

    def start_video_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.video_port))
        print(f"Connected to video server {self.server_ip}:{self.video_port}")
        
        receive_thread = threading.Thread(target=self.receive_video, args=(client_socket,))
        receive_thread.start()
        receive_thread.join()
        client_socket.close()

    def receive_video(self, client_socket):
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
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    client = CommunicationClient(SERVER_IP, MESSAGE_PORT, VIDEO_PORT)
    client.start()
