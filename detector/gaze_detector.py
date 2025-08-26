from playsound import playsound

DISTRACTED_COUNTER = 0
DISTRACTED_FRAMES = 25
DISTRACTION_SOUND_PLAYED = False
DISTRACTION_SOUND_PATH = "sounds/distraction_alert.mp3"

def detect_distraction(frame, shape):
    global DISTRACTED_COUNTER, DISTRACTION_SOUND_PLAYED

    nose = shape.part(30)
    chin = shape.part(8)

    dx = abs(nose.x - chin.x)
    if dx > 20:
        DISTRACTED_COUNTER += 1
        if DISTRACTED_COUNTER >= DISTRACTED_FRAMES:
            if not DISTRACTION_SOUND_PLAYED:
                playsound(DISTRACTION_SOUND_PATH)
                DISTRACTION_SOUND_PLAYED = True
            return True
    else:
        DISTRACTED_COUNTER = 0
        DISTRACTION_SOUND_PLAYED = False

    return False
