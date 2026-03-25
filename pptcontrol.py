import cv2
import time
import os
import handgesture as htm  # Fixed: import from handgesture.py (the actual module in this project)

# Camera setup
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit(1)

# Load presentation images from a configurable path
folderPath = os.path.join(os.path.dirname(__file__), "presentation_slides")

if not os.path.exists(folderPath):
    os.makedirs(folderPath)
    print(f"Created slides folder: {folderPath}")
    print("Please add your presentation slide images (PNG/JPG) to that folder.")

# Load only valid image files
valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
myList = [f for f in sorted(os.listdir(folderPath))
          if f.lower().endswith(valid_extensions)]
print(f"Found {len(myList)} slide images in '{folderPath}'")

overlayList = []
for imPath in myList:
    full_path = os.path.join(folderPath, imPath)
    image = cv2.imread(full_path)
    if image is not None:
        overlayList.append(image)
    else:
        print(f"Warning: Could not read image '{imPath}'")

# Hand detector initialization
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

pTime = 0

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Failed to capture frame.")
        break

    img = cv2.flip(img, 1)  # Mirror effect

    # Detect hands
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        fingers = []

        # Thumb detection (compare x-axis for thumb)
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers detection (compare y-axis)
        for i in range(1, 5):
            if lmList[tipIds[i]][2] < lmList[tipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        print(f"Detected fingers: {totalFingers}")

        # Apply slide overlay if a valid slide exists for this count
        if overlayList and 0 < totalFingers <= len(overlayList):
            slide = overlayList[totalFingers - 1]
            sh, sw = slide.shape[:2]
            # Resize slide to fit camera frame if needed
            if sh > img.shape[0] or sw > img.shape[1]:
                slide = cv2.resize(slide, (img.shape[1], img.shape[0]))
                sh, sw = slide.shape[:2]
            img[0:sh, 0:sw] = slide

    # FPS display
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime > 0 else 0
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.putText(img, "Press 'q' to quit", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Presentation Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()