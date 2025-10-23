# Real-Time Driver Monitoring System

This project is a real-time driver monitoring system that uses computer vision to detect signs of drowsiness, yawning, distraction, and head turning in drivers using a webcam. The system leverages facial landmark detection to analyze eye, mouth, and head movements and provides audible alerts to help prevent accidents caused by driver fatigue or inattention.

---

## Features

- **Drowsiness Detection:** Monitors eye aspect ratio (EAR) to detect prolonged eye closure.
- **Yawn Detection:** Monitors mouth aspect ratio (MAR) to detect yawning.
- **Distraction Detection:** Monitors nose position to detect if the driver is looking away from the road.
- **Head Turn Detection:** Detects significant head rotations (yaw) using a 2D→3D landmark mapping and OpenCV's solvePnP. The module runs a short automatic calibration (default 30 frames) to capture a neutral pose, then raises an alert when the estimated yaw angle exceeds a configurable threshold (default ≈25°) or when nose x-position deviates beyond calibrated bounds. Debouncing (consecutive-frame requirement) is used to avoid transient false positives; thresholds and calibration frames are configurable in detector/head_turn_detector.py.
- **Real-Time Alerts:** Plays different sound alerts for each detected event.
- **Visual Feedback:** Draws facial landmarks and displays alert messages on the video feed.

---

## Requirements

- Python 3.7+
- Webcam
- [dlib](https://pypi.org/project/dlib-bin/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [imutils](https://pypi.org/project/imutils/)
- [scipy](https://pypi.org/project/scipy/)
- [pygame](https://pypi.org/project/pygame/) (for sound alerts)
- [playsound](https://pypi.org/project/playsound/) (used in some detectors)

Install dependencies using:

```sh
pip install -r requirements.txt
```

---

## Folder Structure

```
realtime_driver_monitoring/
│
├── main.py
├── requirements.txt
├── .gitignore
├── utils/
│   └── helpers.py
├── detector/
│   ├── eye_detector.py
│   ├── yawn_detector.py
│   ├── gaze_detector.py
│   └── head_turn_detector.py
├── models/
│   └── shape_predictor_68_face_landmarks.dat
└── sounds/
    ├── drowsiness_alert.wav / drowsy_alert.mp3
    ├── yawn_alert.wav / yawn_alert.mp3
    ├── distraction_alert.wav / distraction_alert.mp3
    └── head_turn_alert.wav (optional)
```

> **Note:** Some detectors use `.mp3` files (e.g., `yawn_alert.mp3`), while others use `.wav`. Ensure both formats are available as needed.

---

## How It Works

### Input

- **Video Feed:** The system captures frames from your webcam in real time.

### Processing

1. **Face Detection:** Uses dlib's frontal face detector to locate faces in each frame.
2. **Landmark Detection:** Uses a pre-trained shape predictor to extract 68 facial landmarks.
3. **Feature Extraction:**
   - **Eyes:** Calculates EAR for both eyes.
   - **Mouth:** Calculates MAR for the mouth.
   - **Nose:** Monitors the x-coordinate of the nose tip for distraction.
   - **Head Pose:** Estimates yaw angle for head turn detection.
4. **Event Detection:**
   - **Drowsiness:** If EAR drops below a threshold for a set number of frames, triggers a drowsiness alert.
   - **Yawn:** If MAR exceeds a threshold for a set number of frames, triggers a yawn alert.
   - **Distraction:** If the nose tip moves significantly sideways, triggers a distraction alert.
   - **Head Turn:** Uses selected facial landmarks (nose tip, chin, eye corners, mouth corners) mapped to a simple 3D model and OpenCV's solvePnP to estimate head pose. The detector:
     - Performs an initial calibration (default 30 frames) to determine a neutral nose x-position and nominal yaw.
     - Computes yaw (in degrees) from the rotation vector returned by solvePnP.
     - Triggers an alert when the absolute yaw exceeds the angle threshold (default ~25°) for a configurable number of consecutive frames.
     - Uses a short debounce window to reduce false alarms from quick, harmless movements.
     - Sound: plays sounds/head_turn_alert.wav (or update filename in the detector) when triggered.

### Output

- **Visual:** Draws contours around eyes and mouth, and displays alert messages on the video window.
- **Audio:** Plays a corresponding sound alert for each detected event.

---

## Usage

1. **Download the dlib shape predictor model:**
   - Place `shape_predictor_68_face_landmarks.dat` in the `models/` directory.

2. **Add Sound Files:**
   - Place alert sound files (`drowsiness_alert.wav`/`drowsy_alert.mp3`, `yawn_alert.wav`/`yawn_alert.mp3`, `distraction_alert.wav`/`distraction_alert.mp3`, `head_turn_alert.wav`) in the `sounds/` directory.

3. **Run the Application:**

   ```sh
   python main.py
   ```

4. **Exit:**
   - Press the `ESC` key to exit the application.

---

## Customization

- **Thresholds:** Adjust EAR, MAR, yaw, and frame thresholds in `main.py` or detector modules for sensitivity.
- **Sound Alerts:** Replace sound files in the `sounds/` directory with your preferred alert sounds.

---

## Code Overview

- [`main.py`](main.py): Main application loop. Handles video capture, detection, and alerting.
- [`utils/helpers.py`](utils/helpers.py): Helper functions for model loading, EAR/MAR calculation, and playing alerts.
- [`detector/eye_detector.py`](detector/eye_detector.py): Standalone drowsiness detection logic.
- [`detector/yawn_detector.py`](detector/yawn_detector.py): Standalone yawn detection logic.
- [`detector/gaze_detector.py`](detector/gaze_detector.py): Standalone distraction detection logic.
- [`detector/head_turn_detector.py`](detector/head_turn_detector.py): Standalone head turn detection logic.

---

## Input/Output Summary

| Input         | Output                                      |
|---------------|---------------------------------------------|
| Webcam frames | Video window with alerts and drawn contours |
|               | Audible alerts for drowsiness, yawn, distraction, head turn |

---

## License

This project is for educational and research purposes only.

---