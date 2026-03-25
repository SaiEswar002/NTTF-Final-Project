# 🖐️ NTTF Final Year Project — AI Hand Gesture Controller

> Control your PC using only hand gestures via a webcam. No mouse. No keyboard.  
> Built with Python, OpenCV, and MediaPipe.

---

## 🚀 Features

| Module | What it does |
|--------|-------------|
| 🔊 `SettingsControl.py` | Control **volume** (right hand) & **brightness** (left hand) |
| 🖱️ `click&zoom.py` | Virtual **mouse click** and **browser zoom** |
| 📰 `news.py` | Fetch **live news headlines** with an open hand |
| 🌤️ `weather.py` | Show **live weather** on camera feed |
| 📸 `photo.py` | Take a **screenshot** with a pinch gesture |
| 📊 `pptcontrol.py` | Control **presentation slides** by counting fingers |
| 🖱️ `scroll.py` | **Scroll** up/down and **click** with hand gestures |
| 🔉 `volumecontrol.py` | Dedicated **volume control** with live bar |
| 🗺️ `viewingmap.py` | View an **interactive map** (Hyderabad) |
| 🧪 `test_hand_tracking.py` | Diagnostic hand tracking tester |
| ℹ️ `info.py` | Gesture-triggered **weather + stock + news** info |

---

## 🛠️ Tech Stack

- **Python 3.x**
- **OpenCV** — Camera feed & image processing
- **MediaPipe** — Real-time hand landmark detection
- **PyAutoGUI / pynput** — Mouse & keyboard automation
- **pycaw** — Windows audio control
- **screen-brightness-control** — Display brightness
- **NewsAPI** — Live news headlines
- **OpenWeatherMap API** — Live weather data
- **Alpha Vantage API** — Stock prices
- **Folium + PyQt5** — Interactive map viewer

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/SaiEswar002/NTTF-Final-Project.git
cd NTTF-Final-Project
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run any module**
```bash
python SettingsControl.py
python "click&zoom.py"
python weather.py
# etc.
```

---

## 🖐️ Gesture Reference

| Gesture | Description |
|---------|-------------|
| **Pinch** | Thumb tip close to index finger tip |
| **Open Hand** | All fingers extended / thumb above index |
| **Fist** | All fingers curled in |
| **Finger Count** | Extend 1–5 fingers to select slide |
| **Index Up / Middle Up** | Scroll up / scroll down |

See **[INSTRUCTIONS.md](INSTRUCTIONS.md)** for the full gesture guide per script.

---

## 📁 Project Structure

```
NTTF-Final-Project/
│
├── SettingsControl.py      # Volume + Brightness control
├── click&zoom.py           # Virtual mouse click & zoom
├── handgesture.py          # Shared hand tracking module
├── info.py                 # Weather + Stock + News
├── news.py                 # News headlines
├── newwss.py               # News headlines (alternate)
├── photo.py                # Screenshot capture
├── pptcontrol.py           # Presentation controller
├── scroll.py               # Scroll & click controller
├── test_hand_tracking.py   # Diagnostic tracker
├── viewingmap.py           # Interactive map viewer
├── volumecontrol.py        # Volume control
├── weather.py              # Weather display
│
├── presentation_slides/    # Add your slides here (for pptcontrol.py)
├── captured_photos/        # Screenshots saved here (auto-created)
│
├── requirements.txt        # All Python dependencies
├── INSTRUCTIONS.md         # Detailed gesture instructions
└── .gitignore
```

---

## 🔑 API Keys

You'll need to replace the placeholder API keys in the respective files:

| File | API | Get Key From |
|------|-----|-------------|
| `info.py`, `weather.py` | OpenWeatherMap | [openweathermap.org](https://openweathermap.org/api) |
| `info.py`, `news.py`, `newwss.py` | NewsAPI | [newsapi.org](https://newsapi.org) |
| `info.py` | Alpha Vantage (stocks) | [alphavantage.co](https://www.alphavantage.co) |

---

## 📋 Requirements

- Windows 10/11
- Python 3.9+
- Webcam
- Good lighting for best gesture detection

---

## 👤 Author

**Sai Eswar**  
NTTF Final Year Project — 2026
