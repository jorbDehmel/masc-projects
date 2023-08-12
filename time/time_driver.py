# Jordan Dehmel, 2023
# jdehmel@outlook.com
# jedehmel@mavs.coloradomesa.edu

# This file uses Python's type hinting as much as possible

import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

import time
import sys


class TimeApplication:
    def __init__(self) -> None:
        # Create members, but do not start window yet
        self.root: ThemedTk = ThemedTk(theme="adapta")
        
        # Activate fullscreen mode
        self.root.attributes('-fullscreen', True)

        # Add frame
        self.frame: tk.Frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=200)

        # Set up escape
        self.root.bind("<Escape>", func=self.close)

        # Used to reduce overhead in start screen
        self.has_initialized_start_screen: bool = False

        # Initialize members that will be needed in start screen
        self.raw_time_label: tk.Label = None
        self.c_time_label: tk.Label = None
        self.bin_label: tk.Label = None

        self.time_mode: str = "now"

        self.cur_time: tk.IntVar = tk.IntVar()
        self.slider_var: float = 0.0

        return
    
    # Erase the current window
    def clear(self) -> None:
        # Iterate through items in the frame
        for child in self.frame.winfo_children():
            # Destroy this item
            child.destroy()

        return
    
    def close(self, event) -> None:
        # Just in case
        self.root.attributes('-fullscreen', False)

        # Should work
        self.root.destroy()

        # Just in case it doesn't work
        sys.exit(0)

        return
    
    def on_slider_change(self, event) -> None:
        self.time_mode = "slider"
        self.slider_var = self.slider.get()
        self.start_screen()

        return
    
    def min(self) -> None:
        self.time_mode = "slider"
        self.slider_var = -pow(2, 31)
        self.start_screen()
    
        return
    
    def max(self) -> None:
        self.time_mode = "slider"
        self.slider_var = pow(2, 31) - 1
        self.start_screen()
    
        pass

    def zero(self) -> None:
        self.time_mode = "slider"
        self.slider_var = 0.0
        self.start_screen()
        return

    def now(self) -> None:
        self.time_mode = "now"
        self.start_screen()
        return

    def start_screen(self) -> None:
        # Create objects only if not previously set up
        # (this fixes flickering issue)
        if not self.has_initialized_start_screen:
            # Clear screen
            self.clear()

            # Title
            tk.Label(self.frame, text="What Time is It?", font=("Arial", 25)).pack()
            tk.Label(self.frame,
                text="How do computers know what time it is?\n",
                font=("Arial", 16)).pack()
            
            tk.Label(self.frame,
                text="Here's what a computer sees:",
                font=("Arial", 12)).pack()

            # Binary label
            self.bin_label = tk.Label(self.frame, font=("Monospace", 12))
            self.bin_label.pack()

            tk.Label(self.frame,
                text="\nThat's called binary! In our numbers, that's:",
                font=("Arial", 12)).pack()

            # Raw UNIX timecode label
            self.raw_time_label = tk.Label(self.frame,
                                        font=("Monospace", 12))
            self.raw_time_label.pack()

            tk.Label(self.frame,
                text="\nThat's the number of seconds since 1970.\nComputers can turn this into a date, like this one:",
                font=("Arial", 12)).pack()

            # ctime label (human readable)
            self.c_time_label = tk.Label(self.frame,
                                         font=("Monospace", 12))
            self.c_time_label.pack()

            tk.Label(self.frame,
                text="\nMove the slider to see time like a computer!",
                font=("Arial", 12)).pack()

            # Slider for interactivity
            self.slider = ttk.Scale(
                self.frame,
                from_=-pow(2, 31),
                to=pow(2, 31)-1,
                orient='horizontal',
                variable=self.slider_var,
                command=self.on_slider_change,
                length=500
            )
            self.slider.pack()

            button_holder: tk.Frame = tk.Frame(self.frame)
            button_holder.pack()

            # Now button
            tk.Button(button_holder, text="Now", command=self.now).grid(column=0, row=0)

            # Min button
            tk.Button(button_holder, text="Min", command=self.min).grid(column=2, row=0)

            # Zero button
            tk.Button(button_holder, text="Zero", command=self.zero).grid(column=3, row=0)

            # Max button
            tk.Button(button_holder, text="Max", command=self.max).grid(column=4, row=0)

            # Update status so we don't do this every time
            self.has_initialized_start_screen = True
        
        if self.time_mode == "now":
            self.cur_time = int(time.time())
        else:
            self.cur_time = int(self.slider_var)

        # Get padded binary representation
        real_bin: str = bin(self.cur_time + pow(2, 31))[2:]

        while len(real_bin) < 32:
            real_bin = "0" + real_bin
        
        real_bin = real_bin[:8] + " " + real_bin[8:16] + " " + real_bin[16:24] + " " + real_bin[24:]

        # Construct this screen
        self.bin_label.config(text=real_bin)
        self.raw_time_label.config(text=str(self.cur_time))
        self.c_time_label.config(text=time.ctime(self.cur_time))

        # After 1 second, call this function again
        self.root.after(1000, self.start_screen)

        return
