print("Hello World!")

import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT



# Initialize LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3


def print_gps_data():

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


def rainbow(delay):
    for color_value in range(255):
        pixel[0] = colorwheel(color_value)
        time.sleep(delay)

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

	rainbow(0.02)

        pixel.fill((255, 0, 0))
        time.sleep(0.5)
        pixel.fill((0, 255, 0))
        time.sleep(0.5)
        pixel.fill((0, 0, 255))
        time.sleep(0.5)

        if not button.value:
            BUTTON_PRESSED = True

        else:
            BUTTON_PRESSED = False

        if BUTTON_PRESSED:
            led.value = True
            time.sleep(0.5)
            led.value = False
            time.sleep(0.5)
