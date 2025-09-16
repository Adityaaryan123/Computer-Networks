import http.server
import socketserver
import os
import hashlib
import time
from datetime import datetime

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        
        file_path = '.' + self.path
        
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return
        
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            
            file_stats = os.stat(file_path)
            last_modified = datetime.fromtimestamp(file_stats.st_mtime)
            etag = hashlib.md5(content).hexdigest()
            
            client_etag = self.headers.get('If-None-Match')
            client_modified = self.headers.get('If-Modified-Since')
            
            if client_etag and client_etag.strip('"') == etag:
                self.send_response(304)
                self.send_header('ETag', f'"{etag}"')
                self.end_headers()
                return
            
            if client_modified:
                try:
                    client_time = datetime.strptime(client_modified, '%a, %d %b %Y %H:%M:%S GMT')
                    if last_modified <= client_time:
                        self.send_response(304)
                        self.send_header('Last-Modified', last_modified.strftime('%a, %d %b %Y %H:%M:%S GMT'))
                        self.end_headers()
                        return
                except ValueError:
                    pass
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(content)))
            self.send_header('ETag', f'"{etag}"')
            self.send_header('Last-Modified', last_modified.strftime('%a, %d %b %Y %H:%M:%S GMT'))
            self.end_headers()
            self.wfile.write(content)
            
        except Exception as e:
            self.send_error(500, "Internal server error")

if __name__ == "__main__":
    port = 8080
    handler = CachingHandler
    
    with socketserver.TCPServer(("", port), handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass