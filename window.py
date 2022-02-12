import tkinter as tk
import threading

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

        label = tk.Label(self.root, text="Hello World")
        label.pack()

        # self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        # self.canvas.pack()

        self.root.mainloop()