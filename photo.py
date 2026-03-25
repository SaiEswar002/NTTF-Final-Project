import numpy as np
import pyautogui
import time
import cv2
import mediapipe as mp
from PIL import ImageGrab
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # Fixed: use primary camera index 0
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit(1)

PINCH_THRESHOLD = 0.05
capture_photo = False  # Track capture state to avoid repeated captures

# Output directory for captured photos
output_dir = "captured_photos"
os.makedirs(output_dir, exist_ok=True)

while True:
    ret, img = cap.read()
    if not ret or img is None:
        print("Failed to capture frame.")
        break

    img = cv2.flip(img, 1)
    h, w, c = img.shape

    # Fixed: convert to RGB before passing to MediaPipe (was using BGR directly)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calculate normalized distance between thumb and index tips
            distance = np.linalg.norm(
                np.array([thumb_tip.x, thumb_tip.y]) -
                np.array([index_tip.x, index_tip.y])
            )

            if distance < PINCH_THRESHOLD:
                if not capture_photo:
                    capture_photo = True
                    screenshot = ImageGrab.grab()
                    screenshot_np = np.array(screenshot)
                    filename = os.path.join(output_dir, f'photo_{int(time.time())}.jpg')
                    cv2.imwrite(filename, cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR))
                    print(f"Photo captured: {filename}")
            else:
                capture_photo = False  # Reset so the next pinch triggers a new capture

            mp_draw.draw_landmarks(
                img, hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec((0, 0, 255), 2, 2),
                mp_draw.DrawingSpec((0, 255, 0), 4, 2)
            )

            # Display distance and status
            cv2.putText(img, f"Dist: {distance:.3f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            if capture_photo:
                cv2.putText(img, "CAPTURED!", (10, 65),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    cv2.imshow("Photo Capture - Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
