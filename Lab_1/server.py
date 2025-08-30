#!/usr/bin/env python3

import socket
import sys
import random

# Check if port number is provided as command line argument
if len(sys.argv) < 2:
    print("Usage: python3 server.py <port>")
    sys.exit(1)

# Server configuration
PORT = int(sys.argv[1])
SERVER_NAME = "Server of Aditya"

# Create and setup the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(5)

print(f"Server listening on port {PORT}...")

try:
    should_terminate = False
    while not should_terminate:
        # Accept incoming connection
        client_connection, client_address = server_socket.accept()
        print(f"\nConnection from {client_address[0]}:{client_address[1]}")
        
        with client_connection:
            # Create a file-like interface for easier reading
            connection_file = client_connection.makefile('rwb')
            
            # Get client's name
            client_name_raw = connection_file.readline()
            if not client_name_raw:
                print("No data received. Closing connection.")
                continue
            client_name = client_name_raw.decode('utf-8', errors='replace').rstrip('\r\n')

            # Get client's number
            client_number_raw = connection_file.readline()
            if not client_number_raw:
                print("Client closed before sending integer.")
                continue
                
            client_number_str = client_number_raw.decode('utf-8', errors='replace').strip()
            try:
                client_number = int(client_number_str)
            except ValueError:
                client_number = None

            # Display connection information
            print(f"  Client's name : {client_name}")
            print(f"  Server's name : {SERVER_NAME}")

            # Validate client's number
            if client_number is None or not (1 <= client_number <= 100):
                print(f"  Client's integer: {client_number_str} (invalid or out of range)")
                print("Received number outside 1..100 (or invalid). Server will terminate and close sockets.")
                should_terminate = True
                break

            # Generate server's random number and calculate total
            server_number = random.randint(1, 100)
            sum_of_numbers = client_number + server_number

            # Display the numbers
            print(f"  Client's integer: {client_number}")
            print(f"  Server's integer: {server_number}")
            print(f"  Sum: {sum_of_numbers}")

            # Send response to client
            response = f"{SERVER_NAME}\n{server_number}\n".encode('utf-8')
            try:
                client_connection.sendall(response)
            except BrokenPipeError:
                print("Failed to send reply (client disconnected).")

        print("Connection closed. Waiting for next client...")

finally:
    server_socket.close()
    print("Server socket closed. Exiting.")
