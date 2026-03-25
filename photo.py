import numpy as np
import pyautogui
import imutils
import time
import cv2
import mediapipe as mp
from PIL import ImageGrab

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(1)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

capture_photo = False  # Initialize the capture_photo variable

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    results = hands.process(img)

    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            distance = np.linalg.norm(np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_tip.x, index_tip.y]))

            if distance < 0.05:
                if not capture_photo:
                    capture_photo = True
                    screenshot = ImageGrab.grab()  # Take a screenshot of the entire screen
                    screenshot_np = np.array(screenshot)
                    cv2.imwrite(f'captured_photo_{time.time()}.jpg', cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR))
                    print("Photo captured!")
            else:
                capture_photo = False

            mp_draw.draw_landmarks(img, hand_landmarks,
                                   mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0, 0, 255), 2, 2),
                                   mp_draw.DrawingSpec((0, 255, 0), 4, 2))

    cv2.imshow("hand tracking", img)
    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
