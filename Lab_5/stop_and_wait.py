import random
import time
import threading
from typing import Optional

class StopAndWaitARQ:
    def __init__(self, total_frames: int, loss_probability: float = 0.3, timeout_duration: float = 2.0):
        self.total_frames = total_frames
        self.loss_probability = loss_probability
        self.timeout_duration = timeout_duration
        self.current_frame = 0
        self.ack_received = False
        self.transmission_complete = False
        
    def simulate_frame_transmission(self, frame_number: int) -> bool:
        time.sleep(0.5)
        
        if random.random() < self.loss_probability:
            print(f"Frame {frame_number} lost during transmission")
            return False
        else:
            print(f"Frame {frame_number} successfully transmitted")
            return True
    
    def simulate_ack_transmission(self, frame_number: int) -> bool:
        time.sleep(0.3)
        
        if random.random() < self.loss_probability * 0.5:
            print(f"ACK {frame_number} lost during transmission")
            return False
        else:
            print(f"ACK {frame_number} received")
            return True
    
    def sender_timeout_handler(self, frame_number: int):
        time.sleep(self.timeout_duration)
        if not self.ack_received and not self.transmission_complete:
            print(f"Timeout for Frame {frame_number}! Retransmitting...")
    
    def send_frame(self, frame_number: int) -> bool:
        print(f"\nSending Frame {frame_number}")
        
        self.ack_received = False
        
        timeout_thread = threading.Thread(
            target=self.sender_timeout_handler, 
            args=(frame_number,)
        )
        timeout_thread.daemon = True
        timeout_thread.start()
        
        frame_transmitted = self.simulate_frame_transmission(frame_number)
        
        if frame_transmitted:
            ack_received = self.simulate_ack_transmission(frame_number)
            
            if ack_received:
                self.ack_received = True
                print(f"ACK {frame_number} received - Frame {frame_number} confirmed")
                return True
            else:
                print(f"ACK {frame_number} lost - will timeout and retransmit")
                return False
        else:
            print(f"Frame {frame_number} lost - will timeout and retransmit")
            return False
    
    def run_simulation(self):
        print("Starting Stop-and-Wait ARQ Protocol Simulation")
        print(f"Configuration:")
        print(f"   Total frames to send: {self.total_frames}")
        print(f"   Loss probability: {self.loss_probability * 100:.1f}%")
        print(f"   Timeout duration: {self.timeout_duration} seconds")
        print("=" * 60)
        
        frame_number = 0
        total_transmissions = 0
        retransmissions = 0
        
        while frame_number < self.total_frames:
            total_transmissions += 1
            
            success = self.send_frame(frame_number)
            
            if success:
                frame_number += 1
                print(f"Frame {frame_number - 1} successfully delivered!")
            else:
                retransmissions += 1
                print(f"Frame {frame_number} lost, retransmitting...")
                time.sleep(self.timeout_duration)
        
        self.transmission_complete = True
        
        print("\n" + "=" * 60)
        print("Simulation Complete!")
        print(f"All {self.total_frames} frames successfully transmitted")
        print(f"Statistics:")
        print(f"   Total transmissions: {total_transmissions}")
        print(f"   Retransmissions: {retransmissions}")
        print(f"   Efficiency: {(self.total_frames / total_transmissions) * 100:.1f}%")


def main():
    print("Stop-and-Wait ARQ Protocol Simulator")
    print("=" * 60)
    
    try:
        total_frames = int(input("Enter the number of frames to transmit (default: 5): ") or "5")
        loss_prob = float(input("Enter frame loss probability 0.0-1.0 (default: 0.3): ") or "0.3")
        timeout = float(input("Enter timeout duration in seconds (default: 2.0): ") or "2.0")
        
        if total_frames <= 0:
            print("Number of frames must be positive. Using default value of 5.")
            total_frames = 5
        
        if not 0.0 <= loss_prob <= 1.0:
            print("Loss probability must be between 0.0 and 1.0. Using default value of 0.3.")
            loss_prob = 0.3
        
        if timeout <= 0:
            print("Timeout must be positive. Using default value of 2.0 seconds.")
            timeout = 2.0
            
    except ValueError:
        print("Invalid input. Using default values.")
        total_frames = 5
        loss_prob = 0.3
        timeout = 2.0
    
    simulator = StopAndWaitARQ(total_frames, loss_prob, timeout)
    simulator.run_simulation()


if __name__ == "__main__":
    main()