import cv2
import mediapipe as mp
from pynput.mouse import Controller, Button
import time
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize hand tracking
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Initialize the mouse controller
mouse = Controller()

# Main loop
cap = cv2.VideoCapture(0)  # Fixed: use primary camera index 0
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit(1)

scroll_speed = 3       # Mouse scroll units per gesture trigger
scroll_delay = 0.15   # Seconds between scroll actions
click_cooldown = 0.5  # Seconds between clicks

last_scroll_time = 0
last_click_time = 0

# Get screen dimensions for coordinate mapping
screen_w, screen_h = pyautogui.size()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    status = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Map thumb position to screen coordinates for cursor movement
            screen_x = int(thumb_tip.x * screen_w)
            screen_y = int(thumb_tip.y * screen_h)
            mouse.position = (screen_x, screen_y)

            # Check index finger position relative to middle finger for scroll direction
            now = time.time()

            # Thumb-index pinch → click
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            pinch_dist = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

            if pinch_dist < 40:
                if now - last_click_time > click_cooldown:
                    mouse.click(Button.left)
                    last_click_time = now
                    status = "CLICK"
            elif index_tip.y < middle_tip.y - 0.05:
                # Index finger raised more than middle → scroll up
                if now - last_scroll_time > scroll_delay:
                    mouse.scroll(0, scroll_speed)
                    last_scroll_time = now
                    status = "SCROLL UP"
            elif middle_tip.y < index_tip.y - 0.05:
                # Middle finger raised more than index → scroll down
                if now - last_scroll_time > scroll_delay:
                    mouse.scroll(0, -scroll_speed)
                    last_scroll_time = now
                    status = "SCROLL DOWN"

            # Draw thumb position indicator
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)

    cv2.putText(frame, status, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, "Press 'q' to quit", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.imshow('Scroll & Click Controller', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
