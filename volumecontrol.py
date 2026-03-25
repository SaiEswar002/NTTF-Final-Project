from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import mediapipe as mp
import math

# Initialize hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5)

# Get the default audio endpoint for playback devices
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Create a volume object
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Video capture from the default camera (change the argument if using an external camera)
cap = cv2.VideoCapture(1)

# Desired maximum volume level
max_volume_level = 0.100

while True:
    # Read frames from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe hands
    results = hands.process(rgb_frame)

    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            try:
                # Get the positions of thumb and index finger tips
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

                # Calculate the distance between thumb tip and index finger base
                distance = math.sqrt((thumb_tip.x - index_base.x) ** 2 + (thumb_tip.y - index_base.y) ** 2)

                # Map the distance to volume range (0 to 1)
                volume_level = max(0, min(1, distance))

                # Check if the hand is in a fist (distance is small)
                is_fist = distance < 0.05  # Adjust this threshold based on your preference

                # Set the system volume based on the calculated level, but stop if it's a fist
                if not is_fist:
                    volume.SetMasterVolumeLevelScalar(volume_level, None)

                # Break the loop if the volume exceeds the maximum desired level
                if volume_level >= max_volume_level:
                    break
            except IndexError:
                pass

    # Display the frame
    cv2.imshow('Volume Control', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
