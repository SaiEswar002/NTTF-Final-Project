import cv2
import time
import os
import handtrackingmoduleofppt as htm
import mediapipe as mp

# Camera setup
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Load presentation images
folderPath = r"C:\Users\saies\Desktop"
myList = os.listdir(folderPath)
print(f"Found {len(myList)} images in the folder")

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

# Hand detector initialization
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

# MediaPipe setup
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0

while True:
    # Read frame
    success, img = cap.read()
    
    # Detect hands
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if lmList:
        fingers = []
        
        # Thumb detection (different logic for thumb)
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers detection
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        totalFingers = fingers.count(1)
        print(f"Detected fingers: {totalFingers}")
        
        # Apply overlay if valid index
        if 0 < totalFingers <= len(overlayList):
            h, w, c = overlayList[totalFingers - 1].shape
            img[0:h, 0:w] = overlayList[totalFingers - 1]
    
    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
    # Display
    cv2.imshow("Presentation Controller", img)
    cv2.waitKey(1)