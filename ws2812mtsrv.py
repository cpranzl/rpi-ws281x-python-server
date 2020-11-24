#!/usr/bin/env python
# -*- coding: utf-8 -*

import time
import threading
import queue
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from rpi_ws281x import PixelStrip, Color
import argparse

# Server configuration
HOST = 'localhost'
PORT = 8000

# Neopixel configuration
LED_PIN = 18            # GPIO connected to pixels (18 uses PWM!)
LED_FREQ_HZ = 800000    # LED signal frequency in hertz
LED_DMA = 10            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert (whith NPN transistor level shift)
LED_CHANNEL = 0         # Set to '1' for GPIOs 13, 19, 41, 45 or 53

DELAY = 0.02            # 50 Fps

# Configuration of daisychained strips and rings
RING_ONE_LENGTH = 24

# Sum of all LEDs
LED_NUMBER = RING_ONE_LENGTH

# Some calculations for the animations
RING_ONE_START = 0                      # 0
RING_ONE_FIRST = RING_ONE_START + 1     # 1
RING_ONE_HALF = RING_ONE_LENGTH // 2    # 12
RING_ONE_LAST = RING_ONE_LENGTH - 1     # 23

# Some colors
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
TEAL = Color(0, 128, 128)
CYAN = Color(0, 255, 255)
WHITE = Color(255, 255, 255)


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Animation(object):
    """ Animations consist of description, color, value and change """
    def __init__(self, description, color=BLACK, value=0, change=0):
        self.description = description
        self.color = color
        self.value = value
        self.change = change
        print('New request for animation {0} received'.format(description))
        return


# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class RemoteProcedures:
    def addAnimation(self, description, color, value, change):
        script.put(Animation(description, color))
        print('Animation {0} added to script'.format(description))
        return 'ACK'

    def clrAnimations(self):
        with script.mutex:
            script.queue.clear()
        print('Script cleared')
        return 'ACK'

    def chgBrightness(self, value):
        script.put(Animation('chgbrightness', value=value))
        print('Brightness changed to {0}'.format(value))
        return 'ACK'


# Create a class to encapsulate the XMLRPCServer
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localServer = SimpleXMLRPCServer((HOST, PORT),
                                              requestHandler=RequestHandler,
                                              allow_none=True)
        self.localServer.register_introspection_functions()
        self.localServer.register_instance(RemoteProcedures())

    def run(self):
        self.localServer.serve_forever()


def wipe(pixels, color):
    """ Wipe color across strip a pixel at a time """
    print('Wipe the strip with color {0}'.format(color))
    for i in range(LED_NUMBER):
        pixels.setPixelColor(i, color)
        pixels.show()
        time.sleep(DELAY)


def powerup(pixels, color):
    """ Phoniebox powerup """
    print('Powerup sequence with color {0}'.format(color))
    # First LED in ring
    pixels.setPixelColor(RING_ONE_START, color)
    pixels.show()
    time.sleep(DELAY)
    # Rings on both sides simultanously
    ring_one_led = RING_ONE_FIRST
    for i in range((RING_ONE_LAST - RING_ONE_FIRST), 0, -2):
        pixels.setPixelColor((ring_one_led), color)
        pixels.setPixelColor((ring_one_led + i), color)
        pixels.show()
        time.sleep(DELAY)
        ring_one_led = ring_one_led + 1
    # Last LED in ring
    pixels.setPixelColor(RING_ONE_HALF, color)
    pixels.show()
    time.sleep(DELAY)


def powerdown(pixels, color):
    """ Phoniebox powerdown """
    print('Powerdown sequence with color {0}'.format(color))
    # Last LED in ring
    pixels.setPixelColor(RING_ONE_HALF, color)
    pixels.show()
    time.sleep(DELAY)
    # Rings on both sides simultanously
    ring_one_led = RING_ONE_HALF - 1
    for i in range(2, (RING_ONE_LAST + RING_ONE_FIRST), 2):
        pixels.setPixelColor((ring_one_led), color)
        pixels.setPixelColor((ring_one_led + i), color)
        pixels.show()
        time.sleep(DELAY)
        ring_one_led = ring_one_led - 1
    # First LED in ring
    pixels.setPixelColor(RING_ONE_START, color)
    pixels.show()
    time.sleep(DELAY)


def nextsong(pixels, color):
    """ Play next song in playlist """
    print('Next sequence with color {0}'.format(color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def previoussong(pixles, color):
    """ Play previous song in playlist """
    print('Previous sequence with color {0}'.format(color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def chgvolume(pixles, color, value, change):
    """ Volume change """
    print('Volume change from value {0} to {1} sequence with color {2}'
          .format(value, (value + change), color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def chgbrightness(value):
    """ Change brightness of the LEDs """
    print('Brightness change to {0}'.format(value))
    pixels.setBrightness(value)


def carddetected(color):
    """ A card was detected """
    print('Card detected sequence with color {0}'.format(color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def cardremoved(color):
    """ A card was removed """
    print('Card removed sequence with color {0}'.format(color))
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


def accelerate(color):
    """ A pixel is accelerated until all LEDs are filled """
    print("ACCELERATE!")
    for i in range(LED_NUMBER):
        print(i)
        time.sleep(DELAY)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--clear',
                        action='store_true',
                        help='clear the display on exit')
    args = parser.parse_args()

    # Create the queue
    script = queue.Queue()

    # Create server thread and start it
    server = ServerThread()
    server.start()

    # Queue powerup animation
    script.put(Animation('powerup', TEAL))
    script.put(Animation('wipe', BLACK))

    # Create Neopixel object with appropriate configuration
    pixels = PixelStrip(LED_NUMBER,
                        LED_PIN,
                        LED_FREQ_HZ,
                        LED_DMA,
                        LED_INVERT,
                        LED_BRIGHTNESS,
                        LED_CHANNEL)

    # Intialize the library (must be called once before other functions)
    pixels.begin()

    # Clear all pixels
    pixels.clear()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            while not script.empty():
                animation = script.get()
                if animation.description == 'wipe':
                    wipe(pixels, animation.color)
                elif animation.description == 'powerup':
                    powerup(pixels, animation.color)
                elif animation.description == 'powerdown':
                    powerdown(pixels, animation.color)
                elif animation.description == 'chgvolume':
                    chgvolume(pixels,
                              animation.color,
                              animation.value,
                              animation.change)
                elif animation.description == 'chgbrightness':
                    chgbrightness(animation.value)
                else:
                    pass

    except KeyboardInterrupt:
        if args.clear:
            wipe(pixels, BLACK)
