import cv2
import numpy as np
import os
from datetime import datetime
from collections import deque
import random
new_message = "test"
class QuantumCommunicator:
    def __init__(self, sensitivity=500):
        # Camera and processing setup
        self.sensitivity = sensitivity
        self.data2 = None
        self.capture = cv2.VideoCapture(0)
        
        # Initialize quantum state variables
        self.Do = 0
        self.Do2 = 0
        self.qu = 0
        self.it = 0
        self.and_count = 0
        self.or_count = 0
        self.cyc = 0
        self.swi = 0
        self.longcyc = 3
        self.numa = ",".join(str(np.random.randint(0, 2)) for _ in range(100000))
        self.corr = 3
        self.prime = 0
        self.ghostprotocol = 0
        self.ghostprotocollast = 0
        self.GhostIterate = 0
        self.testchecknum = 5
        # ACK and status tracking
        self.ack = 0
        self.nul = 0
        self.last_ack_count = 0
        self.start_time = datetime.now()
        self.ack_history = []
        
        # Status tracking variables
        self.motion_frame_count = 0
        self.active_quadrants = set()
        self.last_status_update = datetime.now()
        self.status_update_interval = 0.5
        self.total_frames = 0
        self.binary = ""
        # Ghost protocol variables
        self.ghost_messages = deque(maxlen=4)
        self.range = 10
        self.last_ghost_check = 0
        self.prime = 0
        self.prime_threshold = 3
        
        # OR state tracking
        self.or_state_duration = 0
        self.or_state_threshold = 3  # Number of consecutive seconds to trigger message
        self.last_or_state_time = None

    def analyze_ack_rate(self):
        """Calculate and return ACK rate statistics"""
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()
        
        # Calculate rates
        ack_delta = self.ack - self.last_ack_count
        refreshes = elapsed_time / self.status_update_interval
        
        stats = {
            'acks_per_refresh': round(ack_delta / refreshes if refreshes > 0 else 0, 2),
            'acks_per_second': round(ack_delta / elapsed_time if elapsed_time > 0 else 0, 2),
            'total_acks': self.ack,
            'ack_delta': ack_delta,
            'elapsed_time': round(elapsed_time, 2)
        }
        
        # Update tracking variables
        self.last_ack_count = self.ack
        self.ack_history.append(stats)
        
        return stats

    def clear_console(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_status(self):
        """Display current status information with ACK rate analysis"""
        current_time = datetime.now()
        if (current_time - self.last_status_update).total_seconds() < self.status_update_interval:
            return
            
        self.clear_console()
        ack_stats = self.analyze_ack_rate()

        
        print(self.binary)
       
        
        
        # Log ACK stats to file
        self.log_ack_stats(ack_stats)
        
        self.last_status_update = current_time
        self.active_quadrants.clear()

    def log_ack_stats(self, stats):
        """Log ACK statistics and ghost protocol messages to a file"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (
self.binary
        )
        
       
        
        log_entry += "\n\n"
        
        with open("ack_stats.log", "a") as f:
            f.write(log_entry)

    def process_camera(self):
        """Process camera feed and detect motion in quadrants"""
        while True:
            ret, frame = self.capture.read()
            if not ret:
                break
            
            self.total_frames += 1
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            if self.data2 is None:
                self.data2 = gray
                continue
            
            self.process_motion(frame, gray)
            self.data2 = gray
            
            # Display status in command line
            self.display_status()
            
            # Display the resulting frame
            cv2.imshow('Motion Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.capture.release()
        cv2.destroyAllWindows()

    def process_motion(self, current_frame, gray_frame):
        """Process motion detection and quantum logic"""
        frame_delta = cv2.absdiff(self.data2, gray_frame)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        motion_detected_in_frame = False
        
        height, width = thresh.shape
        quadrant_width = width // 16
        quadrant_height = height // 8
        
        for row in range(8):
            for col in range(16):
                x1 = col * quadrant_width
                y1 = row * quadrant_height
                x2 = (col + 1) * quadrant_width
                y2 = (row + 1) * quadrant_height
                
                quadrant = thresh[y1:y2, x1:x2]
                motion_detected = np.sum(quadrant > 10) > self.sensitivity
                
                if motion_detected:
                    motion_detected_in_frame = True
                    self.active_quadrants.add((row, col))
                    self.apply_quantum_logic(row, col)
                    self.highlight_quadrant(current_frame, x1, y1, x2, y2)
        
        if motion_detected_in_frame:
            self.motion_frame_count += 1

    def highlight_quadrant(self, frame, x1, y1, x2, y2):
        """Highlight a quadrant with motion"""
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    def apply_quantum_logic(self, b, bb):
        """Apply quantum state logic based on motion detection"""
        if self.Do == 1:
            self.Do2 = 1
            if self.qu == 1 and self.it == 0:
                self.qu = 0
                self.it += 1
            if self.qu == 0 and self.it == 0:
                self.qu = 1
                self.it += 1
            self.it = 0
            
        if 4 < b < 11 or 4 < bb < 11:
            self.or_count += 1
            
        if 4 < b < 11 and 4 < bb < 11:
            self.and_count += 1
            if self.Do == 1:
                self.toggle_quantum_state()
                
        self.check_quantum_states()

    def toggle_quantum_state(self):
        """Toggle quantum state based on current conditions"""
        if self.qu == 1 and self.it == 0:
            self.qu = 0
            self.it += 1
        elif self.qu == 0 and self.it == 0:
            self.qu = 1
            self.it += 1
        self.it = 0

    def check_quantum_states(self):
        """Check and process quantum states"""
        check = self.numa.split(",")
        current_time = datetime.now()
        
        # Process OR states
        if self.or_count > self.corr and self.cyc < len(check):
            if self.last_or_state_time is None:
                self.last_or_state_time = current_time
                self.ghost_messages.append(f"OR state initiated at {current_time.strftime('%H:%M:%S')}")
            
            or_duration = (current_time - self.last_or_state_time).total_seconds()
            
            if check[self.cyc] == str(self.qu):
                if self.swi == self.longcyc:
                    self.qu = np.random.randint(0, 2)
                    self.swi = 0
                self.swi += 1
                self.Do = 1
                self.nul += 1
                self.or_count = 0
                self.and_count = 0
                self.cyc += 1
                self.binary += "1"

                self.prime = min(self.prime + 1, self.prime_threshold)
                
                if or_duration >= self.or_state_threshold:
                    message = f"Prolonged OR state detected: Duration {or_duration:.2f}s, Value: {self.qu}"
                    self.ghost_messages.append(message)
                
                self.process_ghost_protocol()
        else:
            if self.last_or_state_time is not None:
                or_duration = (current_time - self.last_or_state_time).total_seconds()
                if or_duration >= self.or_state_threshold:
                    self.ghost_messages.append(f"OR state ended after {or_duration:.2f}s")
            self.last_or_state_time = None
        
        # Process AND states
        if self.and_count > self.corr and self.cyc < len(check):
            if check[self.cyc] != str(self.qu):
                if self.swi == self.longcyc:
                    self.qu = np.random.randint(0, 2)
                    self.swi = 0
                    self.prime = 0
                self.swi += 1
                self.Do = 1
                self.ack += 1
                self.and_count = 0
                self.cyc += 1
                self.binary += "0"
                if self.prime >= self.prime_threshold:
                    self.prime = 0
                else:
                    self.prime += 1

    def process_ghost_protocol(self):
        """Process ghost protocol states"""
        current_value = self.ghostprotocol * self.range
        
        if self.prime > 1 and self.ghostprotocol > 3:
            if self.GhostIterate == 0:
                self.ghostprotocollast = current_value
                self.GhostIterate += 1
                current_time = datetime.now()
                message = f"Ghost Protocol Initiated: {self.ghostprotocol} (Value: {current_value}), Time: {current_time.strftime('%H:%M:%S')}"
                self.ghost_messages.append(message)
                self.last_ghost_check = current_value
                
                # Log initialization
                with open("ack_stats.log", "a") as f:
                    f.write(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}, GHOST PROTOCOL INITIALIZED, Value: {current_value}\n")
            
            if current_value != self.ghostprotocollast:
                msg = f"Protocol state: {self.binary}"
                self.ghost_messages.append(msg)
                self.ghostprotocollast = current_value
        self.ghostprotocol += 1

        
def send_message(self):
        """Send a quantum message when conditions are met, could be a message or math."""
        new_message = input("Input:")
        if old_message == new_message:
            self.numa += ",".join('9' for _ in range(500)) #Paradox search
            

if __name__ == "__main__":
    try:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Initialize the communicator
        communicator = QuantumCommunicator(sensitivity=500)
        print("Quantum Communicator initialized. Starting camera feed...")
        
        # Start processing
        communicator.process_camera()
        
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up
        if hasattr(communicator, 'capture'):
            communicator.capture.release()
        cv2.destroyAllWindows()
        print("Shutdown complete.")