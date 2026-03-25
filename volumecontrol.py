from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import mediapipe as mp
import math
import numpy as np

# Initialize hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Get default audio endpoint
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Volume range (min, max in dB)
vol_min, vol_max = volume.GetVolumeRange()[:2]

# Video capture
cap = cv2.VideoCapture(0)  # Fixed: use primary camera index 0
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)  # Mirror effect
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    vol_bar_pct = 0  # For visual feedback

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            try:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Pixel coordinates for visualization
                thumb_x = int(thumb_tip.x * w)
                thumb_y = int(thumb_tip.y * h)
                index_x = int(index_tip.x * w)
                index_y = int(index_tip.y * h)

                # Distance between thumb and index tip
                distance = math.sqrt(
                    (thumb_tip.x - index_tip.x) ** 2 +
                    (thumb_tip.y - index_tip.y) ** 2
                )

                # Fixed: map distance to scalar volume [0.0, 1.0] with interp
                # distance typically ranges from ~0.02 (pinch) to ~0.35 (fully spread)
                vol_scalar = float(np.interp(distance, [0.02, 0.35], [0.0, 1.0]))
                vol_scalar = max(0.0, min(1.0, vol_scalar))

                is_fist = distance < 0.05
                if not is_fist:
                    volume.SetMasterVolumeLevelScalar(vol_scalar, None)

                vol_bar_pct = int(vol_scalar * 100)

                # Draw line between thumb and index
                cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 2)
                cv2.circle(frame, (thumb_x, thumb_y), 8, (0, 0, 255), -1)
                cv2.circle(frame, (index_x, index_y), 8, (255, 0, 0), -1)

                status = "FIST (muted)" if is_fist else f"Vol: {vol_bar_pct}%"
                cv2.putText(frame, status, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

            except Exception as e:
                print(f"Error: {e}")

    # Volume bar visualization on right side
    bar_x, bar_y, bar_h_full = w - 50, 50, h - 100
    bar_filled = int(bar_h_full * vol_bar_pct / 100)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 30, bar_y + bar_h_full), (50, 50, 50), -1)
    cv2.rectangle(frame, (bar_x, bar_y + bar_h_full - bar_filled),
                  (bar_x + 30, bar_y + bar_h_full), (0, 200, 0), -1)
    cv2.putText(frame, f"{vol_bar_pct}%", (bar_x - 5, bar_y + bar_h_full + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.putText(frame, "Press 'q' to quit", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.imshow('Volume Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
