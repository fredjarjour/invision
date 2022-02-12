# Hackatown 2022 Project
# Frederic Jarjour, Eduard Anton, Rayane Sahi, Mohamed Elsamadouny

# Yoinked code from https://google.github.io/mediapipe/solutions/hands#python-solution-api

from logging import root
from hands import Hands
from gamepad import Gamepad
from vgamepad import XUSB_BUTTON
from window import App
from data import Database
from sklearn.preprocessing import MinMaxScaler

gamepad : Gamepad = None
hands : Hands = None
app : App = None
database : Database = None

preview_enabled = False

# variable
mapping = False
current_mapping = []
frame_counter = 0

def on_results(handsObj, results, frame, is_right_hand_visible, is_left_hand_visible, velocities):
    global app, gamepad, hands, database, current_mapping, mapping, frame_counter
    
    # Pass the frame to the window
    app.update_frame(frame)

    # Update the hands
    handsObj.set_preview_enabled(preview_enabled)

    # Exit function if no hands are visible
    if not results.multi_hand_landmarks:
        return

    # Check if we are assigning controls
    if mapping and frame_counter < database.number_of_frames:
        app.progress_bar["value"] = frame_counter/database.number_of_frames * 100
        
        # Change results to the right format ['label', X[0], Y[0], Z[0], ... X[20], Y[20], Z[20] * nbOfFrames]
        originX = results.multi_hand_landmarks[0].landmark[0].x
        originY = results.multi_hand_landmarks[0].landmark[0].y
        originZ = results.multi_hand_landmarks[0].landmark[0].z

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

        # Add the scaled data to the database
        database.append_to_dataframe(current_mapping)
        
        print(database.dfObj)
        app.enable_controls()
        app.progress_bar["value"] = 0
        mapping = False
        frame_counter = 0
        # merge it with label
        
    # When Play mode is activated: 
    # Import model, run it on data and take the ouput to presss button

    
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
    current_mapping = [label]

def on_del_pressed(application, label):
    global database
    database.delete_label(label)

def on_save_pressed(application):
    global database
    database.to_csv()


def on_window_update(hands_preview_enabled):
    global preview_enabled
    preview_enabled = hands_preview_enabled


if (__name__ == '__main__'):
    print("Running.")
    database = Database()
    app = App(on_window_update, on_map_pressed, on_del_pressed, on_save_pressed)
    gamepad = Gamepad()
    hands = Hands(on_results, 1)