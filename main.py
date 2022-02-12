# Hackatown 2022 Project
# Frederic Jarjour, Eduard Anton, Rayane Sahi, Mohamed Elsamadouny

#asdasdsed
#hello sdnad
# Yoinked code from https://google.github.io/mediapipe/solutions/hands#python-solution-api

import cv2
import mediapipe as mp
import vgamepad as vg

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

gamepad = vg.VX360Gamepad()

cap = cv2.VideoCapture(0) # cap is the camera
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read() # gets the frame
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image) # results
        print(results)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()



def press_button(gamepad_button):
    """
    Available buttons:
    XUSB_GAMEPAD_DPAD_UP = 0x0001
    XUSB_GAMEPAD_DPAD_DOWN = 0x0002
    XUSB_GAMEPAD_DPAD_LEFT = 0x0004
    XUSB_GAMEPAD_DPAD_RIGHT = 0x0008
    XUSB_GAMEPAD_START = 0x0010
    XUSB_GAMEPAD_BACK = 0x0020
    XUSB_GAMEPAD_LEFT_THUMB = 0x0040
    XUSB_GAMEPAD_RIGHT_THUMB = 0x0080
    XUSB_GAMEPAD_LEFT_SHOULDER = 0x0100
    XUSB_GAMEPAD_RIGHT_SHOULDER = 0x0200
    XUSB_GAMEPAD_GUIDE = 0x0400
    XUSB_GAMEPAD_A = 0x1000
    XUSB_GAMEPAD_B = 0x2000
    XUSB_GAMEPAD_X = 0x4000
    XUSB_GAMEPAD_Y = 0x8000
    """

    # Example: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    gamepad.press_button(button=gamepad_button)
    gamepad.update()


def move_joystick(joystick, x, y):
    # Joystick: 0 = left, 1 = right
    # x, y: values between -1 and 1

    if joystick == 0:
        gamepad.move_left_joystick(x_value_float=x, y_value_float=y)
    elif joystick == 1:
        gamepad.move_right_joystick(x_value_float=x, y_value_float=y)
    
    gamepad.update()

def press_trigger(trigger):
    # Trigger: 0 = left, 1 = right

    if trigger == 0:
        gamepad.left_trigger(value=255) # 255 = max value
    elif trigger == 1:
        gamepad.right_trigger(value=255)
    
    gamepad.update()