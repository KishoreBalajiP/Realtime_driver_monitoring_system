import cv2
import numpy as np
from imutils import face_utils

# Calibration variables
neutral_yaw = None
calibration_frames = 30
yaw_values = []

def detect_head_turn(shape, frame, play_alert):
    """
    Detects head turn direction.
    Returns: "LEFT", "RIGHT", or "STRAIGHT"
    """
    global neutral_yaw, yaw_values

    # Convert dlib shape to NumPy array
    shape_np = face_utils.shape_to_np(shape)

    # 3D model points of facial landmarks
    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -330.0, -65.0),        # Chin
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corner
        (-150.0, -150.0, -125.0),    # Left mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
    ])

    # 2D image points from landmarks
    image_points = np.array([
        shape_np[30],  # Nose tip
        shape_np[8],   # Chin
        shape_np[36],  # Left eye left corner
        shape_np[45],  # Right eye right corner
        shape_np[48],  # Left mouth corner
        shape_np[54]   # Right mouth corner
    ], dtype="double")

    h, w = frame.shape[:2]
    focal_length = w
    center = (w / 2, h / 2)

    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))

    # Solve PnP
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return "STRAIGHT"

    rmat, _ = cv2.Rodrigues(rotation_vector)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    yaw = angles[1] * 180  # Yaw in degrees

    # Calibration
    if neutral_yaw is None and len(yaw_values) < calibration_frames:
        yaw_values.append(yaw)
        cv2.putText(frame, "Calibrating... Look Straight!", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if len(yaw_values) == calibration_frames:
            neutral_yaw = np.mean(yaw_values)
            print(f"[HeadTurn] Calibration complete. Neutral yaw = {neutral_yaw:.2f}")
        return "STRAIGHT"

    # Compare yaw to neutral
    deviation = yaw - neutral_yaw
    if deviation > 15:  # turned right
        play_alert("head_turn")
        return "RIGHT"
    elif deviation < -15:  # turned left
        play_alert("head_turn")
        return "LEFT"
    else:
        return "STRAIGHT"
