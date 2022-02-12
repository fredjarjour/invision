import tkinter as tk
import threading
from PIL import Image, ImageTk
import numpy as np

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        # Resize window
        self.root.geometry("800x600")

        self.label = tk.Label(self.root)
        self.label.pack()
        
        # self.canvas = tk.Canvas(self.root)
        # self.canvas.pack()

        self.root.mainloop()

    def update_frame(self, frame):
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.configure(image=imgtk)
        self.label.image = imgtk