# Jordan Dehmel, 2023
# jdehmel@outlook.com
# jedehmel@mavs.coloradomesa.edu

# This file uses Python's type hinting as much as possible

import tkinter as tk
from tkinter import ttk
from tkinter import font

from ttkthemes import ThemedTk
from PIL import Image, ImageTk

import time

# Get the trimmed & padded & byte-spaced binary version of a number, limited
# to a certain number of bits (digits)


def get_bin(what: int, digits: int) -> str:
    if what + pow(2, digits - 1) >= pow(2, digits):
        return ("11111111 " * (digits // 8))[:-1]

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


# A number for the second screen; This is the starting point
# to demonstrate the integer overflow of 2038
overflow_constant: int = pow(2, 31) - 10

# A safer version of ctime: If it is within the range
# representable, it will return that. Otherwise, it will
# return a rough estimate of the year (CE / BCE)


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

# The actual application running the computer time exhibit


class TimeApplication:
    # Initialize all needed member variables
    def __init__(self) -> None:
        # Create members, but do not start window yet
        self.root: ThemedTk = ThemedTk(theme="breeze")

        temp = list(font.families())
        temp.sort()

        if "Adelle" not in temp or "Amsi Pro Narw" not in temp:
            print("Error: Font(s) not present! Installed fonts:")

            for item in temp:
                print("'" + item + "'")

        # Activate fullscreen mode
        self.root.attributes("-fullscreen", True)

        # Add background image via label
        try:
            # Get screen dimensions
            self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

            # Load unscaled image
            temp = Image.open("images/bg.png")

            # Calculate scaling factor as greatest of h and w scale factors
            scale: float = 1.0

            h_scale: float = (self.h + 10) / temp.height
            w_scale: float = (self.w + 10) / temp.width

            if h_scale > w_scale:
                scale = h_scale
            else:
                scale = w_scale

            # Rescale
            temp = temp.resize(
                size=(int(temp.width * scale), int(temp.height * scale)))
            self.photo = ImageTk.PhotoImage(temp)

            # Set scaled image as background
            self.bg_image: ttk.Label = ttk.Label(self.root, image=self.photo)
            self.bg_image.place(x=0, y=0, relheight=1.0, relwidth=1.0)

        except:
            print("Failed to open background image")
            self.photo = None
            self.bg_image = None

        # These images are mandatory to load, unlike the background
        temp = Image.open("images/next_arrow.png")
        temp = temp.resize(size=(64, 32))
        self.next_arrow_photo = ImageTk.PhotoImage(temp)

        temp = Image.open("images/restart_arrow.png")
        temp = temp.resize(size=(64, 64))
        self.prev_arrow_photo = ImageTk.PhotoImage(temp)

        # Add frame
        self.frame: ttk.Frame = ttk.Frame(self.root)
        self.frame.pack(padx=20, pady=190)

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

    # Close the application. Minimizes, then destroys, then exits
    # in order to have three backup systems.
    def close(self, event) -> None:
        # Just in case
        self.root.attributes('-fullscreen', False)

        # Should work
        self.root.destroy()

        return

    # Janky way to update the slider and its variable
    # every time it is moved
    def on_slider_change(self, event) -> None:
        if self.outgoing != "":
            self.root.after_cancel(self.outgoing)

        self.slider_var = self.slider.get()

        if self.time_mode != "NULL":
            self.time_mode = "slider"

            # Update screen
            if self.current_screen == "first":
                self.first_screen()
            elif self.current_screen == "fifth":
                self.fifth_screen()

        return

    # The function called when the 'min' button is pressed
    # Sets the slider and its variable tot eh minimum position.
    # On screen one, the lowest 32-bit integer. On screen three,
    # the lowest 64-bit integer
    def min(self) -> None:
        self.time_mode = "NULL"

        if self.current_screen == "first":
            self.slider_var = -pow(2, 31)
            self.slider.set(self.slider_var)
            self.time_mode = "slider"

            self.first_screen()

        elif self.current_screen == "fifth":
            self.slider_var = -pow(2, 63)
            self.slider.set(self.slider_var)
            self.time_mode = "slider"

            self.fifth_screen()

        return

    # Same as min, but for the maximal value of the respective
    # integer representations.
    def max(self) -> None:
        self.time_mode = "NULL"

        if self.current_screen == "first":
            self.slider_var = pow(2, 31) - 1
            self.slider.set(self.slider_var)
            self.time_mode = "slider"

            self.first_screen()

        elif self.current_screen == "fifth":
            self.slider_var = pow(2, 63) - 1
            self.slider.set(self.slider_var)
            self.time_mode = "slider"

            self.fifth_screen()

        pass

    # Zeroes out the slider and its variable, no matter the screen
    def zero(self) -> None:
        self.time_mode = "NULL"
        self.slider_var = 0.0
        self.slider.set(0)

        if self.current_screen == "first":
            self.time_mode = "slider"
            self.first_screen()

        elif self.current_screen == "fifth":
            self.time_mode = "slider"
            self.fifth_screen()

        return

    # Sets the slider to the current time's position, no matter
    # the screen. Does not regularly update because you can't really
    # notice the change over a short period of time.
    def now(self) -> None:
        self.time_mode = "NULL"
        self.slider.set(time.time())

        if self.current_screen == "first":
            self.time_mode = "now"

            self.first_screen()

        elif self.current_screen == "fifth":
            self.time_mode = "now"

            self.fifth_screen()

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
            ttk.Label(self.frame, text="What Time is It?",
                      font=("Amsi Pro Narw", 25)).pack()
            ttk.Label(self.frame,
                      text="How do computers know what time it is?\n",
                      font=("Amsi Pro Narw", 16)).pack()

            ttk.Label(self.frame,
                      text="Here's what a computer sees:\n",
                      font=("Adelle", 12)).pack()

            # Binary label
            self.bin_label = ttk.Label(self.frame, font=("Monospace", 16))
            self.bin_label.pack()

            ttk.Label(self.frame,
                      text="\nThat's called binary! In our numbers, that's:\n",
                      font=("Adelle", 12)).pack()

            # Raw UNIX timecode label
            self.raw_time_label = ttk.Label(self.frame,
                                            font=("Monospace", 16))
            self.raw_time_label.pack()

            ttk.Label(self.frame, text="\nThat's the number of seconds since 1970.", font=(
                "Adelle", 12)).pack()
            ttk.Label(self.frame, text="\nComputers can turn this into a date, like this one:\n", font=(
                "Adelle", 12)).pack()

            # ctime label (human readable)
            self.c_time_label = ttk.Label(self.frame,
                                          font=("Monospace", 16))
            self.c_time_label.pack()

            ttk.Label(self.frame,
                      text="\nMove the slider to change the time!\n",
                      font=("Adelle", 12)).pack()

            # Slider for interactivity
            self.slider = ttk.Scale(
                self.frame,
                from_=-pow(2, 31),
                to=pow(2, 31)-1,
                orient='horizontal',
                variable=self.slider_var,
                command=self.on_slider_change,
                length=1000,
                value=time.time()
            )
            self.slider.pack()

            button_holder: ttk.Frame = ttk.Frame(self.frame)
            button_holder.pack(pady=50)

            # Now button
            ttk.Button(button_holder, text="Now",
                       command=self.now).grid(column=0, row=0)

            # Min button
            ttk.Button(button_holder, text="Min",
                       command=self.min).grid(column=2, row=0)

            # Zero button
            ttk.Button(button_holder, text="Zero",
                       command=self.zero).grid(column=3, row=0)

            # Max button
            ttk.Button(button_holder, text="Max",
                       command=self.max).grid(column=4, row=0)

            ttk.Button(self.frame, command=self.second_screen,
                       image=self.next_arrow_photo).pack()

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

            self.clear()

            ttk.Label(self.frame, text="What is binary?",
                      font=("Amsi Pro Narw", 25)).pack()
            ttk.Label(self.frame, text="How can computers count with just 0 and 1?\n", font=(
                "Adelle", 16)).pack()

            # ttk.Label(self.frame, text="", font=("Adelle", 12)).pack()

            ttk.Label(self.frame, text="In real life, we have 10 numbers: 0, 1, 2, 3, 4, 5, 6, 7, 8, and 9.", font=(
                "Adelle", 12)).pack()
            ttk.Label(self.frame, text="But computers only have 0 and 1. This way of counting is called binary.", font=(
                "Adelle", 12)).pack()

            ttk.Label(self.frame, text="\nWe use multiple numbers to make bigger ones (like 12, which is made of a 1 and a 2).", font=(
                "Adelle", 12)).pack()
            ttk.Label(self.frame, text="Computers combine their numbers the same way! A computer would say '10' for 2, or '1100' for 12.", font=(
                "Adelle", 12)).pack()

            ttk.Label(self.frame, text="\nYou could write a number as a math problem like this:", font=(
                "Adelle", 12)).pack()

            ttk.Label(self.frame, text="\n2,345:",
                      font=("Monospace", 12)).pack()

            ttk.Label(self.frame,
                      text='   5 * 1     |   5 * 1                | The one\'s place      \n'
                      + '   4 * 10    |   4 * 1 * 10           | The ten\'s place      \n'
                        + '   3 * 100   |   3 * 1 * 10 * 10      | The hundred\'s place  \n'
                        + ' + 2 * 1,000 | + 2 * 1 * 10 * 10 * 10 | The thousand\'s place \n'
                        + '-------------|------------------------|----------------------\n'
                        + '   2,345     |   2,345                |                      ',
                      font=("Monospace", 12)
                      ).pack()

            ttk.Label(self.frame, text="\nFor us, each digit is ten times larger than the last. In binary, each digit is only two times larger!", font=(
                "Adelle, 12")).pack()

            ttk.Label(self.frame, text="\n0111:",
                      font=("Monospace", 12)).pack()

            ttk.Label(self.frame,
                      text='   1 * 1 |   1 * 1             | The one\'s place   \n'
                      + '   1 * 2 |   1 * 1 * 2         | The two\'s place   \n'
                        + '   1 * 4 |   1 * 1 * 2 * 2     | The four\'s place  \n'
                        + ' + 0 * 8 | + 0 * 1 * 2 * 2 * 2 | The eight\'s place \n'
                        + '---------|---------------------|-------------------\n'
                        + '   7     |   7                 |                   ',
                      font=("Monospace", 12)
                      ).pack()

            ttk.Label(self.frame, text="\nNow you know how to count like a computer!\n", font=(
                "Adelle", 12)).pack()

            ttk.Button(self.frame, image=self.next_arrow_photo,
                       command=self.third_screen).pack()

            self.current_screen = "second"

        return

    def third_screen(self) -> None:
        if self.current_screen != "third":
            if self.outgoing != "":
                self.root.after_cancel(self.outgoing)

            self.clear()

            ttk.Label(self.frame, text="Here are the first few binary numbers:\n", font=(
                "Adelle", 16)).pack()

            ttk.Label(self.frame, text="0000 0000 | 0       0001 0000 | 16\n" +
                                       "0000 0001 | 1       0001 0001 | 17\n" +
                                       "0000 0010 | 2       0001 0010 | 18\n" +
                                       "0000 0011 | 3       0001 0011 | 19\n" +
                                       "0000 0100 | 4       0001 0100 | 20\n" +
                                       "0000 0101 | 5       0001 0101 | 21\n" +
                                       "0000 0110 | 6       0001 0110 | 22\n" +
                                       "0000 0111 | 7       0001 0111 | 23\n" +
                                       "0000 1000 | 8       0001 1000 | 24\n" +
                                       "0000 1001 | 9       0001 1001 | 25\n" +
                                       "0000 1010 | 10      0001 1010 | 26\n" +
                                       "0000 1011 | 11      0001 1011 | 27\n" +
                                       "0000 1100 | 12      0001 1100 | 28\n" +
                                       "0000 1101 | 13      0001 1101 | 29\n" +
                                       "0000 1110 | 14      0001 1110 | 30\n" +
                                       "0000 1111 | 15      0001 1111 | 31\n",
                      font=("Monospace", 16)).pack()

            ttk.Button(self.frame, image=self.next_arrow_photo,
                       command=self.fourth_screen).pack()

            self.current_screen = "third"

        return

    # Secondary screen; Explains what integer overflow is
    # and demonstrates it occuring in 2038.
    def fourth_screen(self) -> None:
        if self.current_screen != "fourth":
            if self.outgoing != "":
                self.root.after_cancel(self.outgoing)

            self.clear()

            ttk.Label(self.frame, text="The 2038 Problem",
                      font=("Amsi Pro Narw", 25)).pack()
            ttk.Label(self.frame, text="How could 99 + 1 = 0?",
                      font=("Amsi Pro Narw", 16)).pack()

            ttk.Label(self.frame, text="\nWhat is 99 + 1? 100! But what if we only have two digits to write the answer?\n",
                      font=("Adelle", 12)).pack()
            ttk.Label(self.frame, text="We would have to write 99 + 1 = 00!\n",
                      font=("Adelle", 12)).pack()
            ttk.Label(self.frame, text="This same thing happens to computers! Here's what a computer sees:", font=(
                "Adelle", 12)).pack()

            ttk.Label(self.frame, text="11111111 + 1 = ?",
                      font=("Monospace", 12)).pack()
            ttk.Label(self.frame, text="11111111 + 1 = 1 00000000",
                      font=("Monospace", 12)).pack()

            ttk.Label(self.frame, text="\nJust like 99 + 1, the computer needs an extra digit for the answer.",
                      font=("Adelle", 12)).pack()
            ttk.Label(self.frame, text="\nThis means that a computer might see this as zero!", font=(
                "Adelle", 12)).pack()
            ttk.Label(self.frame, text="\nThis is called overflow, and it can be a problem for computer time!\n", font=(
                "Adelle", 12)).pack()

            # Binary label
            self.bin_label = ttk.Label(self.frame, font=("Monospace", 16))
            self.bin_label.pack()

            # Raw UNIX timecode label
            self.raw_time_label = ttk.Label(self.frame,
                                            font=("Monospace", 16))
            self.raw_time_label.pack()

            # ctime label (human readable)
            self.c_time_label = ttk.Label(self.frame,
                                          font=("Monospace", 16))
            self.c_time_label.pack()

            ttk.Label(self.frame, text="\nThis will make some computers think 2038 is 1901.", font=(
                "Adelle", 12)).pack()
            ttk.Label(self.frame, text="\nBut don't worry! We have a solution!\n", font=(
                "Adelle", 12)).pack()

            ttk.Button(self.frame, image=self.next_arrow_photo,
                       command=self.fifth_screen).pack()

            self.current_screen = "fourth"

        self.cur_time = int(time.time() % 20) + overflow_constant
        if self.cur_time >= pow(2, 31):
            self.cur_time -= pow(2, 32)

        # Get padded binary representation
        real_bin: str = get_bin(self.cur_time, 32)

        # Construct this screen
        self.bin_label.config(text=real_bin)
        self.raw_time_label.config(text=str(self.cur_time))
        self.c_time_label.config(text=safe_ctime(self.cur_time))

        # After 1 second, call this function again
        self.outgoing = self.root.after(1000, self.fourth_screen)

        return

    # Demonstrates the "new" 64-bit integer representation of computer time
    def fifth_screen(self) -> None:
        if self.current_screen != "fifth":
            if self.outgoing != "":
                self.root.after_cancel(self.outgoing)

            # Clear screen
            self.clear()

            # Title, subtitle, subsubtitle
            ttk.Label(self.frame, text="What's New in Computer Time?",
                      font=("Amsi Pro Narw", 25)).pack()
            ttk.Label(self.frame,
                      text="Nowadays, we use twice as much space to store the time!\n",
                      font=("Amsi Pro Narw", 16)).pack()
            ttk.Label(self.frame,
                      text="Here's what a computer sees now:\n",
                      font=("Adelle", 12)).pack()

            # Binary label
            self.bin_label = ttk.Label(self.frame, font=("Monospace", 16))
            self.bin_label.pack()

            ttk.Label(self.frame,
                      text="\nIn our numbers, that's:\n",
                      font=("Adelle", 12)).pack()

            # Raw UNIX timecode label
            self.raw_time_label = ttk.Label(self.frame,
                                            font=("Monospace", 16))
            self.raw_time_label.pack()

            ttk.Label(self.frame,
                      text="\nThis can store 4,294,967,296 times as much!\n",
                      font=("Adelle", 12)).pack()
            ttk.Label(self.frame,
                      text="This number is about:\n",
                      font=("Adelle", 12)).pack()

            # ctime label (human readable)
            self.c_time_label = ttk.Label(self.frame,
                                          font=("Monospace", 16))
            self.c_time_label.pack()

            ttk.Label(self.frame,
                      text="\nMove the slider to change the time!\n",
                      font=("Adelle", 12)).pack()

            # Slider for interactivity
            self.slider = ttk.Scale(
                self.frame,
                from_=-pow(2, 63),
                to=pow(2, 63)-1,
                orient='horizontal',
                variable=self.slider_var,
                command=self.on_slider_change,
                length=1000
            )
            self.slider.pack()

            ttk.Label(self.frame, text="\nNow overflow won't happen for another 292 billion years!", font=(
                "Adelle", 12)).pack()

            button_holder: ttk.Frame = ttk.Frame(self.frame)
            button_holder.pack(pady=50)

            # Now button
            ttk.Button(button_holder, text="Now",
                       command=self.now).grid(column=0, row=0)

            # Min button
            ttk.Button(button_holder, text="Min",
                       command=self.min).grid(column=2, row=0)

            # Zero button
            ttk.Button(button_holder, text="Zero",
                       command=self.zero).grid(column=3, row=0)

            # Max button
            ttk.Button(button_holder, text="Max",
                       command=self.max).grid(column=4, row=0)

            ttk.Button(self.frame, image=self.prev_arrow_photo,
                       command=self.first_screen).pack()

            self.current_screen = "fifth"

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
        self.outgoing = self.root.after(1000, self.fifth_screen)

        return
