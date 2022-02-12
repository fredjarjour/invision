import vgamepad as vg

class Gamepad:
    def __init__(self):
        self.button_ids = {
            "0x1": "XUSB_GAMEPAD_DPAD_UP",
            "0x2": "XUSB_GAMEPAD_DPAD_DOWN",
            "0x4": "XUSB_GAMEPAD_DPAD_LEFT",
            "0x8": "XUSB_GAMEPAD_DPAD_RIGHT",
            "0x10": "XUSB_GAMEPAD_START",
            "0x20": "XUSB_GAMEPAD_BACK",
            "0x40": "XUSB_GAMEPAD_LEFT_THUMB",
            "0x80": "XUSB_GAMEPAD_RIGHT_THUMB",
            "0x100": "XUSB_GAMEPAD_LEFT_SHOULDER",
            "0x200": "XUSB_GAMEPAD_RIGHT_SHOULDER",
            "0x400": "XUSB_GAMEPAD_GUIDE",
            "0x1000": "XUSB_GAMEPAD_A",
            "0x2000": "XUSB_GAMEPAD_B",
            "0x4000": "XUSB_GAMEPAD_X",
            "0x8000": "XUSB_GAMEPAD_Y"
        }
        
        self.button_pressed = {
            'XUSB_GAMEPAD_DPAD_UP': False, 
            "XUSB_GAMEPAD_DPAD_DOWN": False,
            "XUSB_GAMEPAD_DPAD_LEFT": False,
            "XUSB_GAMEPAD_DPAD_RIGHT": False,
            "XUSB_GAMEPAD_START": False,
            "XUSB_GAMEPAD_BACK": False,
            "XUSB_GAMEPAD_LEFT_THUMB": False,
            "XUSB_GAMEPAD_RIGHT_THUMB": False,
            "XUSB_GAMEPAD_LEFT_SHOULDER": False, 
            "XUSB_GAMEPAD_RIGHT_SHOULDER": False,
            "XUSB_GAMEPAD_GUIDE": False,
            "XUSB_GAMEPAD_A": False,
            "XUSB_GAMEPAD_B": False,
            "XUSB_GAMEPAD_X": False,
            "XUSB_GAMEPAD_Y": False        
        }
    
        self.gamepad = vg.VX360Gamepad()
        
        print("Gamepad initialized.")

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def press_button(self, gamepad_button):
        # Example: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
        self.gamepad.press_button(button=gamepad_button)
        self.button_pressed[gamepad_button] = True
        self.gamepad.update()

    def release_button(self, gamepad_button):
        # Example: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
        self.gamepad.release_button(button=gamepad_button)
        self.button_pressed[gamepad_button] = False
        self.gamepad.update()

    def left_trigger(self, value): # takes values between 0.0 and 1.0
        self.left_trigger_float(value_float = value)
        self.button_pressed["XUSB_GAMEPAD_LEFT_SHOULDER"] = True if value > 0 else False
        self.gamepad.update()

    def right_trigger(self, value): # takes values between 0.0 and 1.0
        self.right_trigger_float(value_float = value)
        self.button_pressed["XUSB_GAMEPAD_RIGHT_SHOULDER"] = True if value > 0 else False
        self.gamepad.update()
    
    def left_joystick(self, x, y): # takes values between -1.0 and 1.0
        self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()

    def right_joystick(self, x, y): # takes values between -1.0 and 1.0
        self.gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()
    
    def reset(self):
        self.gamepad.reset()
        for i in self.button_pressed:
            self.button_pressed[i] = False
        self.gamepad.update()
    
    def compare_button(self, value: int):
        if hex(value) in self.button_ids:
            return self.button_ids[hex(value)]
        else:
            return None