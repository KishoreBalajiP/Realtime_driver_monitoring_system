import cv2
import dlib
import numpy as np
from imutils import face_utils
from utils.helpers import load_model, eye_aspect_ratio, mouth_aspect_ratio, play_alert

# Constants
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 20
MOUTH_AR_THRESH = 0.50

COUNTER = 0
YAWN_COUNTER = 0

# Load dlib models
detector, predictor = load_model()

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # Eyes
        leftEye = shape[36:42]
        rightEye = shape[42:48]
        ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

        # Mouth
        mouth = shape[48:68]
        mar = mouth_aspect_ratio(mouth)

        # Draw contours
        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (0, 0, 255), 1)

        # Drowsiness Detection
        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                play_alert("drowsiness")
        else:
            COUNTER = 0

        # Yawn Detection
        if mar > MOUTH_AR_THRESH:
            YAWN_COUNTER += 1
            if YAWN_COUNTER > 2:
                cv2.putText(frame, "YAWNING ALERT!", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                play_alert("yawn")
        else:
            YAWN_COUNTER = 0

        # Distraction Detection (nose tip moves sideways)
        nose = shape[30]
        if nose[0] < 220 or nose[0] > 420:
            cv2.putText(frame, "DISTRACTION ALERT!", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            play_alert("distraction")

    cv2.imshow("Driver Monitor", frame)
    if cv2.waitKey(1) == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
