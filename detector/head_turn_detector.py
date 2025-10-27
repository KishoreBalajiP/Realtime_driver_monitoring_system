import cv2
import time
from imutils import face_utils

# --- Calibration Data ---
neutral_offset = None
offset_values = []
calibration_frames = 30

# --- Sensitivity ---
TURN_THRESHOLD = 12        # Increase to reduce sensitivity
HOLD_TIME = 0.8            # Seconds head must stay turned

# --- State ---
turn_start_time = None
last_state = "STRAIGHT"


def detect_head_turn(shape, frame, play_alert):
    global neutral_offset, offset_values, turn_start_time, last_state

    shape_np = face_utils.shape_to_np(shape)

    # Face reference points
    left_face_x = shape_np[1][0]
    right_face_x = shape_np[15][0]
    nose_x = shape_np[30][0]

    # Compute center of face
    face_center = (left_face_x + right_face_x) / 2
    offset = nose_x - face_center  # nose shift from face center

    # --- Calibration Phase (Look Straight Normally) ---
    if neutral_offset is None and len(offset_values) < calibration_frames:
        offset_values.append(offset)
        cv2.putText(frame, f"Calibrating... Look Straight ({len(offset_values)}/{calibration_frames})",
                    (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if len(offset_values) == calibration_frames:
            neutral_offset = sum(offset_values) / len(offset_values)
            print(f"[HeadTurn] Calibration Complete → Neutral offset = {neutral_offset:.2f}")
        return "STRAIGHT"

    deviation = offset - neutral_offset

    # Determine direction
    if deviation > TURN_THRESHOLD:
        direction = "RIGHT"
    elif deviation < -TURN_THRESHOLD:
        direction = "LEFT"
    else:
        direction = "STRAIGHT"

    # --- Hold-Time Filtering ---
    if direction != last_state:
        last_state = direction
        turn_start_time = time.time()

    if direction == "STRAIGHT":
        return "STRAIGHT"

    if time.time() - turn_start_time >= HOLD_TIME:
        play_alert("head_turn")
        return direction

    return "STRAIGHT"
