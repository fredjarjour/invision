import mediapipe as mp
import pandas as pd
import cv2
import os


# Get the images
IMAGE_FILES = []

def get_files_names(letter, start, end):
    img_files = []
    for i in range(start, end):
        os.path.join("asl", "asl_alphabet", "a", "a1.jpg")


# Pass images through the MediaPipe pipeline to get the landmarks

mp_hands = mp.solutions.hands

data = {"letter": []}

for i in range(21):
    data[f"x{str(i)}"] = []
    data[f"y{str(i)}"] = []
    data[f"z{str(i)}"] = []

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(IMAGE_FILES):
        # Read an image, flip it around y-axis for correct handedness output (see above).
        image = cv2.flip(cv2.imread(file), 1)
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_hand_landmarks:
            continue
        
        for hand_landmarks in results.multi_hand_landmarks:
            print('hand_landmarks:', hand_landmarks)


# Make pandas dataframe from the images