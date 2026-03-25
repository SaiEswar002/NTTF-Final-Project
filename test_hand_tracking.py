import cv2
import mediapipe as mp
import time
import argparse

# Initialize MediaPipe Hands with better configuration
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Command line arguments
parser = argparse.ArgumentParser(description='Hand Tracking with MediaPipe')
parser.add_argument('--camera', type=int, default=0, help='Camera index (default: 0)')
parser.add_argument('--model', type=str, default='full', choices=['lite', 'full'], help='Hand model complexity')
parser.add_argument('--max_hands', type=int, default=2, help='Maximum number of hands to detect')
args = parser.parse_args()

# Initialize MediaPipe Hands with configurable parameters
model_complexity = 1 if args.model == 'full' else 0
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=args.max_hands,
    model_complexity=model_complexity,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize webcam with error handling
cap = cv2.VideoCapture(args.camera)
if not cap.isOpened():
    print(f"Error: Could not open camera {args.camera}")
    exit(1)

# FPS calculation
prev_time = 0
curr_time = 0

print("Hand Tracking started. Press 'q' to quit, 'h' for help")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame")
        break

    # Flip image for mirror effect
    img = cv2.flip(img, 1)
    
    # Convert to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process hand detection
    results = hands.process(imgRGB)
    
    # Calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
    prev_time = curr_time
    
    # Draw FPS counter
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Draw hand count
    hand_count = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0
    cv2.putText(img, f'Hands: {hand_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2, cv2.LINE_AA)
    
    if results.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Get hand classification (left/right)
            hand_label = "Unknown"
            if results.multi_handedness:
                hand_label = results.multi_handedness[hand_idx].classification[0].label
            
            # Draw hand landmarks and connections
            mp_drawing.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # Draw hand label
            h, w, c = img.shape
            cx = int(hand_landmarks.landmark[0].x * w)
            cy = int(hand_landmarks.landmark[0].y * h) - 30
            cv2.putText(img, f'{hand_label}', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 0, 0), 2, cv2.LINE_AA)
            
            # Basic gesture recognition - check if hand is open
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]
            
            # Check if fingers are extended (simple gesture detection)
            fingers_extended = 0
            if thumb_tip.x < hand_landmarks.landmark[3].x:  # Thumb check
                fingers_extended += 1
            if index_tip.y < hand_landmarks.landmark[6].y:  # Index finger
                fingers_extended += 1
            if middle_tip.y < hand_landmarks.landmark[10].y:  # Middle finger
                fingers_extended += 1
            if ring_tip.y < hand_landmarks.landmark[14].y:  # Ring finger
                fingers_extended += 1
            if pinky_tip.y < hand_landmarks.landmark[18].y:  # Pinky finger
                fingers_extended += 1
            
            # Display gesture info
            gesture_text = f'Fingers: {fingers_extended}'
            cv2.putText(img, gesture_text, (cx, cy + 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 0, 255), 2, cv2.LINE_AA)

    # Display help text
    cv2.putText(img, "Press 'q' to quit", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Display the image
    cv2.imshow("Hand Tracking", img)
    
    # Handle key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('h'):
        print("Help:")
        print("- Press 'q' to quit")
        print("- Press 'h' to show this help")
        print("- Command line arguments:")
        print("  --camera [index] - Camera index (default: 0)")
        print("  --model [lite|full] - Model complexity (default: full)")
        print("  --max_hands [number] - Maximum hands to detect (default: 2)")

# Clean up
cap.release()
cv2.destroyAllWindows()
