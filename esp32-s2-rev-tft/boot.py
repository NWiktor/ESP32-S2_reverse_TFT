""" This module contains functions for booting (runs only when hard reset occurs). """

# pylint: disable = import-error
import time
from secrets import secrets
import ssl
import socketpool
import rtc
import wifi
import adafruit_requests


def init_gps():
    """  """
    # print("Init GPS")
    pass


def set_rtc():
    """ Reads current time from WorldTimeAPI and sets the RTC accordingly. """

    SET_TIME = False

    try:
        time.sleep(0.5)
        print("Connecting to WorldTimeAPI...")
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        print("Connected, getting WorldTimeAPI time...")
        pool = socketpool.SocketPool(wifi.radio)
        request = adafruit_requests.Session(pool, ssl.create_default_context())

        print("Getting current time...")
        response = request.get("http://worldtimeapi.org/api/ip")
        time_data = response.json()
        unixtime = (int(time_data['unixtime']) + int(time_data['raw_offset'])
            + int(time_data["dst_offset"]))
        print("URL time: ", response.headers['date'])

        # Create time struct and set RTC with it
        rtc.RTC().datetime = time.localtime(unixtime)

    except adafruit_requests.OutOfRetries:
        print("OutOfRetries Exception occured! RTC unchanged!")
        print("Please try hard reset!")
        time.sleep(2)


if __name__ == '__main__':
    set_rtc()
    # init_gps()
