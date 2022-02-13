# Hackatown 2022 Project
# Frederic Jarjour, Eduard Anton, Rayane Sahi, Mohamed Elsamadouny

# Yoinked code from https://google.github.io/mediapipe/solutions/hands#python-solution-api

from logging import root

from cv2 import threshold
from hands import Hands
from gamepad import Gamepad
from vgamepad import XUSB_BUTTON
from window import App
from data import Database
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import model

gamepad : Gamepad = None
hands : Hands = None
app : App = None
database : Database = None

preview_enabled = False

# variable
mapping = False
current_mapping = []
frame_counter = 0
iteration_counter = 0
iterations = 50
current_button = None

play_mode = False

def on_results(handsObj, results, frame, is_right_hand_visible, is_left_hand_visible, velocities):
    global app, gamepad, hands, database, current_mapping, mapping, frame_counter, iteration_counter, iterations, current_button
    
    # Pass the frame to the window
    app.update_frame(frame)

    # Update the hands
    handsObj.set_preview_enabled(preview_enabled)

    # Exit function if no hands are visible
    if not results.multi_hand_landmarks:
        if current_button != None:
            gamepad.reset()
            current_button = None
        return
    
    originX = results.multi_hand_landmarks[0].landmark[0].x
    originY = results.multi_hand_landmarks[0].landmark[0].y
    originZ = results.multi_hand_landmarks[0].landmark[0].z
    # Check if we are assigning controls
    if mapping and frame_counter < database.number_of_frames:
        app.progress_bar["value"] = (database.number_of_frames * iteration_counter + frame_counter)/(database.number_of_frames * (iterations+1)) * 100
        
        # Change results to the right format ['label', X[0], Y[0], Z[0], ... X[20], Y[20], Z[20] * nbOfFrames]
    
    
        new_landmarkers = []
        for landmarker in results.multi_hand_landmarks[0].landmark:
            landmarker.x -= originX
            landmarker.y -= originY
            landmarker.z -= originZ
            new_landmarkers.extend([landmarker.x, landmarker.y, landmarker.z])
        
        current_mapping.extend(new_landmarkers)

        frame_counter += 1

    elif mapping:
        # print("Mapping complete")

        # Scaled data is between 0 and 1
        # scaler = MinMaxScaler()
        # scaled = scaler.fit_transform(current_mapping[1:])

        # After scaling all items except the label, insert the label at the beginning
        # scaled.insert(0, current_mapping[0])

        frame_counter = 0
        database.append_to_dataframe(current_mapping)
        current_mapping = current_mapping[0:1]
        

        if iteration_counter < iterations:
            iteration_counter += 1
            return
        # Add the scaled data to the database
        app.progress_bar["value"] = 0
        iteration_counter = 0
        # print(database.dfObj)
        app.enable_controls()
        mapping = False
    

    # (every frame)
    # When Play mode is activated: 
    # Import model, run it on data and take the ouput to presss button
    if play_mode:
        X_test = []
        for landmarker in results.multi_hand_landmarks[0].landmark:
            landmarker.x -= originX
            landmarker.y -= originY
            landmarker.z -= originZ
            X_test.extend([landmarker.x, landmarker.y, landmarker.z])

        # Scaled data is between 0 and 1
        # scaler = MinMaxScaler()
        # scaled = scaler.fit_transform(X_test)
        
        prediction = model.make_predictions(X_test)[0]
        # print(model.make_predictions(X_test))
        
        # button_ids = {
        #     3: ["Y Button", XUSB_BUTTON.XUSB_GAMEPAD_Y],
        #     2: ["X Button", XUSB_BUTTON.XUSB_GAMEPAD_X],
        #     1: ["B Button", XUSB_BUTTON.XUSB_GAMEPAD_B],
        #     0: ["A Button", XUSB_BUTTON.XUSB_GAMEPAD_A]
        # }



        if current_button == None:
            # print(prediction)
            if abs(prediction - round(prediction)) < 0.1 and model.get_btn_name(round(prediction)) != -1:
                button = model.get_btn_name(round(prediction))
                print(button)

                if isinstance(button, str):
                    # a joystick button
                    if button == "left":
                        gamepad.left_joystick(velocities["left"]["x"] * 100, velocities["left"]["y"] * 100)
                else:
                    # a gamepad button
                    gamepad.press_button(button)
                current_button = round(prediction)
                
                # print(current_button)
        else:
            if abs(prediction - current_button) > 0.3:
                gamepad.reset()
                current_button = None
            # button = model.get_btn_name(round(prediction))
            # print(button)
            # gamepad.reset()
            # if isinstance(button, str):
            #     # a joystick button
            #     if button == "left":
            #         gamepad.left_joystick(0, 0)
            # else:
            #     # a gamepad button
            #     gamepad.release_button(button)
            # current_button = None

            # button = button_ids[current_button]
            # gamepad.release_button(button[1])
            # current_button = None
        
        
    
        # model = pd.read_pickle(r'/file.pkl')
        # input = [array]
        # model.predict(input)

    # database.append_to_dataframe(data)

        # gamepad.reset()
        
        # for hand in results.multi_handedness:
            # print(hand.classification)
            # print(hand.classification[0].index)
            
            # for c in hand.classification:
            #     if c.index == 0 and not gamepad.button_pressed["XUSB_GAMEPAD_A"]:
            #         gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
            #     elif c.index == 1 and not gamepad.button_pressed["XUSB_GAMEPAD_B"]:
            #         gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
            
            # print(gamepad.compare_button(gamepad.gamepad.report.wButtons))

            # gamepad.reset()
            # if hand.classification[0].index == 0:
            #     gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
                
            # if hand.classification[0].index == 1:
            #     gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)

    # else:
        # gamepad.reset()
        # print(len(results.multi_handedness))
        #print(results.multi_handedness[0].label)

def on_map_pressed(application, label):
    global current_mapping, mapping
    application.add_to_list(label) 
    application.disable_controls()
    mapping = True
    current_mapping = [model.get_btn_index(label)]

def on_del_pressed(application, label):
    global database
    database.delete_label(label)

def on_save_pressed(application):
    global database
    model.save_model()
    database.to_csv()

def on_load_pressed(application):
    model.load_model()

def on_train_pressed(application):
    print("Training...")
    application.disable_controls()
    model.train_model(database.dfObj)
    application.enable_controls()
    print("Training complete")


def on_window_update(application, hands_preview_enabled, in_play):
    global preview_enabled, play_mode
    preview_enabled = hands_preview_enabled
    if in_play and not play_mode:
        play_mode = True
        application.disable_controls()
    elif not in_play and play_mode:
        play_mode = False
        application.enable_controls()


if (__name__ == '__main__'):
    print("Running.")
    database = Database(1)
    app = App(on_window_update, on_map_pressed, on_del_pressed, on_save_pressed, on_train_pressed, on_load_pressed)
    gamepad = Gamepad()
    hands = Hands(on_results, 1)