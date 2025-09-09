import socket
import sys

if len(sys.argv) < 3:
    print("Hey! I need the server IP and port to connect. Please use: python3 client.py <server_ip> <port>")
    sys.exit(1)

SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
CLIENT_NAME = "Client of Aryan"

try:
    user_number = int(input("Please enter a number between 1 and 100: ").strip())
except ValueError:
    print("Oops! That's not a valid number. Let me exit gracefully.")
    sys.exit(1)

if not (1 <= user_number <= 100):
    print("Sorry, the number needs to be between 1 and 100. Closing now.")
    sys.exit(1)

with socket.create_connection((SERVER_IP, PORT)) as client_socket:
    message = f"{CLIENT_NAME}\n{user_number}\n".encode('utf-8')
    client_socket.sendall(message)

    socket_file = client_socket.makefile('rb')
    server_name_raw = socket_file.readline()
    if not server_name_raw:
        print("Hmm, the server didn't respond. Something's not right.")
        sys.exit(1)
    server_name = server_name_raw.decode('utf-8', errors='replace').strip()

    server_number_raw = socket_file.readline()
    if not server_number_raw:
        print("The server forgot to send me a number. That's unusual.")
        sys.exit(1)
    
    try:
        server_number = int(server_number_raw.decode('utf-8', errors='replace').strip())
    except ValueError:
        server_number = None

    print("\nGreat! I got a response from the server:")
    print(f"My name is: {CLIENT_NAME}")
    print(f"Server's name is: {server_name}")
    print(f"I sent the number: {user_number}")
    print(f"Server sent back: {server_number}")
    
    if server_number is not None:
        print(f"Together our numbers add up to: {user_number + server_number}")
    else:
        print("Unfortunately, the server sent me something I couldn't understand.")
