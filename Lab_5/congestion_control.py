import matplotlib.pyplot as plt
import random
from typing import List, Tuple

class TCPCongestionControl:
    def __init__(self, initial_ssthresh: int = 16, loss_probability: float = 0.05, max_rounds: int = 100):
        self.cwnd = 1
        self.ssthresh = initial_ssthresh
        self.loss_probability = loss_probability
        self.max_rounds = max_rounds
        self.cwnd_history = []
        self.round_history = []
        self.events = []

    def is_slow_start(self) -> bool:
        return self.cwnd < self.ssthresh

    def simulate_packet_loss(self) -> bool:
        return random.random() < self.loss_probability

    def handle_successful_ack(self):
        if self.is_slow_start():
            self.cwnd *= 2
            phase = "Slow Start"
        else:
            self.cwnd += 1
            phase = "Congestion Avoidance"
        
        return phase

    def handle_packet_loss(self, round_num: int):
        print(f"Round {round_num}: Packet loss detected! cwnd={self.cwnd}")
        self.ssthresh = max(self.cwnd // 2, 2)
        self.cwnd = 1
        self.events.append((round_num, "Packet Loss"))
        print(f"Round {round_num}: ssthresh set to {self.ssthresh}, cwnd reset to 1")

    def run_simulation(self):
        print("Starting TCP Congestion Control Simulation")
        print(f"Initial ssthresh: {self.ssthresh}")
        print(f"Loss probability: {self.loss_probability * 100:.1f}%")
        print(f"Maximum rounds: {self.max_rounds}")
        print("=" * 60)

        for round_num in range(1, self.max_rounds + 1):
            self.round_history.append(round_num)
            self.cwnd_history.append(self.cwnd)

            if self.simulate_packet_loss():
                self.handle_packet_loss(round_num)
            else:
                phase = self.handle_successful_ack()
                print(f"Round {round_num}: {phase} - cwnd={self.cwnd}, ssthresh={self.ssthresh}")

            if self.cwnd > 1000:
                self.cwnd = 1000

        print("\nSimulation completed!")
        return self.round_history, self.cwnd_history, self.events

    def plot_results(self, filename: str = "cwnd_plot.png"):
        plt.figure(figsize=(12, 8))
        plt.plot(self.round_history, self.cwnd_history, 'b-', linewidth=2, label='Congestion Window Size')
        
        for round_num, event in self.events:
            if event == "Packet Loss":
                plt.axvline(x=round_num, color='red', linestyle='--', alpha=0.7, label='Packet Loss' if round_num == self.events[0][0] else "")
                plt.annotate(f'Loss\nRound {round_num}', 
                           xy=(round_num, self.cwnd_history[round_num-1]), 
                           xytext=(round_num+5, self.cwnd_history[round_num-1]+10),
                           arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
                           fontsize=8, color='red')

        plt.xlabel('Transmission Rounds', fontsize=12)
        plt.ylabel('Congestion Window Size (cwnd)', fontsize=12)
        plt.title('TCP Congestion Control: cwnd Evolution Over Time', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as {filename}")
        plt.show()

    def print_statistics(self):
        max_cwnd = max(self.cwnd_history)
        avg_cwnd = sum(self.cwnd_history) / len(self.cwnd_history)
        loss_count = len([event for _, event in self.events if event == "Packet Loss"])
        
        print("\nSimulation Statistics:")
        print(f"Maximum cwnd reached: {max_cwnd}")
        print(f"Average cwnd: {avg_cwnd:.2f}")
        print(f"Total packet loss events: {loss_count}")
        print(f"Loss rate: {(loss_count / self.max_rounds) * 100:.2f}%")


def main():
    print("TCP Congestion Control Simulator")
    print("=" * 60)
    
    try:
        initial_ssthresh = int(input("Enter initial slow start threshold (default: 16): ") or "16")
        loss_prob = float(input("Enter packet loss probability 0.0-1.0 (default: 0.05): ") or "0.05")
        max_rounds = int(input("Enter maximum transmission rounds (default: 100): ") or "100")
        
        if initial_ssthresh <= 0:
            print("Initial ssthresh must be positive. Using default value of 16.")
            initial_ssthresh = 16
        
        if not 0.0 <= loss_prob <= 1.0:
            print("Loss probability must be between 0.0 and 1.0. Using default value of 0.05.")
            loss_prob = 0.05
        
        if max_rounds <= 0:
            print("Maximum rounds must be positive. Using default value of 100.")
            max_rounds = 100
            
    except ValueError:
        print("Invalid input. Using default values.")
        initial_ssthresh = 16
        loss_prob = 0.05
        max_rounds = 100
    
    simulator = TCPCongestionControl(initial_ssthresh, loss_prob, max_rounds)
    
    rounds, cwnd_values, events = simulator.run_simulation()
    
    simulator.print_statistics()
    
    simulator.plot_results("cwnd_plot.png")


if __name__ == "__main__":
    main()