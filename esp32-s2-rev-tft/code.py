# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
CircuitPython simple text display demo
"""

import os
import time
import board
import neopixel
import terminalio
import digitalio
from rainbowio import colorwheel
import adafruit_datetime as adt
from adafruit_display_text import bitmap_label

import boot_script

# Favorit colors
# 0xDBFF33
# 0xFFBD33
# 0xFF5733

def rainbow(delay):
    for color_value in range(255):
        pixel[0] = colorwheel(color_value)
        time.sleep(delay)


def get_disk():
    fs_stat = os.statvfs('/')
    disk = (fs_stat[0] * fs_stat[2] / 1024 / 1024) # Disk size in MB
    free = (fs_stat[0] * fs_stat[3] / 1024 / 1024) # Free space in MB
    return f"{free:.2f}/{disk:.2f}"


def main():
    # Second text
    tt = time.localtime()
    cur_date = f"{tt[0]}-{tt[1]:02d}-{tt[2]:02d}" #time.strftime("%Y-%m-%d", time.localtime())
    cur_time = f"{tt[3]:02d}:{tt[4]:02d}:{tt[5]:02d}" #time.strftime("%H:%M:%S", time.localtime())
    mem = get_disk()

    text = f"Date: {cur_date}\nTime: {cur_time}\nDisk: {mem} MB"
    text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=2, color=0x75FF33)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)


if __name__ == '__main__':

    # Set RTC and show welcome screen
    boot_script.set_rtc()
    boot_script.main()


    # Initialize LED
    # led = digitalio.DigitalInOut(board.LED)
    # led.direction = digitalio.Direction.OUTPUT

    # button = digitalio.DigitalInOut(board.BUTTON)
    # button.switch_to_input(pull=digitalio.Pull.UP)

    # pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
    # pixel.brightness = 0.3

    while True:
        main()

        # rainbow(0.02)

        # pixel.fill((255, 0, 0))
        # time.sleep(0.5)
        # pixel.fill((0, 255, 0))
        # time.sleep(0.5)
        # pixel.fill((0, 0, 255))
        # time.sleep(0.5)

        # if not button.value:
        #     BUTTON_PRESSED = True

        # else:
        #     BUTTON_PRESSED = False

        # if BUTTON_PRESSED:
        #     led.value = True
        #     time.sleep(0.5)
        #     led.value = False
        #     time.sleep(0.5)