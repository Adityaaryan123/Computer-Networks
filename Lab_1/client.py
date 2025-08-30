#!/usr/bin/env python3

import socket
import sys

# Check if required command line arguments are provided
if len(sys.argv) < 3:
    print("Usage: python3 client.py <server_ip> <port>")
    sys.exit(1)

# Client configuration
SERVER_IP = sys.argv[1]
PORT = int(sys.argv[2])
CLIENT_NAME = "Client of Aryan"

# Get user input and validate it
try:
    user_number = int(input("Enter an integer between 1 and 100: ").strip())
except ValueError:
    print("Invalid integer. Exiting.")
    sys.exit(1)

# Ensure number is within valid range
if not (1 <= user_number <= 100):
    print("Number must be between 1 and 100. Exiting.")
    sys.exit(1)

# Establish connection and communicate with server
with socket.create_connection((SERVER_IP, PORT)) as client_socket:
    # Send client name and number to server
    message = f"{CLIENT_NAME}\n{user_number}\n".encode('utf-8')
    client_socket.sendall(message)

    # Create file-like interface for reading server response
    socket_file = client_socket.makefile('rb')
    server_name_raw = socket_file.readline()
    if not server_name_raw:
        print("No reply from server.")
        sys.exit(1)
    server_name = server_name_raw.decode('utf-8', errors='replace').strip()

    # Get server's number
    server_number_raw = socket_file.readline()
    if not server_number_raw:
        print("Server did not send a number.")
        sys.exit(1)
    
    # Parse server's number
    try:
        server_number = int(server_number_raw.decode('utf-8', errors='replace').strip())
    except ValueError:
        server_number = None

    # Display results
    print("\n--- Received Reply ---")
    print(f"Client's name: {CLIENT_NAME}")
    print(f"Server's name: {server_name}")
    print(f"Client's integer: {user_number}")
    print(f"Server's integer: {server_number}")
    
    # Show sum if server sent a valid number
    if server_number is not None:
        print(f"Sum: {user_number + server_number}")
    else:
        print("Server sent invalid number.")
