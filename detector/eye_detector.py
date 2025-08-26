from scipy.spatial import distance as dist
from imutils import face_utils
from playsound import playsound

COUNTER = 0
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20
SOUND_PLAYED = False
SOUND_PATH = "sounds/drowsy_alert.mp3"

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def detect_drowsiness(frame, shape):
    global COUNTER, SOUND_PLAYED
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    leftEye = face_utils.shape_to_np(shape)[lStart:lEnd]
    rightEye = face_utils.shape_to_np(shape)[rStart:rEnd]

    ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

    if ear < EAR_THRESHOLD:
        COUNTER += 1
        if COUNTER >= CONSEC_FRAMES:
            if not SOUND_PLAYED:
                playsound(SOUND_PATH)
                SOUND_PLAYED = True
            return True
    else:
        COUNTER = 0
        SOUND_PLAYED = False

    return False
