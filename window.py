import tkinter as tk
import tkinter.ttk as ttk
import threading
from turtle import width
from PIL import Image, ImageTk

class App(threading.Thread):
    
    def __init__(self, on_window_update, on_map_pressed, on_del_pressed, on_save_pressed, on_train_pressed, on_load_pressed):
        threading.Thread.__init__(self)
        self.start()

        self.loaded = False
        self.selected_action = None
        self.on_window_update = on_window_update
        self.on_map_pressed = on_map_pressed
        self.on_del_pressed = on_del_pressed
        self.on_save_pressed = on_save_pressed
        self.on_load_pressed = on_load_pressed
        self.on_train_pressed = on_train_pressed

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.title("Invision")
        
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        # Resize window
        self.root.geometry("800x1000")
        self.root.resizable(width=False, height=False)

        self.loading_video = tk.Label(self.root, text="Loading video...", font=("Consolas", 14))
        self.loading_video.pack()
        self.video = tk.Label(self.root)
        self.video.pack(fill=tk.X, padx=5, pady=5)

        # Other variables
        self.selected_btn = tk.StringVar()
        self.show_frame_preview = tk.IntVar()
        self.show_frame_preview.set(1)
        self.in_play_mode = tk.IntVar()
        self.in_play_mode.set(0)
        
        # self.canvas = tk.Canvas(self.root)
        # self.canvas.pack()

        self.root.mainloop()

    def map_btn_pressed(self):
        type = self.btn_select.get()
        self.on_map_pressed(self, type)

    def del_btn_pressed(self):
        if self.selected_action != None:
            label = self.actions_list.get(self.selected_action)
            # print(label)
            for i in range(self.actions_list.size()-1, -1, -1):
                if self.actions_list.get(i) == label:
                    self.actions_list.delete(i)
            self.selected_action = None
            self.del_btn.config(state="disabled")
            self.on_del_pressed(self, label)
    
    def save_btn_pressed(self):
        self.on_save_pressed(self)
    
    def load_btn_pressed(self):
        self.on_load_pressed(self)
    
    def train_btn_pressed(self):
        self.on_train_pressed(self)

    def on_actions_list_select(self, event):
        selection = event.widget.curselection()
        if selection:
            self.selected_action = selection[0]
            self.del_btn.config(state="normal")
        else:
            self.selected_action = None
            self.del_btn.config(state="disabled")

    def get_selected_action(self):
        return self.actions_list.get(self.selected_action)

    def disable_controls(self):
        self.btn_select.config(state="disabled")
        self.actions_list.config(state="disabled")
        self.map_btn.config(state="disabled")
        self.del_btn.config(state="disabled")
        self.train_btn.config(state="disabled")

    def enable_controls(self):
        self.btn_select.config(state="readonly")
        self.actions_list.config(state="normal")
        self.map_btn.config(state="normal")
        self.train_btn.config(state="normal")

    def add_to_list(self, item):
        self.actions_list.insert(0, item)

    def update_frame(self, frame):
        
        # Remove loading label
        self.loading_video.pack_forget()

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video.configure(image=imgtk)
        self.video.image = imgtk
        
        if (not self.loaded):

            # self.counter_label = tk.Label(self.root, text="", font=("Consolas", 30))
            # self.counter_label.pack()

            self.training = tk.Frame(self.root)
            self.training.pack(fill=tk.X, padx=1.5, pady=1.5)

            # Progress bar
            self.progress_bar = ttk.Progressbar(self.training, orient = tk.HORIZONTAL, length = 100, mode = "determinate")
            self.progress_bar["value"] = 0
            self.progress_bar.pack(fill=tk.X, padx=100, pady=1.5)

            # Combo box for selecting a button
            self.btn_select = ttk.Combobox(self.training, textvariable=self.selected_btn, state="readonly")
            self.btn_select['values'] = ["Y Button", "X Button", "B Button", "A Button", "Left Joystick"]
            self.btn_select.current(0)
            self.btn_select.pack()

            # List of actions
            # scrollbar = tk.Scrollbar(self.training, orient="vertical")
            self.actions_list = tk.Listbox(self.training, selectmode=tk.SINGLE )
            # scrollbar.config(command=self.actions_list.yview)
            # scrollbar.pack(side="right", fill="y")
            self.actions_list.pack(fill=tk.BOTH, padx=100, pady=1.5)
            self.actions_list.bind("<<ListboxSelect>>", self.on_actions_list_select)            

            # Map new action
            self.map_btn = ttk.Button(self.training, text="Map new action", command=self.map_btn_pressed)
            self.map_btn.pack()

            # Delete action
            self.del_btn = ttk.Button(self.training, text="Delete action",state="disabled", command=self.del_btn_pressed)
            self.del_btn.pack()

            # Train model action
            self.train_btn = ttk.Button(self.training, text="Train model",state="disabled", command=self.train_btn_pressed)
            self.train_btn.pack()  

            # Save model action
            self.save_btn = ttk.Button(self.training, text="Save model", command=self.save_btn_pressed)
            self.save_btn.pack()

            # Load model action
            self.load_btn = ttk.Button(self.training, text="Load model", command=self.load_btn_pressed)
            self.load_btn.pack()

            # Play action
            self.play_checkbox = tk.Checkbutton(self.training, text='Play',variable=self.in_play_mode, onvalue=1, offvalue=0)
            self.play_checkbox.pack()

            self.settings = tk.Frame(self.root)
            self.settings.pack(side=tk.BOTTOM, fill=tk.X, padx=1.5, pady=1.5)

            # Checkbox for enabling/disabling the hand preview
            self.show_preview_checkbox = tk.Checkbutton(self.settings, text='Show Hand Preview',variable=self.show_frame_preview, onvalue=1, offvalue=0)
            self.show_preview_checkbox.pack(side="left")

        else:
            self.on_window_update(self, self.show_frame_preview.get(), self.in_play_mode.get())

        self.loaded = True