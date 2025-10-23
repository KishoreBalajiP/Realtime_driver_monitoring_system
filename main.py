import cv2
import numpy as np
from imutils import face_utils
from utils.helpers import load_model, eye_aspect_ratio, mouth_aspect_ratio, play_alert
from detector.head_turn_detector import detect_head_turn  # Fixed robust detector

# --- Constants ---
EYE_AR_THRESH = 0.25           # Drowsiness threshold
EYE_AR_CONSEC_FRAMES = 20      # Frames before drowsy alert
MOUTH_AR_THRESH = 0.50         # Yawn threshold
YAWN_FRAMES = 15               # Frames before yawn alert
DISTRACTION_LIMIT_LEFT = 220   # Nose X position bounds
DISTRACTION_LIMIT_RIGHT = 420

# --- Counters ---
COUNTER = 0
YAWN_COUNTER = 0

# --- Load models ---
detector, predictor = load_model()

# --- Start webcam ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Error: Could not access webcam.")

print("[System] Starting Driver Monitoring... Please look straight for calibration.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape_np = face_utils.shape_to_np(shape)

        # --- Eye Aspect Ratio ---
        leftEye = shape_np[36:42]
        rightEye = shape_np[42:48]
        ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

        # --- Mouth Aspect Ratio ---
        mouth = shape_np[48:68]
        mar = mouth_aspect_ratio(mouth)

        # --- Draw landmarks ---
        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (0, 0, 255), 1)

        # --- Drowsiness Detection ---
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                play_alert("drowsiness")
        else:
            COUNTER = 0

        # --- Yawn Detection ---
        if mar > MOUTH_AR_THRESH:
            YAWN_COUNTER += 1
            if YAWN_COUNTER >= YAWN_FRAMES:
                cv2.putText(frame, "YAWNING ALERT!", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                play_alert("yawn")
        else:
            YAWN_COUNTER = 0

        # --- Distraction Detection (side movement) ---
        nose = shape_np[30]
        if nose[0] < DISTRACTION_LIMIT_LEFT or nose[0] > DISTRACTION_LIMIT_RIGHT:
            cv2.putText(frame, "DISTRACTION ALERT!", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            play_alert("distraction")

        # --- Head Turn Detection (robust) ---
        direction = detect_head_turn(shape, frame, play_alert)
        if direction == "LEFT":
            cv2.putText(frame, "HEAD TURN LEFT!", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        elif direction == "RIGHT":
            cv2.putText(frame, "HEAD TURN RIGHT!", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        # STRAIGHT → no alert text

    # --- Display output ---
    cv2.imshow("Driver Monitoring System", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        print("[System] Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
