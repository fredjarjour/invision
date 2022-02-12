# Hackatown 2022 Project
# Frederic Jarjour, Eduard Anton, Rayane Sahi, Mohamed Elsamadouny

#asdasdsed
#hello sdnad
# Yoinked code from https://google.github.io/mediapipe/solutions/hands#python-solution-api

from logging import root
from hands import Hands
from gamepad import Gamepad
from vgamepad import XUSB_BUTTON
from window import App

gamepad : Gamepad = None
hands : Hands = None
app : App = None

def on_results(results):
    
    # Check if hands are visible in the frame
    if results.multi_hand_landmarks:
        # for hand_landmarks in results.multi_hand_landmarks:
        #     print(hand_landmarks)
        gamepad.reset()
        print(results.multi_handedness)
        for hand in results.multi_handedness:
            print(hand.classification[0].index)
            
            for c in hand.classification:
                if c.index == 0 and not gamepad.button_pressed["XUSB_GAMEPAD_A"]:
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
                elif c.index == 1 and not gamepad.button_pressed["XUSB_GAMEPAD_B"]:
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
            
            print(gamepad.compare_button(gamepad.gamepad.report.wButtons))

            # gamepad.reset()
            # if hand.classification[0].index == 0:
            #     gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
                
            # if hand.classification[0].index == 1:
            #     gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)

    else:
        gamepad.reset()
        # print(len(results.multi_handedness))
        #print(results.multi_handedness[0].label)
        

def main():
    global gamepad, hands, app
    app = App()
    gamepad = Gamepad()
    hands = Hands(on_results, 1)

if (__name__ == '__main__'):
    print("Running.")
    main()