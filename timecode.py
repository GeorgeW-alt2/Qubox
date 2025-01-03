import numpy as np
import time
import random
import signal
import sys
import serial  # Import the serial library for communication with the serial device
import matplotlib.pyplot as plt  # Import matplotlib for plotting
lambda_time = 0.1001 #time sleep changing from 0.1 to 0.001, has interesting results
class TemporalSpringSystem:
    def __init__(self, oscillation_frequency, max_buffer_depth, photon_threshold, serial_port='COM3'):
        self.oscillation_frequency = oscillation_frequency  # Frequency of oscillation
        self.max_buffer_depth = max_buffer_depth  # Maximum depth of latent temporal buffer
        self.photon_threshold = photon_threshold  # Threshold for photon detection (0 to 1)
        self.temporal_buffer = []  # History of previous system states
        self.time_offset = 0  # A time offset to simulate the passage of time
        
        # Initialize serial connection to read photon probability
        self.serial_port = serial_port
        self.serial_connection = serial.Serial(self.serial_port, 9600, timeout=1)  # Open serial port at 9600 baud rate
        
        # Register signal handler for keyboard interrupt (Ctrl + C)
        signal.signal(signal.SIGINT, self.handle_interrupt)
        
        # Store the states for plotting
        self.states = []

    def oscillation(self):
        """Generate an oscillating number based on a sine wave."""
        t = time.time() + self.time_offset  # Use the system time as the base for oscillation
        return np.sin(2 * np.pi * self.oscillation_frequency * t)
    
    def time_based_random(self):
        """Generate a time-based random number influenced by the current time."""
        current_time = time.time()  # Get the current time in seconds
        random.seed(current_time)  # Use current time as the seed for randomness
        return random.random()  # Return a time based random number

    def read_photon_probability(self):
        """Read photon probability from the serial input (range 0 to 1)."""
        if self.serial_connection.in_waiting > 0:  # Check if there's data available
            try:
                data = self.serial_connection.readline().decode('utf-8').strip()  # Read data from serial
                photon_probability = float(data)  # Convert to float (make sure the data is a valid float)
                return photon_probability
            except ValueError:
                return random.random()  # If data is invalid, fall back to a random number
        else:
            return random.random()  # If no data is available, fall back to a random number
    
    def update_temporal_buffer(self, state):
        """Update the latent temporal buffer with the new state."""
        self.temporal_buffer.append(state)
        if len(self.temporal_buffer) > self.max_buffer_depth:
            self.temporal_buffer.pop(0)  # Keep the buffer within the max depth
    
    def cost_function(self):
        """Calculate the cost based on the depth of the latent temporal buffer."""
        return len(self.temporal_buffer)  # Simple cost function: deeper buffers increase cost
    
    def photon_measurement(self):
        """Simulate a photon measurement event based on the threshold read from serial input."""
        photon_probability = self.read_photon_probability()  # Get photon probability from serial
        if photon_probability < self.photon_threshold:
            return True  # Photon detected
        else:
            return False  # No photon detected
    
    def get_current_state(self):
        """Calculate the current system state (for simplicity, we'll use the random number)."""
        time_rand = self.time_based_random()
        state = time_rand + self.oscillation()  # Combine randomness and oscillation for state
        return state
    
    def handle_interrupt(self, signum, frame):
        """Handle Ctrl + C (SIGINT) interruption."""
        print("\nCtrl + C detected! Checking sentinel condition...")
        
        # Check if the sentinel condition is met
        print(f"Sentinel triggered. Updating temporal buffer...")
        state = 1  # Generate a state to update the buffer
        for i in range(self.max_buffer_depth):
            self.update_temporal_buffer(state)
        print(f"Temporal buffer updated with state: {state:.4f} * {self.max_buffer_depth} ")
        
        # Exit the program after handling the interrupt
        sys.exit(0)

    def run_step(self):
        """Perform one update step of the system."""
        state = self.get_current_state()
        
        # Store the state for plotting
        self.states.append(state)
        
        # Check for photon measurement at this step
        photon_detected = self.photon_measurement()
        
        cost = self.cost_function()
        
        # Print the state, cost, and photon detection info
        print(f"State: {state:.4f}, Photon Detected: {photon_detected}")
        
        # Simulate the "chronological forcing" by updating time offset
    
    def run(self, steps):
        """Run the system for a certain number of steps."""
        for _ in range(steps):
            self.run_step()
            time.sleep(lambda_time)  # Sleep to simulate time progression

        # Plot the states after the simulation
        self.plot_state_over_time()

    def plot_state_over_time(self):
        """Plot the states over time."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.states, label='System State')
        plt.title('System State Over Time')
        plt.xlabel('Time Steps')
        plt.ylabel('State Value')
        plt.legend()
        plt.grid(True)
        plt.show()


# Initialize the TemporalSpringSystem with photon measurement from serial input
temporal_system = TemporalSpringSystem(oscillation_frequency=0.1, max_buffer_depth=100, photon_threshold=0.75)

# Run the system for a number of steps to simulate time-based, oscillatory behavior, and photon detection
temporal_system.run(steps=150)  
