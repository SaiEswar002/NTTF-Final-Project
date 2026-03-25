import cv2
import mediapipe as mp
from newsapi import NewsApiClient
import time

# Initialize NewsAPI client with your API key
newsapi = NewsApiClient(api_key='c52aca84276847a0a6c3968797090f55')

# Cooldown to avoid fetching news on every frame
last_fetch_time = 0
FETCH_COOLDOWN = 5  # seconds


def fetch_news():
    """Fetch top news headlines from India."""
    top_headlines = newsapi.get_top_headlines(country='in')
    headlines = [article['title'] for article in top_headlines.get('articles', [])]
    return headlines


def detect_open_hand(hand_landmarks):
    """Detect open hand: thumb tip is above index finger tip (lower y = higher on screen)."""
    thumb_tip_y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y
    index_tip_y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
    return thumb_tip_y < index_tip_y


def detect_hands_and_fetch_news():
    cap = cv2.VideoCapture(0)  # Fixed: use primary camera index 0
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

    global last_fetch_time

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video.")
            break

        frame = cv2.flip(frame, 1)  # Fixed: mirror frame for natural interaction
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        status_text = "Show open hand for news"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if detect_open_hand(hand_landmarks):
                    now = time.time()
                    if now - last_fetch_time > FETCH_COOLDOWN:
                        print("Open hand detected! Fetching news...")
                        try:
                            headlines = fetch_news()
                            for headline in headlines:
                                print(f"  - {headline}")
                            last_fetch_time = now
                        except Exception as e:
                            print(f"News API error: {e}")
                    status_text = "Open hand - Headlines fetched!"
                else:
                    status_text = "Fist detected"

        cv2.putText(frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_hands_and_fetch_news()
