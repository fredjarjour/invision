import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
import os

class Database:

    # number_of_frames is the buffer size that represents the number of frames to be used for an single action
    def __init__(self, number_of_frames=11):

        # Creates the list of columns
        self.dfColumns = ['Label']
        self.number_of_frames = number_of_frames  # can adjust the number of frames
        for i in range(21 * self.number_of_frames):
            self.dfColumns.append(f'X{i}')
            self.dfColumns.append(f'Y{i}')
            self.dfColumns.append(f'Z{i}')

        self.dfObj = pd.DataFrame(columns=self.dfColumns)


    # data has the form ['label', X[0], Y[0], Z[0], ... X[20], Y[20], Z[20] * nbOfFrames] one at a time
    def append_to_dataframe(self, data):
        row = pd.DataFrame([data], columns = self.dfColumns) # change the data into a pandas dataframe
        self.dfObj = pd.concat([self.dfObj, row], ignore_index=True) # concatenate the row into the entire dataframe


    def generate_training(self): # create copy of dataframe and drop label
        y_train = self.dfObj['Label'].to_numpy()
        y_train = y_train.T
        copy_df = self.dfObj.drop(['Label'], axis = 1)
        X_train = copy_df.to_numpy()

        return (X_train, y_train)

    def delete_label(self, label):
        self.dfObj = self.dfObj.loc[self.dfObj["label"] != label]

    def to_csv(self):
        self.dfObj.to_csv('data.csv')

    def read_csv(self, file):
        data = pd.read_csv(file)
        return data
        

# # Get the images
# IMAGE_FILES = []

# def get_files_names(letter, start, end):
#     img_files = []
#     for i in range(start, end):
#         os.path.join("asl", "asl_alphabet", "a", "a1.jpg")

# with mp_hands.Hands(
#     static_image_mode=True,
#     max_num_hands=1,
#     min_detection_confidence=0.5) as hands:
#     for idx, file in enumerate(IMAGE_FILES):
#         # Read an image, flip it around y-axis for correct handedness output (see above).
#         image = cv2.flip(cv2.imread(file), 1)
#         # Convert the BGR image to RGB before processing.
#         results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#         if not results.multi_hand_landmarks:
#             continue
        
#         for hand_landmarks in results.multi_hand_landmarks:
#             print('hand_landmarks:', hand_landmarks)


# # Make pandas dataframe from the images