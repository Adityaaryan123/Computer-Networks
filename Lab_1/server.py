import socket
import sys
import random

if len(sys.argv) < 2:
    print("I need a port number to start! Please use: python3 server.py <port>")
    sys.exit(1)

PORT = int(sys.argv[1])
SERVER_NAME = "Server of Aditya"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(5)

print(f"Hello! I'm now listening on port {PORT} and ready to serve clients...")

try:
    should_terminate = False
    while not should_terminate:
        client_connection, client_address = server_socket.accept()
        print(f"\nExcellent! A new client connected from {client_address[0]}:{client_address[1]}")
        
        with client_connection:
            connection_file = client_connection.makefile('rwb')
            
            client_name_raw = connection_file.readline()
            if not client_name_raw:
                print("Strange, the client didn't send any data. Closing this connection.")
                continue
            client_name = client_name_raw.decode('utf-8', errors='replace').rstrip('\r\n')

            client_number_raw = connection_file.readline()
            if not client_number_raw:
                print("The client disconnected before sending their number. Oh well.")
                continue
                
            client_number_str = client_number_raw.decode('utf-8', errors='replace').strip()
            try:
                client_number = int(client_number_str)
            except ValueError:
                client_number = None

            print(f"  Client introduced themselves as: {client_name}")
            print(f"  I am: {SERVER_NAME}")

            if client_number is None or not (1 <= client_number <= 100):
                print(f"  Client sent: {client_number_str} (this is not what I expected!)")
                print("The number is outside the valid range 1-100. I'll have to shut down now.")
                should_terminate = True
                break

            server_number = random.randint(1, 100)
            sum_of_numbers = client_number + server_number

            print(f"  Client's number: {client_number}")
            print(f"  My random number: {server_number}")
            print(f"  Our numbers together make: {sum_of_numbers}")

            response = f"{SERVER_NAME}\n{server_number}\n".encode('utf-8')
            try:
                client_connection.sendall(response)
            except BrokenPipeError:
                print("Couldn't send my response back - the client seems to have left.")

        print("Connection finished. I'm ready for the next client!")

finally:
    server_socket.close()
    print("Server is shutting down. Thanks for using me today!")
