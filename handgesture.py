import mediapipe as mp
import time
import cv2


class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        # Fixed: pass confidence values as floats, not converted to int percentage
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    def findHands(self, img, draw=True):
        if img is None:
            return img
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handsLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handsLms, self.mpHands.HAND_CONNECTIONS)
        return img  # Fixed: always return img, not only when draw=True

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results is None or not self.results.multi_hand_landmarks:
            return lmList
        if handNo >= len(self.results.multi_hand_landmarks):
            return lmList

        myHand = self.results.multi_hand_landmarks[handNo]
        h, w, _ = img.shape
        for id, lm in enumerate(myHand.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        return lmList  # Fixed: always return lmList, not only when draw=True


def main():
    pTime = 0
    cap = cv2.VideoCapture(0)  # Fixed: use camera index 0
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    detector = handDetector()

    while True:
        success, img = cap.read()
        if not success or img is None:
            print("Failed to capture frame.")
            break

        img = cv2.flip(img, 1)  # Mirror effect
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if lmList:
            print(f"Thumb tip: {lmList[4]}")

        cTime = time.time()
        fps = 1 / (cTime - pTime) if pTime > 0 else 0
        pTime = cTime

        cv2.putText(img, f"FPS: {int(fps)}", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Hand Gesture Tracker", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
