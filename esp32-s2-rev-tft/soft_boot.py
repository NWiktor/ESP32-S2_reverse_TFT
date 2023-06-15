""" This module contains soft boot related functions. """

# pylint: disable = import-error
# pylint: disable = no-member
import os
import time
import board
import terminalio
from adafruit_display_text import bitmap_label


def main():
    """ Shows system data and hello message for 2 seconds. """
    mach_name = os.uname().machine
    sys_name = os.uname().sysname

    start_text = (f"Hello, World!\n{mach_name[:25]}\n{mach_name[26:]}\n"
    + f"System: {sys_name}\nInitializing...")
    text_area = bitmap_label.Label(terminalio.FONT, text=start_text, scale=1, color=0xFF00FF)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.brightness = 1.0
    board.DISPLAY.show(text_area)
    ####
    time.sleep(2) # Important for powering up Feathers properly!
    ####

if __name__ == '__main__':
    pass
