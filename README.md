# Real-Time Driver Monitoring System 🚗👀

This project is a **Real-Time Driver Monitoring System** designed to enhance road safety by detecting signs of **drowsiness, yawning, and distraction** using a webcam. It leverages computer vision and machine learning techniques to analyze facial landmarks and trigger alerts when risky behaviors are detected.

---

## ✨ Key Features
- **Drowsiness Detection**  
  Monitors the driver's **Eye Aspect Ratio (EAR)** to detect prolonged eye closure.  
  If eyes remain closed beyond a threshold → triggers **visual + audio alert**.

- **Yawn Detection**  
  Calculates the **Mouth Aspect Ratio (MAR)** to identify yawning.  
  If the mouth remains open beyond a threshold → triggers a **yawn alert**.

- **Distraction Detection**  
  Tracks the position of the **nose tip** to determine if the driver is looking away.  
  If the nose moves significantly sideways → triggers a **distraction alert**.

- **Real-Time Alerts**  
  Plays alert sounds and overlays warning messages on the video feed.

---

## ⚙️ How It Works
1. **OpenCV** captures frames from the webcam.  
2. **dlib’s face detector** and a **pre-trained 68-point facial landmark predictor** extract facial features.  
3. EAR and MAR are calculated to detect **eye closure** and **mouth opening**.  
4. Nose tip position is tracked to check **distraction**.  
5. **pygame** plays alert sounds stored in the `sounds/` directory.  
6. All detection logic is in `main.py`, with utilities in `helpers.py`.

---

## 📂 Project Structure
driver-monitoring/
│── main.py # Main script for video capture, detection, and alerts
│── helpers.py # Helper functions (EAR, MAR, alerts, etc.)
│── requirements.txt # Project dependencies
│── sounds/ # Alert sound files
│── detector/ # Modular detection scripts (optional, not used in main.py)
│── models/ # Pre-trained models (facial landmark predictor)
│ └── shape_predictor_68_face_landmarks.dat (ignored in git)


---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/driver-monitoring.git
cd driver-monitoring

2. Install Dependencies
pip install -r requirements.txt

3. Download Facial Landmark Model

This project requires dlib's 68-point face landmark predictor.
Download it from the official dlib website:

🔗 Download shape_predictor_68_face_landmarks.dat

Then:

# Extract the file
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2

# Move it into models/ directory
mv shape_predictor_68_face_landmarks.dat models/

▶️ Usage

Run the system with:

python main.py


Keep your face visible to the webcam.

Alerts will trigger for drowsiness, yawning, or distraction.

📦 Dependencies

opencv-python

dlib

imutils

scipy

pygame

(Installed automatically via requirements.txt)

🚀 Future Improvements

Add seat-belt detection.

Integrate with vehicle hardware (e.g., alarm/buzzer).

Extend support for multiple drivers (fleet monitoring).
