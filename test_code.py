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
