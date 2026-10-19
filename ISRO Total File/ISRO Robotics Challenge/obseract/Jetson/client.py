import cv2
import socket
import struct
import threading
import numpy as np

class VideoClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_video(self):
        self.client_socket.connect((self.ip, self.port))
        data = b''
        payload_size = struct.calcsize("L")

        while True:
            while len(data) < payload_size:
                packet = self.client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += self.client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Received', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        self.client_socket.close()

class MessageClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self):
        self.client_socket.connect((self.ip, self.port))
        threading.Thread(target=self.receive_message).start()

        while True:
            try:
                message = input("Enter your message: ")
                self.client_socket.sendall(message.encode())
                if message == "0000":
                    print("Closing connection...")
                    break
            except:
                break

        self.client_socket.close()

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Received from server: {message}")
            except:
                break

# Example usage:
if __name__ == "__main__":
    MESSAGE_IP = '127.0.0.1'
    MESSAGE_PORT = 9998
    VIDEO_IP = '127.0.0.1'
    VIDEO_PORT = 9999

    video_client = VideoClient(VIDEO_IP, VIDEO_PORT)
    message_client = MessageClient(MESSAGE_IP, MESSAGE_PORT)

    threading.Thread(target=message_client.send_message).start()
    threading.Thread(target=video_client.receive_video).start()

    try:
        while True:
            continue
    except KeyboardInterrupt:
        print("\nClosing client sockets...")
        video_client.client_socket.close()
        message_client.client_socket.close()
