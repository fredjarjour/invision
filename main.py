# Hackatown 2022 Project
# Frederic Jarjour, Eduard Anton, Rayane Sahi, Mohamed Elsamadouny

#asdasdsed
#hello sdnad
# Yoinked code from https://google.github.io/mediapipe/solutions/hands#python-solution-api

from hands import Hands
from gamepad import Gamepad

gamepad : Gamepad = None
hands : Hands = None

def on_results(results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            print(hand_landmarks)

def main():
    global gamepad, hands
    gamepad = Gamepad()
    hands = Hands(on_results)

if (__name__ == '__main__'):
    print("Running.")
    main()