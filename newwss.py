import cv2
import mediapipe as mp
from newsapi import NewsApiClient

# Initialize NewsAPI client with your API key
newsapi = NewsApiClient(api_key='c52aca84276847a0a6c3968797090f55')

# Function to fetch news headlines from NewsAPI
def fetch_news():
    # Fetch top headlines from India
    top_headlines = newsapi.get_top_headlines(country='in')
    headlines = [article['title'] for article in top_headlines['articles']]
    return headlines

# Function to detect open hand gesture
def detect_open_hand(hand_landmarks):
    thumb_tip_y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y
    index_tip_y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
    if thumb_tip_y < index_tip_y:
        return True
    return False

# Function to detect hands and fetch news headlines
def detect_hands_and_fetch_news():
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video.")
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                if detect_open_hand(hand_landmarks):
                    print("Open hand detected!")
                    headlines = fetch_news()
                    for headline in headlines:
                        print(headline)

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_hands_and_fetch_news()
