import mediapipe as mp
import time
import cv2

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.trakConf = trackCon
        self.detectionCon = int(detectionCon * 100)  # Convert to integer percentage

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.trakConf, self.detectionCon)
        self.mpDraw = mp.solutions.drawing_utils



    
    def findHands(self, img, draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handsLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handsLms,self.mpHands.HAND_CONNECTIONS)
                    return img
    
    def findPosition(self,img,handNo=0,draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, Im in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(Im.x * w), int(Im.y * h)
                lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                return lmList

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        ImList = detector.findPosition(img)

        if ImList is not None:  
            if len(ImList) != 0:
                print(ImList[4])

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

                cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                cv2.imshow("image", img)
                cv2.waitKey(1)

if __name__ == "__main__":
    main()
