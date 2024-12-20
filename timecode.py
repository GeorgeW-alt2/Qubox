import numpy as np
import time
import random
import signal
import sys

class TemporalSpringSystem:
    def __init__(self, oscillation_frequency=0.1, max_buffer_depth=10, photon_threshold=0.5):
        self.oscillation_frequency = oscillation_frequency  # Frequency of oscillation
        self.max_buffer_depth = max_buffer_depth  # Maximum depth of latent temporal buffer
        self.photon_threshold = photon_threshold  # Threshold for photon detection (0 to 1)
        self.temporal_buffer = []  # History of previous system states
        self.time_offset = 0  # A time offset to simulate the passage of time
        
        # Register signal handler for keyboard interrupt (Ctrl + C)
        signal.signal(signal.SIGINT, self.handle_interrupt)

    def oscillation(self):
        """Generate an oscillating number based on a sine wave."""
        t = time.time() + self.time_offset  # Use the system time as the base for oscillation
        return np.sin(2 * np.pi * self.oscillation_frequency * t)
    
    def time_based_random(self):
        """Generate a time-based random number influenced by the current time."""
        current_time = time.time()  # Get the current time in seconds
        random.seed(current_time)  # Use current time as the seed for randomness
        return random.random()  # Return a time based random number
        
    def update_temporal_buffer(self, state):
        """Update the latent temporal buffer with the new state."""
        self.temporal_buffer.append(state)
        if len(self.temporal_buffer) > self.max_buffer_depth:
            self.temporal_buffer.pop(0)  # Keep the buffer within the max depth
    
    def cost_function(self):
        """Calculate the cost based on the depth of the latent temporal buffer."""
        return len(self.temporal_buffer)  # Simple cost function: deeper buffers increase cost
    
    def photon_measurement(self):
        """Simulate a photon measurement event based on a threshold."""
        photon_probability = self.time_based_random() # add photon stream
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
        state = self.get_current_state()  # Generate a state to update the buffer
        self.update_temporal_buffer(state)
        print(f"Temporal buffer updated with state: {state:.4f}")
        
        # Exit the program after handling the interrupt
        sys.exit(0)

    def run_step(self):
        """Perform one update step of the system."""
        state = self.get_current_state()
        
        # Check for photon measurement at this step
        photon_detected = self.photon_measurement()
        
        cost = self.cost_function()
        
        # Print the state, cost, and photon detection info
        print(f"State: {state:.4f}, Cost: {cost}, Photon Detected: {photon_detected}")
        
        # Simulate the "chronological forcing" by updating time offset
        self.time_offset += 0.1  # Increment time to simulate time flow
    
    def run(self, steps):
        """Run the system for a certain number of steps."""
        for _ in range(steps):
            self.run_step()
            time.sleep(0.1)  # Sleep to simulate time progression


# Initialize the TemporalSpringSystem with photon measurement
temporal_system = TemporalSpringSystem(oscillation_frequency=0.1, max_buffer_depth=5, photon_threshold=0.4)

# Run the system for a number of steps to simulate time-based, oscillatory behavior, and photon detection
temporal_system.run(steps=50)
