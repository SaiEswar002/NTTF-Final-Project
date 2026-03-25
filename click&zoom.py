import cv2
import mediapipe as mp
import pyautogui
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize hand tracking
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Safety: disable pyautogui fail-safe pause
pyautogui.PAUSE = 0.01

# Main loop
cap = cv2.VideoCapture(0)  # Fixed: use camera index 0 (primary camera)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit(1)

click_threshold = 50   # Adjust this value for sensitivity
zoom_threshold = 100   # Adjust this value for sensitivity

# Cooldown to prevent multiple rapid clicks
last_click_time = 0
click_cooldown = 0.5  # seconds

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Flip the frame horizontally for a selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get thumb and index finger tip positions
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Convert normalized coordinates to pixel coordinates
            h, w, _ = frame.shape
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Map thumb position to screen coordinates
            screen_w, screen_h = pyautogui.size()
            screen_x = int(thumb_tip.x * screen_w)
            screen_y = int(thumb_tip.y * screen_h)
            pyautogui.moveTo(screen_x, screen_y)

            # Calculate Euclidean distance between thumb and index finger tips
            distance = math.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2)

            now = time.time()
            if distance < click_threshold:
                if now - last_click_time > click_cooldown:
                    pyautogui.click()
                    last_click_time = now
            elif distance < zoom_threshold:
                pyautogui.hotkey('ctrl', '+')
            else:
                pyautogui.hotkey('ctrl', '-')

            # Draw circles at thumb and index finger tips
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)

            # Display distance on frame
            cv2.putText(frame, f"Dist: {int(distance)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow('Virtual Mouse - Click & Zoom', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
