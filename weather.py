import cv2
import mediapipe as mp
import requests
import time

# ── Configuration ─────────────────────────────────────────────────────────────
WEATHER_API_KEY = 'dd6591f39e858fe53f60ba77ed89b4df'  # Replace with your OpenWeatherMap key
DEFAULT_CITY = 'Hyderabad'                              # Change to your city
UNITS = 'metric'                                        # 'metric' → °C, 'imperial' → °F
FETCH_COOLDOWN = 10  # Seconds between weather API calls

# ── MediaPipe Setup ───────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

# ── Camera Setup ──────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def fetch_weather(city: str) -> dict:
    """Fetch current weather for a given city from OpenWeatherMap."""
    url = (f'http://api.openweathermap.org/data/2.5/weather'
           f'?q={city}&appid={WEATHER_API_KEY}&units={UNITS}')
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Weather fetch error: {e}")
        return {}


def detect_open_hand(hand_landmarks) -> bool:
    """Return True if thumb tip is above index finger tip (open/raised hand)."""
    thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    return thumb_y < index_y


# ── State ─────────────────────────────────────────────────────────────────────
last_fetch_time = 0
weather_info = {}
city = DEFAULT_CITY

# ── Main Loop ─────────────────────────────────────────────────────────────────
print("Weather + Hand Gesture app started. Show open hand to fetch weather. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture_text = "Show open hand for weather"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            now = time.time()
            if detect_open_hand(hand_landmarks):
                if now - last_fetch_time > FETCH_COOLDOWN:
                    print(f"Open hand detected! Fetching weather for {city}...")
                    weather_info = fetch_weather(city)
                    last_fetch_time = now
                gesture_text = f"Open hand → {city} weather"
            else:
                gesture_text = "Fist detected"

    # Display weather data on frame
    y_offset = 35
    cv2.putText(frame, gesture_text, (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    y_offset += 35

    if weather_info:
        main_data = weather_info.get('main', {})
        weather_list = weather_info.get('weather', [{}])
        wind_data = weather_info.get('wind', {})

        unit_symbol = '°C' if UNITS == 'metric' else '°F'
        lines = [
            f"City: {weather_info.get('name', city)}",
            f"Temp: {main_data.get('temp', 'N/A')}{unit_symbol}  "
            f"Feels like: {main_data.get('feels_like', 'N/A')}{unit_symbol}",
            f"Humidity: {main_data.get('humidity', 'N/A')}%",
            f"Condition: {weather_list[0].get('description', 'N/A').title()}",
            f"Wind: {wind_data.get('speed', 'N/A')} m/s",
        ]
        for line in lines:
            cv2.putText(frame, line, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 1)
            y_offset += 28

    cv2.putText(frame, "Press 'q' to quit", (10, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.imshow('Weather - Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
