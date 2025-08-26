from scipy.spatial import distance as dist
from imutils import face_utils
from playsound import playsound

YAWN_COUNTER = 0
YAWN_THRESHOLD = 25
YAWN_FRAMES = 15
YAWN_SOUND_PLAYED = False
YAWN_SOUND_PATH = "sounds/yawn_alert.mp3"

def detect_yawn(frame, shape):
    global YAWN_COUNTER, YAWN_SOUND_PLAYED
    mouth = face_utils.shape_to_np(shape)[48:68]
    vertical = dist.euclidean(mouth[14], mouth[18])

    if vertical > YAWN_THRESHOLD:
        YAWN_COUNTER += 1
        if YAWN_COUNTER >= YAWN_FRAMES:
            if not YAWN_SOUND_PLAYED:
                playsound(YAWN_SOUND_PATH)
                YAWN_SOUND_PLAYED = True
            return True
    else:
        YAWN_COUNTER = 0
        YAWN_SOUND_PLAYED = False

    return False
