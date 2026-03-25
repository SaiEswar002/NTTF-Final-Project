import cv2
import mediapipe as mp
from math import hypot
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google.protobuf.json_format import MessageToDict
import screen_brightness_control as sbc

# Left Hand for Brightness
# Right Hand for Volume

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.75)
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame.")
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    left_lmList, right_lmList = [], []
    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, handedness in enumerate(results.multi_handedness):
            label = MessageToDict(handedness)['classification'][0]['label']
            hand_lms = results.multi_hand_landmarks[idx]
            h, w, _ = img.shape

            lm_coords = [[int(lm.x * w), int(lm.y * h)] for lm in hand_lms.landmark]
            mpDraw.draw_landmarks(img, hand_lms, mpHands.HAND_CONNECTIONS)

            if label == 'Left':
                left_lmList = lm_coords
            elif label == 'Right':
                right_lmList = lm_coords

    if left_lmList:
        x1, y1 = left_lmList[4][0], left_lmList[4][1]
        x2, y2 = left_lmList[8][0], left_lmList[8][1]

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        length = hypot(x2 - x1, y2 - y1)

        bright = np.interp(length, [15, 200], [0, 100])
        print(f"Brightness: {int(bright)}  Length: {length:.1f}")
        sbc.set_brightness(int(bright))

    if right_lmList:
        x1, y1 = right_lmList[4][0], right_lmList[4][1]
        x2, y2 = right_lmList[8][0], right_lmList[8][1]

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        length = hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [15, 200], [volMin, volMax])
        try:
            volume.SetMasterVolumeLevel(vol, None)
        except Exception as e:
            print("Error setting volume:", e)

        print(f"Volume level: {vol:.2f}  Length: {length:.1f}")

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()