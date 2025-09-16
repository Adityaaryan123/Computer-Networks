import socket
import cv2
import numpy as np
import sys
import struct
import time
from collections import defaultdict

def start_video_client(host='localhost', port=12345, buffer_size=65536):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
    client_address = (host, port)
    
    client_socket.bind(('', port))
    client_socket.settimeout(10.0)
    
    print(f"Video client started, listening on port {port}")
    print("Press 'q' to quit")
    
    frame_buffer = defaultdict(dict)
    current_frame_id = None
    
    try:
        while True:
            try:
                packet, _ = client_socket.recvfrom(buffer_size)
                
                if len(packet) == struct.calcsize("!I"):
                    frame_id = struct.unpack("!I", packet)[0]
                    current_frame_id = frame_id
                    continue
                    
                header_size = struct.calcsize("!II?")
                header = packet[:header_size]
                frame_id, chunk_id, marker = struct.unpack("!II?", header)
                
                chunk_data = packet[header_size:]
                frame_buffer[frame_id][chunk_id] = chunk_data
                
                if marker:
                    if all(i in frame_buffer[frame_id] for i in range(chunk_id + 1)):
                        frame_data = b''
                        for i in range(chunk_id + 1):
                            frame_data += frame_buffer[frame_id][i]
                            
                        nparr = np.frombuffer(frame_data, np.uint8)
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        
                        if frame is not None:
                            cv2.imshow("Video Stream", frame)
                            key = cv2.waitKey(1) & 0xFF
                            if key == ord('q'):
                                break
                                
                        frame_buffer.pop(frame_id, None)
                        
                        for old_id in list(frame_buffer.keys()):
                            if old_id < frame_id - 5:
                                frame_buffer.pop(old_id, None)
                
            except socket.timeout:
                print("Socket timeout, waiting for data...")
                continue
                
    except KeyboardInterrupt:
        print("\nVideo streaming stopped by user")
    finally:
        client_socket.close()
        cv2.destroyAllWindows()
        print("Client shutdown complete")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    
    start_video_client(host, port)