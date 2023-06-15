"""
This is the main code.
Initializes the main loop, and main functions for the device.
"""

# pylint: disable = import-error
# pylint: disable = no-member
import os
import time
import board
import busio
import terminalio
import digitalio
import microcontroller
from adafruit_display_text import bitmap_label
import adafruit_bmp3xx
import adafruit_gps
import adafruit_max1704x

import soft_boot

### Favorite colors
# 0x75FF33 - lawn green
# 0xDBFF33 - yellow
# 0xFFBD33 - outrageous orange
# 0xFF5733 - red
# 0x3375FF - royal blue
# 0xFF00FF - pink

# Set global variables
MODE = 0
SCREEN_ON = time.time()
LAST_FIX_DATE = time.time()


def check_buttons():
    """ Check button status (pressed or not) and sets, increments flag accordingly. """
    global MODE, SCREEN_ON

    if button_d0.value != BUTT_D2:
        MODE += 1
        SCREEN_ON = time.time()
        time.sleep(0.5)

    if MODE >= 4:
        MODE = 0


def check_screen_ontime_limit(secs=20):
    """ Check if screen ontime reached a given secundums. """
    secs_screen_on = int(time.time() - SCREEN_ON)
    if secs_screen_on >= secs:
        return True
    return False


def get_bmp():
    """ Get data from BMP sensor. """
    pres = f"{bmp.pressure:6.1f}"
    temp = f"{bmp.temperature:5.2f}"
    alt = f"{bmp.altitude:.2f}"
    return pres, temp, alt


def get_disk():
    """ Get avalaiable disk space value. """
    fs_stat = os.statvfs('/')
    disk = (fs_stat[0] * fs_stat[2] / 1024 / 1024) # Disk size in MB
    free = (fs_stat[0] * fs_stat[3] / 1024 / 1024) # Free space in MB
    return f"{free:.2f}/{disk:.2f}"


def show_system_stats():
    """ Show system related data (time, date, memory and battery status). """
    loc_t = time.localtime()
    cur_date = f"Date: {loc_t[0]}-{loc_t[1]:02d}-{loc_t[2]:02d}"
    cur_time = f"Time: {loc_t[3]:02d}:{loc_t[4]:02d}:{loc_t[5]:02d}"
    mem = f"Disk: {get_disk()}"
    bat = f"Bat.: {monitor.cell_voltage:.2f}V / {monitor.cell_percent:.0f}%"
    cpu_temp = f"CPU temp.: {microcontroller.cpu.temperature} C"
    text = f"{cur_date}\n{cur_time}\n{mem} MB\n{bat}\n{cpu_temp}"
    set_display(text, 0x3375FF) # Set display


def show_atm_stats():
    """ Show measured atmospheric data. """
    loc_t = time.localtime()
    cur_time = f"Time: {loc_t[3]:02d}:{loc_t[4]:02d}:{loc_t[5]:02d}"
    pres, temp, alt = get_bmp()
    text = f"{cur_time}\nPres.: {pres} hPa\nTemp.: {temp} C\nAlt.: {alt} m"
    set_display(text, 0x75FF33) # Set display


def show_gps_bmp_stats():
    """ Show measured altitude from GPS and pressure sensor simultaneously. """
    gps.update() # Update data from GPS module

    if not gps.has_fix: # If we don't have a fix yet.
        status = "Waiting for fix..."
        altitude = "Alt.: - m (GPS)"

    else:
        status =  f"Quality: {gps.satellites}/12"
        altitude = f"Alt.: {gps.altitude_m} m (GPS)"

    pres, temp, alt = get_bmp()
    text = f"{status}\n{altitude}\nAlt.: {alt} m\nPres.: {pres} hPa\nTemp.: {temp} C"
    set_display(text, 0xDBFF33) # Set display


def show_gps_stats():
    """ Show GPS coordinates (in decimal degrees), altitude and speed data. """
    global LAST_FIX_DATE
    secs_since_fix = 0 # Seconds since last fix
    text = ""
    gps.update() # Update data from GPS module

    if not gps.has_fix: # If we don't have a fix yet.
        secs_since_fix = int(time.time() - LAST_FIX_DATE)
        text = f"Waiting for fix...\nElapsed: {secs_since_fix} s"
        time.sleep(0.8)

    else:
        LAST_FIX_DATE = time.time()
        # Format and collect display text
        status =  f"Quality: {gps.satellites}/12"
        lat_m = f"{gps.latitude_minutes:07.4f}".replace(".","")
        long_m = f"{gps.longitude_minutes:07.4f}".replace(".","")
        latitude = f"Lat.:  {gps.latitude_degrees}.{lat_m}"
        longitude = f"Long.: {gps.longitude_degrees}.{long_m}"
        altitude = f"Alt.: {gps.altitude_m} m"
        if gps.speed_knots is not None:
            speed = f"Speed: {gps.speed_knots*1.852:.2f} km/h"
        else:
            speed = "Speed: -"
        text = f"{status}\n{latitude}\n{longitude}\n{altitude}\n{speed}"

    set_display(text, 0xFFBD33) # Set display


def set_display(text, color):
    """ Set text onto TFT display. """
    text_area = bitmap_label.Label(terminalio.FONT, text=text,
        scale=2, line_spacing=1.1, color=color)
    text_area.x = 10
    text_area.y = 10
    board.DISPLAY.show(text_area)


if __name__ == '__main__':

    # WELCOME SCREEN
    # Show welcome screen, and allow Feathers to power up properly
    soft_boot.main()

    # PARAMETERS
    BUTT_D0 = True # Screen selector
    BUTT_D1 = False
    BUTT_D2 = False
    SEA_LEVEL_PRESSURE = 1013.25

    # INITIALIZATIONS
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

    # Initialize i2c
    i2c = board.I2C()

    # Initialize battery monitor
    monitor = adafruit_max1704x.MAX17048(i2c)

    # Initialize BMP sensor
    print("Initialize BMP pressure sensor...")
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    print(f"Set sea level pressure to {SEA_LEVEL_PRESSURE} hPa.")
    bmp.sea_level_pressure = SEA_LEVEL_PRESSURE
    # bmp.pressure_oversampling = 8
    # bmp.temperature_oversampling = 2

    # Initialize GPS module
    print("Initialize GPS module...")
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

    if gps.has_fix: # After soft reboot, it is possible to have GPS fix already.
        print("GPS fix OK!")

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


    # Start main loop
    while True:
        check_buttons()
        # Check power-saving:
        if check_screen_ontime_limit(20):
            print("Entering power-saving mode...")

        # Set modes
        if MODE == 0:
            show_gps_stats()

        elif MODE == 1:
            show_atm_stats()

        elif MODE == 2:
            show_system_stats()

        elif MODE == 3:
            show_gps_bmp_stats()
