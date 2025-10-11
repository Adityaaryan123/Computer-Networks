import random
import time
from typing import List, Optional

class GoBackNARQ:
    def __init__(self, total_frames: int, window_size: int, loss_probability: float = 0.3, timeout_duration: float = 2.0):
        self.total_frames = total_frames
        self.window_size = window_size
        self.loss_probability = loss_probability
        self.timeout_duration = timeout_duration
        
        self.window_start = 0
        self.next_frame_to_send = 0
        self.ack_received = [False] * total_frames
        self.last_ack_received = -1
        self.transmission_complete = False
        self.total_transmissions = 0
        self.retransmissions = 0

    def get_window_end(self) -> int:
        return min(self.window_start + self.window_size - 1, self.total_frames - 1)

    def simulate_frame_transmission(self, frame_number: int) -> bool:
        time.sleep(0.1)
        self.total_transmissions += 1
        
        if random.random() < self.loss_probability:
            print(f"Frame {frame_number} lost during transmission")
            return False
        else:
            print(f"Frame {frame_number} transmitted successfully")
            return True

    def simulate_ack_transmission(self, frame_number: int) -> bool:
        time.sleep(0.05)
        
        if random.random() < self.loss_probability * 0.3:
            print(f"ACK {frame_number} lost during transmission")
            return False
        else:
            print(f"ACK {frame_number} received")
            return True

    def send_frames_in_window(self) -> List[int]:
        sent_frames = []
        window_end = self.get_window_end()
        
        if self.next_frame_to_send <= window_end:
            frames_to_send = list(range(self.next_frame_to_send, window_end + 1))
            print(f"Sending frames {frames_to_send[0]} to {frames_to_send[-1]}")
            
            for frame_num in frames_to_send:
                if self.simulate_frame_transmission(frame_num):
                    sent_frames.append(frame_num)
                else:
                    break
            
            self.next_frame_to_send = window_end + 1
        
        return sent_frames

    def process_acknowledgments(self, sent_frames: List[int]) -> bool:
        if not sent_frames:
            return False
        
        for frame_num in sent_frames:
            if self.simulate_ack_transmission(frame_num):
                self.last_ack_received = frame_num
                for i in range(frame_num + 1):
                    self.ack_received[i] = True
                return True
        
        return False

    def handle_timeout_and_retransmit(self):
        lost_frame = self.window_start
        while lost_frame < len(self.ack_received) and self.ack_received[lost_frame]:
            lost_frame += 1
        
        if lost_frame < self.total_frames:
            window_end = self.get_window_end()
            print(f"Timeout! Frame {lost_frame} lost, retransmitting frames {lost_frame} to {window_end}")
            
            self.next_frame_to_send = lost_frame
            self.retransmissions += 1
            
            for frame_num in range(lost_frame, window_end + 1):
                self.simulate_frame_transmission(frame_num)
                self.total_transmissions += 1

    def slide_window(self):
        old_start = self.window_start
        
        while (self.window_start < self.total_frames and 
               self.window_start < len(self.ack_received) and 
               self.ack_received[self.window_start]):
            self.window_start += 1
        
        if self.window_start > old_start:
            window_end = self.get_window_end()
            if self.window_start < self.total_frames:
                print(f"Window slides to {self.window_start} to {window_end}")

    def run_simulation(self):
        print("Starting Go-Back-N ARQ Protocol Simulation")
        print(f"Configuration:")
        print(f"   Total frames: {self.total_frames}")
        print(f"   Window size: {self.window_size}")
        print(f"   Loss probability: {self.loss_probability * 100:.1f}%")
        print(f"   Timeout duration: {self.timeout_duration} seconds")
        print("=" * 60)
        
        while self.window_start < self.total_frames:
            print(f"\nCurrent window: {self.window_start} to {self.get_window_end()}")
            
            sent_frames = self.send_frames_in_window()
            
            if sent_frames:
                ack_received = self.process_acknowledgments(sent_frames)
                
                if ack_received:
                    print(f"Cumulative ACK received up to frame {self.last_ack_received}")
                    self.slide_window()
                else:
                    print(f"No ACK received, waiting for timeout...")
                    time.sleep(self.timeout_duration)
                    self.handle_timeout_and_retransmit()
            else:
                print(f"All frames in current window lost, waiting for timeout...")
                time.sleep(self.timeout_duration)
                self.handle_timeout_and_retransmit()
        
        self.transmission_complete = True
        
        print("\n" + "=" * 60)
        print("Simulation Complete!")
        print(f"All {self.total_frames} frames successfully transmitted")
        print(f"Statistics:")
        print(f"   Total transmissions: {self.total_transmissions}")
        print(f"   Retransmissions: {self.retransmissions}")
        print(f"   Efficiency: {(self.total_frames / self.total_transmissions) * 100:.1f}%")


def main():
    print("Go-Back-N ARQ Protocol Simulator")
    print("=" * 60)
    
    try:
        total_frames = int(input("Enter total number of frames to send (default: 10): ") or "10")
        window_size = int(input("Enter window size N (default: 4): ") or "4")
        loss_prob = float(input("Enter frame loss probability 0.0-1.0 (default: 0.3): ") or "0.3")
        timeout = float(input("Enter timeout duration in seconds (default: 2.0): ") or "2.0")
        
        if total_frames <= 0:
            print("Total frames must be positive. Using default value of 10.")
            total_frames = 10
        
        if window_size <= 0 or window_size > total_frames:
            print(f"Window size must be between 1 and {total_frames}. Using default value of 4.")
            window_size = min(4, total_frames)
        
        if not 0.0 <= loss_prob <= 1.0:
            print("Loss probability must be between 0.0 and 1.0. Using default value of 0.3.")
            loss_prob = 0.3
        
        if timeout <= 0:
            print("Timeout must be positive. Using default value of 2.0 seconds.")
            timeout = 2.0
            
    except ValueError:
        print("Invalid input. Using default values.")
        total_frames = 10
        window_size = 4
        loss_prob = 0.3
        timeout = 2.0
    
    simulator = GoBackNARQ(total_frames, window_size, loss_prob, timeout)
    simulator.run_simulation()


if __name__ == "__main__":
    main()