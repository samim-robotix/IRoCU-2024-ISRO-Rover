import socket
import threading

# Server code
def handle_client(client_socket):
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

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Client code
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

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    send_thread = threading.Thread(target=send_data, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    
    send_thread.start()
    receive_thread.start()
    
    send_thread.join()
    receive_thread.join()
    client_socket.close()

# CLI interface
def main():
    mode = input("Enter 'server' to start as server, 'client' to start as client: ").strip().lower()
    if mode == 'server':
        port = int(input("Enter port to listen on: ").strip())
        start_server(port)
    elif mode == 'client':
        server_ip = input("Enter server IP: ").strip()
        server_port = int(input("Enter server port: ").strip())
        start_client(server_ip, server_port)
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")

if __name__ == "__main__":
    main()
