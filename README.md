# Interactive Leg Extension Tracker

A real-time interactive exercise tracker that monitors leg extensions using your webcam. Built with MediaPipe Pose, OpenCV, and Pygame, this system offers live visual feedback, automatic rep tracking, and a gamified success experience. Designed for amateur athletes, physical therapy patients, and interactive fitness projects.

---

## Features

- Real-time pose tracking using [MediaPipe Pose](https://developers.google.com/mediapipe/solutions/vision/pose)
- Detects leg extensions based on hip-to-ankle distance from center of gravity (COG)
- Requires you to hold each stretch for **3 seconds** to count a rep
- Stretch progress visualized as a circle with live percentage
- Repetition counter for each leg displayed on screen
- Plays a victory sound and shows “Great Job!” when the session is complete (after 5 reps per leg)
- Fullscreen OpenCV display for immersive feedback
- Skips frames and warns the user when hips or ankles are not clearly visible

---

## Project Structure

```text
interactive-leg-extension/
├── assets/
│   └── sounds/
│       └── victory.mp3
├── src/
│   ├── main.py          # Main executable script
│   ├── config.py        # Pose indices and thresholds
│   ├── core/
│   │   └── tracker.py   # LegState class for rep tracking
│   └── utils/
│       ├── pose.py      # COG and stretch logic
│       └── audio.py     # Pygame audio handling
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sersoel/interactive-leg-extension.git
cd interactive-leg-extension-tracker
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Ensure your webcam is connected and the victory sound file exists at `assets/sounds/victory.mp3`.

```bash
python -m src.main
```

> Press `q` to quit at any time.

---

## Configuration

Thresholds and exercise settings can be customized in `src/config.py`:

```python
LEG_HOLD_THRESHOLD_SEC = 3.0
EXTENSION_X_THRESHOLD = 0.15
MAX_REPS = 5
```

---

## Requirements

- Python 3.8+
- `opencv-python`
- `mediapipe`
- `pygame`
- `numpy`

All required packages are listed in `requirements.txt`.

---

## Tips for Best Use

- Use in a clear, well-lit environment
- Position your entire lower body in the webcam frame
- Avoid cluttered backgrounds for accurate pose estimation
- Sit upright during calibration for better COG detection

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Credits

Created by Soheil Samadian  
Powered by [MediaPipe](https://github.com/google/mediapipe), [OpenCV](https://github.com/opencv/opencv), and [Pygame](https://www.pygame.org/)

---

## Future Enhancements

- Add GUI start/stop controls
- Save session summaries to CSV
- Export rep logs per user
- Add sound feedback per rep
