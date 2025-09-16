import socket
import threading
import time
import random
import string

class CookieServer:
    def __init__(self, host='localhost', port=8081):
        self.host = host
        self.port = port
        self.users = {}
        
    def generate_user_id(self):
        return 'User' + ''.join(random.choices(string.digits, k=3))
    
    def parse_request(self, request):
        lines = request.split('\r\n')
        if not lines:
            return None, None, None
        
        request_line = lines[0]
        method, path, version = request_line.split()
        
        headers = {}
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        return method, path, headers
    
    def extract_cookie(self, headers):
        cookie_header = headers.get('cookie', '')
        if 'session_id=' in cookie_header:
            parts = cookie_header.split('session_id=')
            if len(parts) > 1:
                return parts[1].split(';')[0]
        return None
    
    def create_response(self, status, headers, body):
        response = f"HTTP/1.1 {status}\r\n"
        for key, value in headers.items():
            response += f"{key}: {value}\r\n"
        response += "\r\n"
        response += body
        return response.encode('utf-8')
    
    def handle_client(self, client_socket, address):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            
            method, path, headers = self.parse_request(request)
            
            if method != 'GET':
                response = self.create_response("405 Method Not Allowed", 
                                              {"Content-Type": "text/html"}, 
                                              "<h1>Method Not Allowed</h1>")
                client_socket.send(response)
                return
            
            session_id = self.extract_cookie(headers)
            
            if session_id and session_id in self.users:
                user_info = self.users[session_id]
                visit_count = user_info['visits'] + 1
                self.users[session_id]['visits'] = visit_count
                self.users[session_id]['last_visit'] = time.time()
                
                body = f"""
                <html>
                <head><title>Welcome Back</title></head>
                <body>
                    <h1>Welcome Back, {session_id}!</h1>
                    <p>This is visit number {visit_count}</p>
                    <p>Your session ID: {session_id}</p>
                    <p>First visit: {time.ctime(user_info['first_visit'])}</p>
                    <p>Current time: {time.ctime()}</p>
                    <button onclick="location.reload()">Refresh</button>
                </body>
                </html>
                """
                
                response_headers = {
                    "Content-Type": "text/html",
                    "Content-Length": str(len(body.encode('utf-8')))
                }
            else:
                new_session_id = self.generate_user_id()
                current_time = time.time()
                
                self.users[new_session_id] = {
                    'visits': 1,
                    'first_visit': current_time,
                    'last_visit': current_time
                }
                
                body = f"""
                <html>
                <head><title>Welcome New User</title></head>
                <body>
                    <h1>Welcome New Visitor!</h1>
                    <p>Your session ID: {new_session_id}</p>
                    <p>Current time: {time.ctime()}</p>
                    <p>Refresh to see the welcome back message</p>
                    <button onclick="location.reload()">Refresh</button>
                </body>
                </html>
                """
                
                response_headers = {
                    "Content-Type": "text/html",
                    "Content-Length": str(len(body.encode('utf-8'))),
                    "Set-Cookie": f"session_id={new_session_id}; Path=/; HttpOnly"
                }
            
            response = self.create_response("200 OK", response_headers, body)
            client_socket.send(response)
            
        except Exception:
            error_body = "<h1>500 Internal Server Error</h1>"
            response = self.create_response("500 Internal Server Error", 
                                          {"Content-Type": "text/html"}, 
                                          error_body)
            client_socket.send(response)
        finally:
            client_socket.close()
    
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, 
                                                args=(client_socket, address))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            pass
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = CookieServer()
    server.start_server()