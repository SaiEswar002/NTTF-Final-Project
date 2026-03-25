import cv2
import mediapipe as mp
import requests
from newsapi import NewsApiClient

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# API keys
news_api_key = 'f62878dd351b429b8beef3aa8bf4a555'  # Replace with your News API key
weather_api_key = 'dd6591f39e858fe53f60ba77ed89b4df'  # Replace with your OpenWeatherMap API key
stock_api_key = 'QMZZZMU4FLVOBT8N'  # Replace with your Alpha Vantage API key

# OpenCV setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Distance threshold for thumb-down gesture
THUMB_DOWN_DISTANCE = 0.07  # You may need to adjust this value

# Initialize News API client
news_api = NewsApiClient(api_key=news_api_key)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmarks for thumb tip and index finger tip
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calculate the distance between thumb tip and index finger tip
            distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5

            # Perform actions based on gestures
            if distance < THUMB_DOWN_DISTANCE:
                # Thumb Down Gesture: Check Weather and Stock Prices
                city = 'New York'  # Replace with your city name
                weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}'
                weather_response = requests.get(weather_url)
                weather_data = weather_response.json()

                # Add your code to get stock prices using the Alpha Vantage API
                stock_symbol = 'AAPL'  # Replace with the stock symbol you want to check
                stock_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={stock_api_key}'
                stock_response = requests.get(stock_url)
                stock_data = stock_response.json()

                print("\nWeather Forecast:")
                print(f"- Temperature: {weather_data.get('main', {}).get('temp', 'N/A')}°C")
                print(f"- Description: {weather_data.get('weather', [{}])[0].get('description', 'N/A')}")

                print("\nStock Price:")
                print(f"- Symbol: {stock_symbol}")
                print(f"- Price: {stock_data['Global Quote'].get('05. price', 'N/A')}")

            else:
                # Thumb Up Gesture: Check News
                news_data = news_api.get_top_headlines(country='us')
                print("\nNews Headlines:")
                for article in news_data.get('articles', [])[:3]:
                    print(f"- {article.get('title', 'N/A')}")

    cv2.imshow('Hand Gestures', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
