import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
import os

class Database:

    # number_of_frames is the buffer size that represents the number of frames to be used for an single action
    def __init__(self, number_of_frames=10):

        # Creates the list of columns
        self.dfColumns = ['Label']
        self.number_of_frames = number_of_frames  # can adjust the number of frames
        for i in range(21 * self.number_of_frames):
            self.dfColumns.append(f'X{i}')
            self.dfColumns.append(f'Y{i}')
            self.dfColumns.append(f'Z{i}')

            # self.dfColumns.append(f'VX{i}')
            # self.dfColumns.append(f'VY{i}')
            # self.dfColumns.append(f'VZ{i}')

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
        self.dfObj = self.dfObj.loc[self.dfObj["Label"] != label]
        # print(self.dfObj)

    def to_csv(self):
        self.dfObj.to_csv('data.csv')

    def read_csv(self, file):
        data = pd.read_csv(file)
        return data