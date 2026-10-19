import socket

def start_client(host='192.168.1.20', port=9996):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    while True:
        try:
            # Receive the server's message
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                print("Server closed the connection")
                client_socket.close()
                break

            print(f"Server says: \n{message}")

            # Get the client's response to the message
            if(message[:1] == "R"):
                response = input("Enter your response: ")
                if response.lower() == "exit":
                    client_socket.send("exit".encode())
                    print("Closing connection")
                    client_socket.close()
                    break

                client_socket.send(response.encode())
        except (ConnectionResetError, BrokenPipeError):
            print("Server disconnected")
            break

if __name__ == "__main__":
    start_client()
