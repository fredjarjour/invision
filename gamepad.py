import vgamepad as vg

class Gamepad:

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

    def __init__(self):
        self.gamepad = vg.VX360Gamepad()

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def press_button(self, gamepad_button):
        # Example: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
        self.gamepad.press_button(button=gamepad_button)
        self.gamepad.update()

    def release_button(self, gamepad_button):
        # Example: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
        self.gamepad.release_button(button=gamepad_button)
        self.gamepad.update()

    def left_trigger(self, value): # takes values between 0.0 and 1.0
        self.left_trigger_float(value_float = value)
        self.gamepad.update()

    def right_trigger(self, value): # takes values between 0.0 and 1.0
        self.right_trigger_float(value_float = value)
        self.gamepad.update()
    
    def left_joystick(self, x, y): # takes values between -1.0 and 1.0
        self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()

    def right_joystick(self, x, y): # takes values between -1.0 and 1.0
        self.gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()
    
    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()