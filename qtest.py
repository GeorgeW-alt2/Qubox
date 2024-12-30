import cv2
import numpy as np
import random
import time

# Parameters
sensitivity = 80
min_period = 15
x, y = 0.2, 0.3
longcyc = 2
longcyc2 = 3

# State variables
Do = 0
Do2 = 0
it = 0
ack = 0
nul = 0
and_count = 0
or_count = 0
cyc = 0
swi = 0
swi2 = 0
qu = 0
swif = ""
numa = ""
buffer = []

# Generate random binary sequences
swif = ",".join(str(random.randint(0, 1)) for _ in range(500))
numa = ",".join(str(random.randint(0, 1)) for _ in range(100))

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(640 * x))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(480 * y))

# Helper functions
def process_frame(frame, sensitivity):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    return blurred

def detect_motion(prev_frame, current_frame, sensitivity):
    diff = cv2.absdiff(prev_frame, current_frame)
    _, thresh = cv2.threshold(diff, sensitivity, 255, cv2.THRESH_BINARY)
    return np.sum(thresh > 10)

def handle_logic(b, bb):
    global Do, Do2, it, ack, nul, and_count, or_count, cyc, swi, swi2, qu
    done = False
    if b > 4 and b < 11 or bb > 4 and bb < 11:
        or_count += 1
    if b > 4 and b < 11 and bb > 4 and bb < 11:
        and_count += 1
        if Do == 1:
            if qu == 1 and it == 0:
                qu = 0
                it += 1
            elif qu == 0 and it == 0:
                qu = 1
                it += 1
            it = 0
            done = True
    return done

# Main loop
ret, prev_frame = cap.read()
if ret:
    prev_frame = process_frame(prev_frame, sensitivity)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    current_frame = process_frame(frame, sensitivity)
    b = detect_motion(prev_frame, current_frame, sensitivity)

    # Logic based on motion
    if Do == 1:
        Do2 = 1

    bb = 0  # Placeholder for additional logic

    if handle_logic(b, bb):
        cyc += 1

    # Update display
    cv2.putText(frame, f"ACK: {ack} NULL: {nul}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Motion Detection', frame)

    # Check for exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    prev_frame = current_frame

cap.release()
cv2.destroyAllWindows()
