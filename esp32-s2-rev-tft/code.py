# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
CircuitPython xxxxxxxxxx
"""

# pylint: disable = import-error
import os
import time
import board
import busio
import terminalio
import digitalio
from adafruit_display_text import bitmap_label
import adafruit_bmp3xx
import adafruit_gps

import soft_boot

# Favorite colors
# 0x75FF33 - lawn green
# 0xDBFF33 - yellow
# 0xFFBD33 - outrageous orange
# 0xFF5733 - red
# 0x3375FF - royal blue


def check_buttons():
    """  """
    global MODE

    if button_d0.value != BUTT_D0:
        MODE += 1
        time.sleep(0.5)

    if MODE >= 3:
        MODE = 0


def get_bmp():
    """ Get data from BMP sensor. """
    pres = f"{bmp.pressure:6.1f}"
    temp = f"{bmp.temperature:5.2f}"
    alt = f"{bmp.altitude:.2f}"
    return pres, temp, alt


def get_disk():
    """ Get data from storage. """
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


def show_gps_stats(debug=False):
    """  """
    global STEP

    STEP += 1
    text = ""

    # Update data from GPS module
    gps.update()

    if not gps.has_fix:
        # Try again if we don't have a fix yet.
        text = f"Waiting for fix...\nElapsed: {STEP} s"
        if debug:
            print(f'Waiting for fix... ({STEP})')

        time.sleep(1)

    else:
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        if debug:
            print('=' * 40)  # Print a separator line.
            print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
                    gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,   # month!
                    gps.timestamp_utc.tm_sec))
            print(f'Latitude: {gps.latitude} degrees')
            print(f'Longitude: {gps.longitude} degrees')
            print(f'Fix quality: {gps.fix_quality}')
            print(f'Fix quality (3D): {gps.fix_quality_3d}')

            if gps.satellites is not None:
                print(f'# satellites: {gps.satellites}')
            if gps.altitude_m is not None:
                print(f'Altitude: {gps.altitude_m} meters')
            if gps.speed_knots is not None:
                print(f'Speed: {gps.speed_knots} knots')
            if gps.track_angle_deg is not None:
                print(f'Track angle: {gps.track_angle_deg} degrees')
            if gps.horizontal_dilution is not None:
                print(f'Horizontal dilution: {gps.horizontal_dilution}')
            if gps.height_geoid is not None:
                print(f"Height geoid: {gps.height_geoid} meters")
            time.sleep(0.8)

        # Set display text
        status =  f"Quality: {gps.satellites}/12"
        lat_m = f"{gps.latitude_minutes:07.4f}".replace(".","")
        long_m = f"{gps.longitude_minutes:07.4f}".replace(".","")
        latitude = f"Lat.:  {gps.latitude_degrees}.{lat_m}"
        longitude = f"Long.: {gps.longitude_degrees}.{long_m}"
        altitude = f"Alt.: {gps.altitude_m} m"
        speed = f"Speed: {gps.speed_knots} kn"
        text = f"{status}\n{latitude}\n{longitude}\n{altitude}\n{speed}"

    text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=2, color=0xFFBD33)
    text_area.x = 10
    text_area.y = 0
    board.DISPLAY.show(text_area)


if __name__ == '__main__':

    BUTT_D0 = True # Screen selector
    BUTT_D1 = False
    BUTT_D2 = False
    MODE = 0
    STEP = 0
    SEA_LEVEL_PRESSURE = 1013.25

    print("Start initialization...")
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
    time.sleep(1)

    # BMP sensor
    print("Initialize BMP pressure sensor.")
    i2c = board.I2C()
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    print(f"Set sea level pressure to {SEA_LEVEL_PRESSURE} hPa.")
    bmp.sea_level_pressure = SEA_LEVEL_PRESSURE
    # bmp.pressure_oversampling = 8
    # bmp.temperature_oversampling = 2

    # GPS module
    print("Initialize GPS module.")
    # Define RX and TX pins for the board's serial port connected to the GPS.
    # These are the defaults you should use for the GPS FeatherWing.
    # For other boards set RX = GPS module TX, and TX = GPS module RX pins.
    RX = board.RX
    TX = board.TX

    # Create a serial connection for the GPS connection using default speed and
    # a slightly higher timeout (GPS modules typically update once a second).
    uart = busio.UART(TX, RX, baudrate=9600, timeout=2)
    gps = adafruit_gps.GPS(uart)
    time.sleep(2)
    gps.update()
    gps.update()

    # Move to boot.py
    if gps.has_fix:
        print("GPS fixed.")

    else:
        print("Configure GPS module...")
        # print("Query firmware version...")
        # gps.send_command(b'PMTK605') # Query firmware
        # print(uart.readline()) # b'$PMTK705,AXN_2.31_3339_13101700,5632,PA6H,1.0*6B\r\n'
        
        # Turn on the basic GGA and RMC info (what you typically want)
        print("Configure to send GGA and RMC info only.")
        gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on everything
        # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything
        # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Set update rate to once a second (1hz) which is what you typically want.
        gps.send_command(b'PMTK220,1000')
        # Set pedestrian mode
        gps.send_command(b'PMTK886,1')
        # uart.write(b'PGCMD_ANTENNA\r\n')

    # Show welcome screen
    soft_boot.main()

    # Start main loop
    while True:
        check_buttons()

        if MODE == 0:
            show_gps_stats()

        elif MODE == 1:
            show_atm_stats()

        elif MODE == 2:
            show_system_stats()
