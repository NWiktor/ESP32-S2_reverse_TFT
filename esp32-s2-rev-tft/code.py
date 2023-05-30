# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
CircuitPython xxxxxxxxxx
"""

# pylint: disable = import-error
import os
import time
import board
import terminalio
import digitalio
from adafruit_display_text import bitmap_label
import adafruit_bmp3xx

import soft_boot

# Favorite colors
# 0x75FF33 - lawn green
# 0xDBFF33 - yellow
# 0xFFBD33 - outrageous orange
# 0xFF5733 - red
# 0x3375FF - royal blue


def check_buttons():
    """  """
    global BUTT_D0, MODE
    # print(button_d0.value)
    # print(button_d1.value)
    # print(button_d2.value)

    if button_d0.value != BUTT_D0:
        # BUTT_D0 = button_d0.value
        MODE += 1
        time.sleep(0.5)

    if MODE >= 2:
        MODE = 0



def get_bmp():
    """ Get data from BMP sensor. """
    pres = f"{bmp.pressure:6.1f}"
    temp = f"{bmp.temperature:5.2f}"
    alt = f"{bmp.altitude:.2f}"
    return pres, temp, alt


def get_disk():
    """  """
    fs_stat = os.statvfs('/')
    disk = (fs_stat[0] * fs_stat[2] / 1024 / 1024) # Disk size in MB
    free = (fs_stat[0] * fs_stat[3] / 1024 / 1024) # Free space in MB
    return f"{free:.2f}/{disk:.2f}"


def show_system_stats():
    """  """
    loc_t = time.localtime()
    cur_date = f"{loc_t[0]}-{loc_t[1]:02d}-{loc_t[2]:02d}"
    cur_time = f"{loc_t[3]:02d}:{loc_t[4]:02d}:{loc_t[5]:02d}"
    mem = get_disk()

    text = f"Date: {cur_date}\nTime: {cur_time}\nDisk: {mem} MB"
    text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=2, color=0x3375FF)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)


def show_atm_stats():
    """  """
    loc_t = time.localtime()
    cur_time = f"{loc_t[3]:02d}:{loc_t[4]:02d}:{loc_t[5]:02d}"
    pres, temp, alt = get_bmp()

    text = f"Time: {cur_time}\nPres.: {pres} hPa\nTemp.: {temp} C\nAlt.: {alt} m"
    text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=2, color=0x75FF33)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)


if __name__ == '__main__':

    BUTT_D0 = True # Screen selector
    BUTT_D1 = False
    BUTT_D2 = False
    MODE = 0

    # Initialize LED
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

    # Initialize buttons
    button_d0 = digitalio.DigitalInOut(board.D0)
    button_d0.switch_to_input(pull=digitalio.Pull.UP)
    button_d1 = digitalio.DigitalInOut(board.D1)
    button_d1.switch_to_input(pull=digitalio.Pull.DOWN)
    button_d2 = digitalio.DigitalInOut(board.D2)
    button_d2.switch_to_input(pull=digitalio.Pull.DOWN)

    # For sensor
    i2c = board.I2C()
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    print("Set sea level pressure.")
    bmp.sea_level_pressure = 1013.25
    # bmp.pressure_oversampling = 8
    # bmp.temperature_oversampling = 2

    # Show welcome screen
    soft_boot.main()

    while True:
        check_buttons()

        if MODE == 0:
            show_atm_stats()

        elif MODE == 1:
            show_system_stats()
