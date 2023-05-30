""" This module contains soft boot related functions. """

# pylint: disable = import-error
import os
import time
import board
import terminalio
from adafruit_display_text import bitmap_label


def main():
    """ Shows system data and hello message for 5 seconds. """
    mach_name = os.uname().machine
    sys_name = os.uname().sysname

    start_text = f"Hello, World!\n{mach_name}\nSystem: {sys_name}"
    text_area = bitmap_label.Label(terminalio.FONT, text=start_text, scale=1, color=0xFF00FF)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)
    time.sleep(5)


if __name__ == '__main__':
    pass
