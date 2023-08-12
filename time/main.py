#!/usr/bin/python3
# The above line allows this file to be executable (shebang)

# Jordan Dehmel, 2023
# jdehmel@outlook.com
# jedehmel@mavs.coloradomesa.edu

'''
This is a short exhibit for a kiosk in the
Grand Junction Math and Science Center (Eureka!).
It demonstrates how computers tell time, talks
about the 2038 integer overflow issue, what
integer overflow is, and how computer scientists
have solved it.

All images used are stored in the images directory.
You should be able to launch this program by
double-clicking main.py from within the time
directory (because of the shebang), but if not
you can run the command
`python3 /path/to/file/here/main.py` to start it.

This program is designed to function with only
a mouse, but a keyboard is required to exit it.
To close the program, simply press escape.
After escape is pressed, the Raspberry Pi running
it can be powered down safely and unplugged.

This program and all associated source code files
are FOSS under the GPLv3, a copy of which should
be attached here. Designed for public educational
use.
'''

from time_driver import *

if __name__ == '__main__':
    try:
        window = TimeApplication()
        window.first_screen()
        window.root.mainloop()
    except:
        print("Unknown failure occured. Restarting program...")

