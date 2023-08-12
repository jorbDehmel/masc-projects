#!/usr/bin/python3
# The above line allows this file to be executable (shebang)
# This is designed to run on a Raspberry Pi with only a mouse

from time_driver import *


if __name__ == '__main__':
    window = TimeApplication()
    window.first_screen()
    window.root.mainloop()

    sys.exit(0)

