# Jordan Dehmel, 2023
# jdehmel@outlook.com
# jedehmel@mavs.coloradomesa.edu

# This file uses Python's type hinting as much as possible

import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

import time
import sys

def get_bin(what: int, digits: int) -> str:
    # Get raw binary (without 0b at the beginning)
    out: str = bin(what + pow(2, digits - 1))[2:]

    # Pad with leading zeros
    while len(out) < digits:
        out = "0" + out

    # Trim any excess
    while len(out) > digits:
        out = out[1:]
    
    # Space-seperate the bytes
    out = " ".join([out[i:i+8] for i in range(0, len(out), 8)])

    return out

def safe_ctime(what: int) -> str:
    out: str = ""
    
    try:
        out = time.ctime(what)
    except:
        # Get approximate year
        year: int = int(what / (60 * 60 * 24 * 365.25))
        year += 1970

        if year < 0:
            out = str(-year) + " B.C.E."
        else:
            out = str(year) + " C.E."

    return out

class TimeApplication:
    def __init__(self) -> None:
        # Create members, but do not start window yet
        self.root: ThemedTk = ThemedTk(theme="breeze")
        
        # Activate fullscreen mode
        self.root.attributes('-fullscreen', True)

        # Add frame
        self.frame: ttk.Frame = ttk.Frame(self.root)
        self.frame.pack(padx=20, pady=200)

        # Set up escape
        self.root.bind("<Escape>", func=self.close)

        # Used to reduce overhead in start screen
        self.current_screen: str = "NULL"

        # Initialize members that will be needed in start screen
        self.raw_time_label: ttk.Label = None
        self.c_time_label: ttk.Label = None
        self.bin_label: ttk.Label = None

        self.time_mode: str = "now"

        self.cur_time: tk.IntVar = tk.IntVar()
        self.slider_var: float = 0.0

        self.outgoing = ""

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

        if self.current_screen == "first":
            self.first_screen()
        elif self.current_screen == "third":
            self.third_screen()

        return
    
    def min(self) -> None:
        self.time_mode = "slider"

        if self.current_screen == "first":
            self.slider_var = -pow(2, 31)
            self.first_screen()
        elif self.current_screen == "third":
            self.slider_var = -pow(2, 63)
            self.third_screen()
    
        return
    
    def max(self) -> None:
        self.time_mode = "slider"

        if self.current_screen == "first":
            self.slider_var = pow(2, 31) - 1
            self.first_screen()
        elif self.current_screen == "third":
            self.slider_var = pow(2, 63) - 1
            self.third_screen()
    
        pass

    def zero(self) -> None:
        self.time_mode = "slider"
        self.slider_var = 0.0

        if self.current_screen == "first":
            self.first_screen()
        elif self.current_screen == "third":
            self.third_screen()

        return

    def now(self) -> None:
        self.time_mode = "now"

        if self.current_screen == "first":
            self.first_screen()
        elif self.current_screen == "third":
            self.third_screen()
        
        return

    # Main screen; Has the clock and links to others
    def first_screen(self) -> None:
        # Create objects only if not previously set up
        # (this fixes flickering issue)
        if self.current_screen != "first":
            if self.outgoing != "":
                self.root.after_cancel(self.outgoing)

            # Clear screen
            self.clear()

            # Title, subtitle, subsubtitle
            ttk.Label(self.frame, text="What Time is It?", font=("Arial", 25)).pack()
            ttk.Label(self.frame,
                text="How do computers know what time it is?\n",
                font=("Arial", 16)).pack()
            ttk.Label(self.frame,
                text="Here's what a computer sees:",
                font=("Arial", 12)).pack()

            # Binary label
            self.bin_label = ttk.Label(self.frame, font=("Monospace", 12))
            self.bin_label.pack()

            ttk.Label(self.frame,
                text="\nThat's called binary! In our numbers, that's:",
                font=("Arial", 12)).pack()

            # Raw UNIX timecode label
            self.raw_time_label = ttk.Label(self.frame,
                                        font=("Monospace", 12))
            self.raw_time_label.pack()

            ttk.Label(self.frame,
                text="\nThat's the number of seconds since 1970.\nComputers can turn this into a date, like this one:",
                font=("Arial", 12)).pack()

            # ctime label (human readable)
            self.c_time_label = ttk.Label(self.frame,
                                         font=("Monospace", 12))
            self.c_time_label.pack()

            ttk.Label(self.frame,
                text="\nMove the slider to see time like a computer!\n",
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

            button_holder: ttk.Frame = ttk.Frame(self.frame)
            button_holder.pack(pady=50)

            # Now button
            ttk.Button(button_holder, text="Now", command=self.now).grid(column=0, row=0)

            # Min button
            ttk.Button(button_holder, text="Min", command=self.min).grid(column=2, row=0)

            # Zero button
            ttk.Button(button_holder, text="Zero", command=self.zero).grid(column=3, row=0)

            # Max button
            ttk.Button(button_holder, text="Max", command=self.max).grid(column=4, row=0)

            ttk.Label(self.frame, text="What happens after max?", font=("Arial", 12)).pack()
            ttk.Button(self.frame, text="Click here to find out", command=self.second_screen).pack()

            ttk.Label(self.frame, text="\nWhat has improved?", font=("Arial", 12)).pack()
            ttk.Button(self.frame, text="Click here to find out", command=self.third_screen).pack()

            # Update status so we don't do this every time
            self.current_screen = "first"
        
        # If in "now" mode, set current time to actual time.
        # Otherwise, set it to whatever the slider is set to.
        if self.time_mode == "now":
            self.cur_time = int(time.time())
        else:
            self.cur_time = int(self.slider_var)

        # Get padded binary representation
        real_bin: str = get_bin(self.cur_time, 32)

        # Construct this screen
        self.bin_label.config(text=real_bin)
        self.raw_time_label.config(text=str(self.cur_time))
        self.c_time_label.config(text=time.ctime(self.cur_time))

        # After 1 second, call this function again
        self.outgoing = self.root.after(1000, self.first_screen)

        return
    
    def second_screen(self) -> None:
        if self.current_screen != "second":
            if self.outgoing != "":
                self.root.after_cancel(self.outgoing)

            self.current_screen = "second"

        pass

    def third_screen(self) -> None:
        if self.current_screen != "third":
            if self.outgoing != "":
                self.root.after_cancel(self.outgoing)

            # Clear screen
            self.clear()

            # Title, subtitle, subsubtitle
            ttk.Label(self.frame, text="What's New in Computer Time?", font=("Arial", 25)).pack()
            ttk.Label(self.frame,
                text="Nowadays, we use twice as many bytes to store the time!\n",
                font=("Arial", 16)).pack()
            ttk.Label(self.frame,
                text="Here's what a computer sees now:",
                font=("Arial", 12)).pack()

            # Binary label
            self.bin_label = ttk.Label(self.frame, font=("Monospace", 12))
            self.bin_label.pack()

            ttk.Label(self.frame,
                text="\nIn our numbers, that's:",
                font=("Arial", 12)).pack()

            # Raw UNIX timecode label
            self.raw_time_label = ttk.Label(self.frame,
                                        font=("Monospace", 12))
            self.raw_time_label.pack()

            ttk.Label(self.frame,
                text="\nThis can store 4,294,967,296 times as many times!\n" +
                    "This number is the date:",
                font=("Arial", 12)).pack()

            # ctime label (human readable)
            self.c_time_label = ttk.Label(self.frame,
                                         font=("Monospace", 12))
            self.c_time_label.pack()

            ttk.Label(self.frame,
                text="\nMove the slider to see how many dates you can see!\n",
                font=("Arial", 12)).pack()

            # Slider for interactivity
            self.slider = ttk.Scale(
                self.frame,
                from_=-pow(2, 63),
                to=pow(2, 63)-1,
                orient='horizontal',
                variable=self.slider_var,
                command=self.on_slider_change,
                length=500
            )
            self.slider.pack()

            button_holder: ttk.Frame = ttk.Frame(self.frame)
            button_holder.pack(pady=50)

            # Now button
            ttk.Button(button_holder, text="Now", command=self.now).grid(column=0, row=0)

            # Min button
            ttk.Button(button_holder, text="Min", command=self.min).grid(column=2, row=0)

            # Zero button
            ttk.Button(button_holder, text="Zero", command=self.zero).grid(column=3, row=0)

            # Max button
            ttk.Button(button_holder, text="Max", command=self.max).grid(column=4, row=0)

            ttk.Label(self.frame, text="What came first?", font=("Arial", 12)).pack()
            ttk.Button(self.frame, text="Click here to find out", command=self.first_screen).pack()

            ttk.Label(self.frame, text="\Why do we need this?", font=("Arial", 12)).pack()
            ttk.Button(self.frame, text="Click here to find out", command=self.second_screen).pack()

            self.current_screen = "third"

        # If in "now" mode, set current time to actual time.
        # Otherwise, set it to whatever the slider is set to.
        if self.time_mode == "now":
            self.cur_time = int(time.time())
        else:
            self.cur_time = int(self.slider_var)

        # Get padded binary representation
        real_bin: str = get_bin(self.cur_time, 64)

        # Construct this screen
        self.bin_label.config(text=real_bin)
        self.raw_time_label.config(text=str(self.cur_time))
        self.c_time_label.config(text=safe_ctime(self.cur_time))

        # After 1 second, call this function again
        self.root.after(1000, self.third_screen)

        return
