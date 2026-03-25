import cv2
import mediapipe as mp
import requests
from newsapi import NewsApiClient

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# API keys (replace with your own valid keys)
news_api_key = 'f62878dd351b429b8beef3aa8bf4a555'
weather_api_key = 'dd6591f39e858fe53f60ba77ed89b4df'
stock_api_key = 'QMZZZMU4FLVOBT8N'

# OpenCV setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit(1)

# Distance threshold for thumb-index pinch gesture
THUMB_DOWN_DISTANCE = 0.07

# Initialize News API client
news_api = NewsApiClient(api_key=news_api_key)

# Cooldown to avoid spamming API calls every frame
import time
last_api_call_time = 0
API_COOLDOWN = 5  # seconds between API calls

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture_label = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmarks for thumb tip and index finger tip
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calculate distance between thumb tip and index finger tip
            distance = ((thumb_tip.x - index_tip.x) ** 2 +
                        (thumb_tip.y - index_tip.y) ** 2) ** 0.5

            now = time.time()
            if now - last_api_call_time > API_COOLDOWN:
                if distance < THUMB_DOWN_DISTANCE:
                    # Pinch gesture: fetch Weather and Stock info
                    gesture_label = "Pinch: Weather & Stock"
                    try:
                        city = 'New York'
                        weather_url = (f'http://api.openweathermap.org/data/2.5/weather'
                                       f'?q={city}&appid={weather_api_key}&units=metric')
                        weather_response = requests.get(weather_url, timeout=5)
                        weather_data = weather_response.json()

                        stock_symbol = 'AAPL'
                        stock_url = (f'https://www.alphavantage.co/query'
                                     f'?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={stock_api_key}')
                        stock_response = requests.get(stock_url, timeout=5)
                        stock_data = stock_response.json()

                        print("\nWeather Forecast:")
                        print(f"  Temperature: {weather_data.get('main', {}).get('temp', 'N/A')}°C")
                        print(f"  Description: {weather_data.get('weather', [{}])[0].get('description', 'N/A')}")

                        print("\nStock Price:")
                        print(f"  Symbol: {stock_symbol}")
                        global_quote = stock_data.get('Global Quote', {})
                        print(f"  Price: {global_quote.get('05. price', 'N/A')}")

                        last_api_call_time = now
                    except requests.RequestException as e:
                        print(f"Network error: {e}")
                else:
                    # Open hand: fetch News
                    gesture_label = "Open: News"
                    try:
                        news_data = news_api.get_top_headlines(country='us')
                        print("\nNews Headlines:")
                        for article in news_data.get('articles', [])[:3]:
                            print(f"  - {article.get('title', 'N/A')}")
                        last_api_call_time = now
                    except Exception as e:
                        print(f"News API error: {e}")

    cv2.putText(frame, gesture_label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow('Hand Gestures', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
