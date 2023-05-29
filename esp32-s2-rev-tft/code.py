# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
CircuitPython xxxxxxxxxx
"""

import os
import time
import board
import terminalio
import digitalio
from adafruit_display_text import bitmap_label
import adafruit_bmp3xx

import boot_script

# Favorit colors
# 0xDBFF33
# 0xFFBD33
# 0xFF5733


def check_buttons():
    print(button_d0.value)
    print(button_d1.value)
    print(button_d2.value)
    # print(BUTT_D0)
    # print(BUTT_D1)
    # print(BUTT_D2)


def i2c_search():
    while not i2c.try_lock():
        pass

    try:
        while True:
            print(
                "I2C addresses found:",
                [hex(device_address) for device_address in i2c.scan()],
            )
            time.sleep(2)

    finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
        i2c.unlock()


def get_bmp():
    """ Get data from BMP sensor. """
    pres = "{:6.1f}".format(bmp.pressure)
    temp = "{:5.2f}".format(bmp.temperature)
    alt = "{:.2f}".format(bmp.altitude)
    return pres, temp, alt


def get_disk():
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
    text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=2, color=0x75FF33)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)


def show_atm_stats():
    """  """
    loc_t = time.localtime()
    # cur_date = f"{loc_t[0]}-{loc_t[1]:02d}-{loc_t[2]:02d}"
    cur_time = f"{loc_t[3]:02d}:{loc_t[4]:02d}:{loc_t[5]:02d}"
    pres, temp, alt = get_bmp()

    text = f"Time: {cur_time}\nPres.: {pres} hPa\nTemp.: {temp} °C\nAlt.: {alt} m"
    text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=2, color=0x75FF33)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)


if __name__ == '__main__':

    BUTT_D0 = False
    BUTT_D1 = False
    BUTT_D2 = False

    # Initialize LED
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

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

    # Set RTC and show welcome screen
    boot_script.set_rtc()
    boot_script.main()

    while True:
        # check_buttons()
        show_atm_stats()