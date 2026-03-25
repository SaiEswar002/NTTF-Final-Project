# NTTF Final Year Project — Hand Gesture Instructions

## Setup (Run Once)
```bash
pip install -r requirements.txt
```

---

## 1. `SettingsControl.py` — Volume & Brightness Control

**Run:** `python SettingsControl.py`

| Hand | Gesture | Action |
|------|---------|--------|
| **Left hand** | Bring thumb & index finger **close together** | Decrease brightness |
| **Left hand** | Spread thumb & index finger **apart** | Increase brightness |
| **Right hand** | Bring thumb & index finger **close together** | Decrease volume |
| **Right hand** | Spread thumb & index finger **apart** | Increase volume |

> Uses both hands simultaneously. Left = brightness, Right = volume.

---

## 2. `click&zoom.py` — Virtual Mouse Click & Zoom

**Run:** `python "click&zoom.py"`

| Gesture | Action |
|---------|--------|
| Move your **thumb** | Moves the mouse cursor |
| **Pinch** thumb + index finger (distance < 50px) | Left click |
| Thumb + index finger **slightly apart** (50–100px) | Zoom In (`Ctrl +`) |
| Thumb + index finger **far apart** (>100px) | Zoom Out (`Ctrl -`) |

---

## 3. `handgesture.py` — Hand Tracking Module (Library)

This is a **reusable module**, not a standalone app.  
Other scripts (`pptcontrol.py`) import it. Run directly only to test tracking.

**Run:** `python handgesture.py`

| Display | Meaning |
|---------|---------|
| Colored dots on hand | Landmark positions |
| FPS counter | Tracking speed |

---

## 4. `info.py` — Weather, Stock & News Info

**Run:** `python info.py`

| Gesture | Action |
|---------|--------|
| **Pinch** thumb + index finger (distance < 0.07) | Fetch **Weather** (New York) + **Stock Price** (AAPL) |
| **Open hand** (thumb + index far apart) | Fetch **Top 3 News Headlines** |

> Results are printed in the terminal. API cooldown: 5 seconds between calls.

---

## 5. `news.py` — News Headlines

**Run:** `python news.py`

| Gesture | Action |
|---------|--------|
| **Open hand** — thumb tip above index finger tip | Fetch top news headlines from **India** |
| **Fist / closed hand** | No action |

> Headlines are printed in the terminal. Cooldown: 5 seconds.

---

## 6. `newwss.py` — News Headlines (Alternate)

Same as `news.py` — identical functionality with the same gestures.

---

## 7. `photo.py` — Take Screenshots

**Run:** `python photo.py`

| Gesture | Action |
|---------|--------|
| **Pinch** thumb + index finger (normalized distance < 0.05) | Take a **full-screen screenshot** |
| **Release** pinch | Ready for next capture |

> Photos are saved in the `captured_photos/` folder as `photo_<timestamp>.jpg`.

---

## 8. `pptcontrol.py` — Presentation Controller

**Run:** `python pptcontrol.py`

> First add your slide images (PNG/JPG) to the `presentation_slides/` folder.

| Fingers Extended | Action |
|-----------------|--------|
| **1 finger** | Show slide 1 |
| **2 fingers** | Show slide 2 |
| **3 fingers** | Show slide 3 |
| **4 fingers** | Show slide 4 |
| **5 fingers (open hand)** | Show slide 5 |
| **Fist (0 fingers)** | Clear overlay |

> Slides are overlaid on the camera feed based on finger count.

---

## 9. `scroll.py` — Scroll & Click Controller

**Run:** `python scroll.py`

| Gesture | Action |
|---------|--------|
| Move **thumb** | Moves mouse cursor |
| **Pinch** thumb + index finger (< 40px) | Left **click** |
| **Index finger raised** higher than middle finger | **Scroll Up** |
| **Middle finger raised** higher than index finger | **Scroll Down** |

> Click cooldown: 0.5s. Scroll delay: 0.15s.

---

## 10. `test_hand_tracking.py` — Hand Tracking Tester

**Run:** `python test_hand_tracking.py`  
**Options:**
```bash
python test_hand_tracking.py --camera 0 --model full --max_hands 2
```

| Display | Meaning |
|---------|---------|
| **FPS counter** | Tracking speed |
| **"Left" / "Right"** label | Hand classification |
| **Fingers: N** count | Number of extended fingers |
| `h` key | Print help to terminal |
| `q` key | Quit |

> No gesture actions — pure diagnostic/testing tool.

---

## 11. `viewingmap.py` — Interactive Map Viewer

**Run:** `python viewingmap.py`

| Action | Result |
|--------|--------|
| App launches | Shows interactive map centered on **Hyderabad, India** |
| Mouse scroll on map | Zoom in / out |
| Click & drag | Pan the map |

> No hand gesture control. Opens a PyQt5 window with a Folium map.

---

## 12. `volumecontrol.py` — Volume Control (Dedicated)

**Run:** `python volumecontrol.py`

| Gesture | Action |
|---------|--------|
| Spread thumb + index finger **wide** | **High volume** |
| Bring thumb + index finger **close** | **Low volume** |
| **Pinch** (distance < 0.05) → fist | **Mute** (no volume change) |

> Live volume bar displayed on the right side of the camera feed.

---

## 13. `weather.py` — Weather Display

**Run:** `python weather.py`

| Gesture | Action |
|---------|--------|
| **Open hand** — thumb tip above index finger tip | Fetch **current weather** for Hyderabad |
| **Fist / closed hand** | No action |

> Weather info (Temperature, Humidity, Condition, Wind) is displayed on the camera feed.  
> Cooldown: 10 seconds between API calls.

---

## Quick Reference

| Script | Primary Gesture | Output |
|--------|----------------|--------|
| `SettingsControl.py` | Pinch spread (both hands) | System brightness & volume |
| `click&zoom.py` | Pinch / spread | Mouse click & browser zoom |
| `news.py` | Open hand | News in terminal |
| `info.py` | Pinch / open hand | Weather+Stock / News in terminal |
| `photo.py` | Pinch | Screenshot saved to file |
| `pptcontrol.py` | Count fingers (1–5) | Presentation slide overlay |
| `scroll.py` | Index/middle raise + pinch | Mouse scroll & click |
| `volumecontrol.py` | Pinch spread | System volume |
| `weather.py` | Open hand | Weather on screen |
| `viewingmap.py` | *(mouse only)* | Interactive map |
| `test_hand_tracking.py` | Any | Diagnostics only |
