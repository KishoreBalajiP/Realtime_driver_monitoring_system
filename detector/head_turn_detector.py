import cv2
from imutils import face_utils

# --- Calibration variables ---
neutral_nose_x = None
calibration_frames = 30
nose_x_values = []

# --- Thresholds ---
YAW_THRESHOLD = 30  # pixels deviation from neutral to trigger alert

def detect_head_turn(shape, frame, play_alert):
    """
    Detects head turn direction based on nose x-position relative to neutral.
    Returns: "LEFT", "RIGHT", or "STRAIGHT".
    Alert only triggers when looking sideways.
    """
    global neutral_nose_x, nose_x_values

    shape_np = face_utils.shape_to_np(shape)
    nose = shape_np[30]  # nose tip (x, y)
    nose_x = nose[0]

    # --- Calibration phase ---
    if neutral_nose_x is None and len(nose_x_values) < calibration_frames:
        nose_x_values.append(nose_x)
        cv2.putText(frame, f"Calibrating... Look Straight! ({len(nose_x_values)}/{calibration_frames})",
                    (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if len(nose_x_values) == calibration_frames:
            neutral_nose_x = sum(nose_x_values) / len(nose_x_values)
            print(f"[HeadTurn] Calibration complete. Neutral nose x = {neutral_nose_x:.2f}")
        return "STRAIGHT"  # no alert during calibration

    # --- Check deviation ---
    deviation = nose_x - neutral_nose_x

    if deviation > YAW_THRESHOLD:
        play_alert("head_turn")
        return "RIGHT"
    elif deviation < -YAW_THRESHOLD:
        play_alert("head_turn")
        return "LEFT"
    else:
        return "STRAIGHT"
