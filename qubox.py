import cv2
import numpy as np
import os
from datetime import datetime
from collections import deque

test_int = 10000000000000 #requires number larger than state space search
        
class QuantumCommunicator:
    def __init__(self, sensitivity=500):
        # Previous initialization code remains the same
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
        self.longcyc = 10
        self.numa = ",".join(str(np.random.randint(0, 2)) for _ in range(100000))
        self.corr = 3
        self.prime = 0
        self.ghostprotocol = 0
        self.ghostprotocollast = 0
        self.GhostIterate = 0
        self.testchecknum = 5
        self.ack = 0
        self.nul = 0
        
        # Status tracking variables
        self.motion_frame_count = 0
        self.active_quadrants = set()
        self.last_status_update = datetime.now()
        self.status_update_interval = 0.5
        self.total_frames = 0
        
        # Ghost protocol variables
        self.ghost_messages = deque(maxlen=10)  # Increased to show more messages
        self.range = 10000000000000000
        self.last_ghost_check = 0
        self.prime = 0
        self.prime_threshold = 10  # Add a maximum threshold
    
    
    def clear_console(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')                
    

    def display_status(self):
        """Display current status information"""
        current_time = datetime.now()
        if (current_time - self.last_status_update).total_seconds() < self.status_update_interval:
            return
            
        self.clear_console()
        print("=" * 50)
        print("QUANTUM COMMUNICATOR STATUS")
        print("=" * 50)
        print(f"Time: {current_time.strftime('%H:%M:%S')}")
        
        print(f"\nQUANTUM STATES:")
        print(f"Current Quantum State (qu): {self.qu}")
        print(f"Cycle Position (cyc): {self.cyc}/{len(self.numa.split(','))}")
        print(f"Switch Counter (swi): {self.swi}/{self.longcyc}")
        
        print(f"\nDETECTION COUNTERS:")
        print(f"AND Gate Detections: {self.and_count}/{self.corr}")
        print(f"OR Gate Detections: {self.or_count}/{self.corr}")
        motion_percentage = (self.motion_frame_count / max(1, self.total_frames)) * 100
        print(f"Motion Detected: {self.motion_frame_count} frames ({motion_percentage:.1f}%)")
        
        print(f"\nPROTOCOL STATUS:")
        print(f"Ghost Protocol Value: {self.ghostprotocol * self.range}")
        print(f"Target Value: {test_int}")
        print(f"Ghost Protocol State: {self.ghostprotocol}")
        print(f"Prime State: {self.prime}")
        print(f"Acknowledgments (ACK): {self.ack}")
        print(f"Nullifications (NUL): {self.nul}")
        
        print(f"\nGHOST PROTOCOL OUTPUT:")
        if self.ghost_messages:
            for msg in self.ghost_messages:
                print(msg)
        else:
            print("No ghost protocol messages yet")
        
        print(f"\nACTIVE QUADRANTS: {len(self.active_quadrants)}")
        if self.active_quadrants:
            quadrants_str = ", ".join([f"({x},{y})" for x, y in self.active_quadrants])
            print(f"Locations: {quadrants_str}")
        
        print("\nPress 'Q' to exit")
        print("=" * 50)
        
        self.last_status_update = current_time
        self.active_quadrants.clear()

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
        
        # Check if there's any significant motion in the frame
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
            
        # Process quantum states
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
        """Check and process quantum states with proper prime handling"""
        check = self.numa.split(",")
        
        if self.and_count > self.corr and self.cyc < len(check):
            if check[self.cyc] == str(self.qu):
                if self.swi == self.longcyc:
                    self.qu = np.random.randint(0, 2)
                    self.swi = 0
                    self.prime = 0  # Prime gets reset to 0 here
                self.swi += 1
                self.Do = 1
                self.ack += 1
                self.and_count = 0
                self.cyc += 1
                # Only reset prime if it exceeds threshold
                if self.prime >= self.prime_threshold:
                    self.prime = 0
                else:
                    self.prime += 1  # Increment prime with proper bounds
                
        if self.or_count > self.corr and self.cyc < len(check):
            if check[self.cyc] != str(self.qu):
                if self.swi == self.longcyc:
                    self.qu = np.random.randint(0, 2)
                    self.swi = 0
                self.swi += 1
                self.Do = 1
                self.nul += 1
                self.or_count = 0
                self.and_count = 0
                self.cyc += 1
                self.prime = min(self.prime + 1, self.prime_threshold)  # Increment with ceiling
                self.process_ghost_protocol()
                
    def process_ghost_protocol(self):
        """Process ghost protocol states"""
        self.ghostprotocol += 1
        current_value = self.ghostprotocol * self.range
        
        if self.prime > 1 and self.ghostprotocol > 3:
            # Initial protocol start
            if self.GhostIterate == 0:
                self.ghostprotocollast = current_value
                self.GhostIterate += 1
                current_time = datetime.now()
                self.ghost_messages.append(f"Ghost Protocol Initiated: {self.ghostprotocol} (Value: {current_value}), Time: {current_time.strftime('%H:%M:%S')}")
                message = f"Ghost Protocol Initiated: {self.ghostprotocol} (Value: {current_value}), Time: {current_time.strftime('%H:%M:%S')}"
                self.last_ghost_check = current_value
                with open("log.txt", "a") as file:
                    file.write(f"{message}\n")
            
            f"Ghost Protocol Initiated: {self.ghostprotocol} (Value: {current_value})"
            # Check for test_int requirement
            if current_value >= test_int and self.last_ghost_check != current_value:
                self.ghost_messages.append(f"Range requirement met: {current_value} >= {test_int}")
                self.last_ghost_check = current_value
                
            
            # Regular protocol updates
            if current_value != self.ghostprotocollast:
                msg = f"Protocol state: {current_value} (End state: {test_int})"
                self.ghost_messages.append(msg)
                self.ghostprotocollast = current_value
                
                # Check if we've reached a milestone
                if (current_value * self.range) == (self.ghostprotocollast + self.range):

                    self.ghost_messages.append("****** Milestone reached ******")
    
    def update_output(self, message):
        """Update output display"""
        self.ghost_messages.append(message.strip())
import hashlib
def send_message(self):
        """Send a quantum message when conditions are met, could be a message or math."""
        input_text = "test"

        test_sha256 ="9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
        test_hex = "9f86d081884c7d65"
        test_decimal = 11495104353665842533
        # Generate SHA-256 hash of the input text
        sha256_hash = hashlib.sha256(input_text.encode()).hexdigest()
        binary_val = ''.join(format(ord(c), '08b') for c in "9f86d081884c7d65")
        decimal_val = int(binary_val, 2)  # Convert binary to decimal, ACKs/NUL ratio slows down to ~5 integers per refresh if number is surpassed
        decimal_val = 5 # ACKs/NUL ratio slows down if number is surpassed
        # Using test_int as our target value
        if decimal_val <= self.ghostprotocol * self.range:
            self.numa += ",".join('9' for _ in range(500))
            self.ghost_messages.append(f">>> End state {decimal_val} reached <<<")
            
if __name__ == "__main__":
    communicator = QuantumCommunicator(sensitivity=500)
    communicator.process_camera()