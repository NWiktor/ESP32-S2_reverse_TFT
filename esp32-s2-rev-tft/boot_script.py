""" This module contains functions for booting (runs only once during booting). """

import os
import time
from secrets import secrets
import wifi, ssl, socketpool
import rtc
import board
import terminalio
from adafruit_display_text import bitmap_label
import adafruit_requests



def main():
    """ Shows system data and hello message for 5 seconds. """
    mach_name = os.uname().machine
    sys_name = os.uname().sysname

    start_text = f"Hello, World!\n{mach_name}\nSystem: {sys_name}"
    text_area = bitmap_label.Label(terminalio.FONT, text=start_text, scale=2, color=0xFF00FF)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)
    time.sleep(5)


def set_rtc():
    """ Reads current time from WorldTimeAPI and sets the RTC accordingly. """
    # try:
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    print("Connected, getting WorldTimeAPI time...")
    pool = socketpool.SocketPool(wifi.radio)
    request = adafruit_requests.Session(pool, ssl.create_default_context())

    print("Getting current time...")
    response = request.get("http://worldtimeapi.org/api/ip")
    time_data = response.json()
    unixtime = int(time_data['unixtime']) + int(time_data['raw_offset']) + int(time_data["dst_offset"])
    print("URL time: ", response.headers['date'])

    rtc.RTC().datetime = time.localtime( unixtime ) # create time struct and set RTC with it

    # except Exception as e:
    #     pass


if __name__ == '__main__':
    pass
