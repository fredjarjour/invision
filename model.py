import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from vgamepad import XUSB_BUTTON

model = None

button_ids = {
    "Y Button": [0, XUSB_BUTTON.XUSB_GAMEPAD_Y],
    "X Button": [1, XUSB_BUTTON.XUSB_GAMEPAD_X],
    "B Button": [2, XUSB_BUTTON.XUSB_GAMEPAD_B],
    "A Button": [3, XUSB_BUTTON.XUSB_GAMEPAD_A],
    "DPAD Up": [4, XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP],
    "DPAD Down": [5, XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN],
    "DPAD Left": [6, XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT],
    "DPAD Right": [7, XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT]
}

joystick_ids = {
    "Left Joystick": [4, "left"],
    "Right Joystick": [5, "right"]
}

def get_btn_index(btn_name):
    if btn_name in button_ids:
        return button_ids[btn_name][0]
    elif btn_name in joystick_ids:
        return joystick_ids[btn_name][0]
    else:
        return -1

def get_btn_name(btn_index):
    for info in button_ids.values():
        if info[0] == btn_index:
            return info[1]
    for info in joystick_ids.values():
        if info[0] == btn_index:
            return info[1]
    return -1


def train_model(df):
    global model
    global y_test

    # le = LabelEncoder()
    # df['Label'] = le.fit_transform(df['Label'])

    # for index, row in df.iterrows():
    #     row['Label'] = get_btn_index(row['Label'])
    print(df)
    
    X = df.iloc[:,1:]
    X = X.values
    y = df.iloc[:,0]
    y.to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    gb = GradientBoostingRegressor()

    # Fiting model with best parameters
    model = GradientBoostingRegressor(n_estimators=600, min_samples_split= 8, min_samples_leaf= 1, max_features= 'sqrt', max_depth=4, learning_rate=0.01)
    model.fit(X_train, y_train)

def make_predictions(X_test):
    predictions = model.predict([X_test])
    return predictions

def save_model():
    # Dumps model into a pkl file
    file = open("model.pkl", "wb") 
    pickle.dump(model, file)

def load_model():
    global model
    model = pd.read_pickle(r'model.pkl')