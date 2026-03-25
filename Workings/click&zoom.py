import cv2
import mediapipe as mp
import pyautogui
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize hand tracking
hands = mp_hands.Hands(min_detection_confidence=0.5)

# Main loop
cap = cv2.VideoCapture(1)
click_threshold = 50  # Adjust this value for sensitivity
zoom_threshold = 100   # Adjust this value for sensitivity

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
            # Get the positions of thumb and index finger tips
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Convert the normalized coordinates to pixel coordinates
            thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
            index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])

            # Move the mouse cursor to the thumb tip position
            pyautogui.moveTo(thumb_x, thumb_y)

            # Calculate the Euclidean distance between thumb and index finger tips
            distance = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)

            # Check for a click gesture (distance less than the click threshold)
            if distance < click_threshold:
                # Perform a click action
                pyautogui.click()

            # Check for a zoom in gesture (distance less than the zoom threshold)
            elif distance < zoom_threshold:
                # Perform a zoom in action
                pyautogui.hotkey('ctrl', '+')

            # Check for a zoom out gesture (distance greater than the zoom threshold)
            else:
                # Perform a zoom out action
                pyautogui.hotkey('ctrl', '-')

            # Draw circles at the thumb and index finger tips
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)

    # Display the frame
    cv2.imshow('Virtual Mouse', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
