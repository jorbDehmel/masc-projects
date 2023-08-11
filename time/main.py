#!/usr/bin/python3
# The above line allows this file to be executable (shebang)

from time_driver import *


if __name__ == '__main__':
    window = TimeApplication()
    window.start_screen()
    window.root.mainloop()

