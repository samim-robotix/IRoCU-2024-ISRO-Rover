#communication
import cv2
import socket
import struct
import threading

class VideoServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.client_sockets = []

    def send_video_to_client(self, client_socket):
        cap = cv2.VideoCapture(0)  # Open the default webcam
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = frame.tobytes()
            try:
                client_socket.sendall(struct.pack("L", len(data)) + data)
            except:
                break
        cap.release()
        client_socket.close()

    def start_video_server(self):
        self.server_socket.listen(5)
        print(f"Video server listening on port {self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted video connection from {addr}")
            self.client_sockets.append(client_socket)
            video_handler = threading.Thread(target=self.send_video_to_client, args=(client_socket,))
            video_handler.start()

    def close_video_server(self):
        for client_socket in self.client_sockets:
            client_socket.close()
        self.server_socket.close()
        print("Video server closed.")

class MessageServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client_message(self, client_socket):
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
        client_socket.close()

    def send_data_to_client(self, client_socket):
        while True:
            try:
                response = input("Enter response for client: ")
                client_socket.send(response.encode())
            except:
                break

    def start_message_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        print(f"Message server listening on port {self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted message connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client_message, args=(client_socket,))
            client_handler.start()

    def close_message_server(self):
        self.server_socket.close()
        print("Message server closed.")

class Server:
    def __init__(self, message_ip, message_port, video_ip, video_port):
        self.message_server = MessageServer(message_ip, message_port)
        self.video_server = VideoServer(video_ip, video_port)

    def start_servers(self):
        threading.Thread(target=self.message_server.start_message_server).start()
        threading.Thread(target=self.video_server.start_video_server).start()

    def close_servers(self):
        self.message_server.close_message_server()
        self.video_server.close_video_server()

    def close_on_keyboard_interrupt(self):
        try:
            while True:
                continue
        except KeyboardInterrupt:
            print("\nClosing servers...")
            self.close_servers()

# Example usage:
if __name__ == "__main__":
    MESSAGE_IP = '127.0.0.1'
    MESSAGE_PORT = 9998
    VIDEO_IP = '127.0.0.1'
    VIDEO_PORT = 9999

    server = Server(MESSAGE_IP, MESSAGE_PORT, VIDEO_IP, VIDEO_PORT)
    server.start_servers()

    # To close servers, send "0000" message from the client side.
    # To close servers via keyboard interrupt, press Ctrl+C in the terminal.
    server.close_on_keyboard_interrupt()
