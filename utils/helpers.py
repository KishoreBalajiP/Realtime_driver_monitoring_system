import dlib
import os
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load dlib face detector and shape predictor
def load_model():
    detector = dlib.get_frontal_face_detector()
    predictor_path = "models/shape_predictor_68_face_landmarks.dat"
    if not os.path.exists(predictor_path):
        raise FileNotFoundError(f"Missing model file: {predictor_path}")
    predictor = dlib.shape_predictor(predictor_path)
    return detector, predictor

# Calculate Eye Aspect Ratio
def eye_aspect_ratio(eye):
    from scipy.spatial import distance as dist
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Calculate Mouth Aspect Ratio
def mouth_aspect_ratio(mouth):
    from scipy.spatial import distance as dist
    A = dist.euclidean(mouth[13], mouth[19])
    B = dist.euclidean(mouth[14], mouth[18])
    C = dist.euclidean(mouth[15], mouth[17])
    D = dist.euclidean(mouth[12], mouth[16])
    mar = (A + B + C) / (3.0 * D)
    return mar

# Play sound alert using pygame
def play_alert(alert_type):
    sound_path = os.path.join("sounds", f"{alert_type}_alert.wav")
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    else:
        print(f"[Missing Sound] {sound_path}")
