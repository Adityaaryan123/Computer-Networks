import socket
import time
import cv2
import numpy as np
import sys
import struct

def start_video_server(video_path, host='localhost', port=12345, fps=30, quality=80, chunk_size=4096):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    frame_interval = 1.0 / fps
    frame_count = 0
    
    print(f"Video server started on {host}:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        while True:
            start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                print("End of video file reached. Restarting...")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            frame_count += 1
            
            height, width = frame.shape[:2]
            if width > 640:
                scale = 640 / width
                frame = cv2.resize(frame, (640, int(height * scale)))
                
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
            frame_data = encoded_frame.tobytes()
            
            total_bytes = len(frame_data)
            num_chunks = (total_bytes + chunk_size - 1) // chunk_size
            
            frame_info = struct.pack("!I", frame_count)
            server_socket.sendto(frame_info, server_address)
            
            for i in range(num_chunks):
                start_idx = i * chunk_size
                end_idx = min(start_idx + chunk_size, total_bytes)
                chunk = frame_data[start_idx:end_idx]
                
                marker = 1 if i == num_chunks - 1 else 0
                header = struct.pack("!II?", frame_count, i, marker)
                
                packet = header + chunk
                server_socket.sendto(packet, server_address)
            
            elapsed = time.time() - start_time
            sleep_time = max(0, frame_interval - elapsed)
            time.sleep(sleep_time)
            
            if frame_count % 30 == 0:
                print(f"Streaming... Sent {frame_count} frames")
                
    except KeyboardInterrupt:
        print("\nVideo streaming stopped by user")
    finally:
        cap.release()
        server_socket.close()
        print("Server shutdown complete")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python video_server.py <video_file> [host] [port]")
        sys.exit(1)
        
    video_file = sys.argv[1]
    host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 12345
    
    start_video_server(video_file, host, port)