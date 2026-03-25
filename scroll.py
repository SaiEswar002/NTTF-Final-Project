import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize hand tracking
hands = mp_hands.Hands(min_detection_confidence=0.5)

# Initialize the mouse controller
mouse = Controller()

# Main loop
cap = cv2.VideoCapture(1)
click_threshold = 50  # Adjust this value for sensitivity
scroll_speed = 1.5    # Adjust this value for scroll speed
scroll_delay = 0.5    # Adjust this value for scroll delay

while cap.isOpened():
    # Read frames from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe hands
    results = hands.process(rgb_frame)

    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the position of thumb tip
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert the normalized coordinates to pixel coordinates
            thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])

            # Check if the thumb is extended
            thumb_extended = thumb_tip.y < 0.8  # Adjust this threshold based on your hand's behavior

            # Move the mouse cursor to the thumb tip position
            mouse.position = (thumb_x, thumb_y)

            # Check for a click gesture (thumb extended)
            if thumb_extended:
                # Perform a click action
                mouse.click(Button.left)

            # Draw a circle at the thumb tip
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)

    # Display the frame
    cv2.imshow('Virtual Mouse', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
