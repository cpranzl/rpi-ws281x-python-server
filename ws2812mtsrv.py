#!/usr/bin/env python
# -*- coding: utf-8 -*

import time
import threading
import queue
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import argparse

RING_LENGTH = 24
LED_COUNT = RING_LENGTH

DELAY = 0.05


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Animation(object):
    """ Animations consist of priority and description """
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New Animation: {0}'.format(description))
        return


# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class RemoteProcedures:
    def addAnimation(self, priority, description):
        animations.put(Animation(priority, description))
        print('Animation {0} with priority {1} added to queue'.format(description, priority))
        return 'OK'

    def clrAnimations(self):
        with animations.mutex:
            animations.queue.clear()
        print('Animation queue cleared')


# Create a class to encapsulate the XMLRPCServer
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localServer = SimpleXMLRPCServer(('localhost', 8000),
                                              requestHandler=RequestHandler,
                                              allow_none=True)
        self.localServer.register_introspection_functions()
        self.localServer.register_instance(RemoteProcedures())

    def run(self):
        self.localServer.serve_forever()


def wipe(color):
    """ Wipe color across strip a pixel at a time """
    print('Wipe the strip with color {0}'.format(color))
    for i in range(LED_COUNT):
        print(i)
        time.sleep(DELAY)


def powerup(color):
    """ Phoniebox powerup """
    print('Powerup sequence with color {0}'.format(color))
    for i in range(LED_COUNT):
        print(i)
        time.sleep(DELAY)


def powerdown(color):
    """ Phoniebox powerdown """
    print('Powerdown sequence with color {0}'.format(color))
    for i in range(LED_COUNT):
        print(i)
        time.sleep(DELAY)

def nextsong(color):
    """ Play next song in playlist """
    print('Next sequence with color {0}'.format(color))
    for i in range(LED_COUNT):
        print(i)
        time.sleep(DELAY)

def previoussong(color):
    """ Play previous song in playlist """
    print('Previous sequence with color {0}'.format(color))
    for i in range(LED_COUNT):
        print(i)
        time.sleep(DELAY)

def chgvolume (volume, change, color):
    """ Volume change """
    print('Volume change sequence with color {0}'.format(color))
    for i in range(LED_COUNT):
        print(i)
        time.sleep(DELAY)

def carddetected(color):
    """ A card was detected """
    print('Card detected sequence with color {0}'.format(color))
    for i in range(LED_COUNT):
        print(i)
        time.sleep(DELAY)

def cardremoved(color):
    """ A card was removed """
    print('Card removed sequence with color {0}'.format(color))
    for i in range(LED_COUNT):
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
    animations = queue.Queue()

    # Create server thread and start it
    server = ServerThread()
    server.start()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print('Main thread')
            while not animations.empty():
                animation = animations.get()
                if animation.description == 'wipe':
                    wipe('BLACK')
                elif animation.description == 'powerup':
                    powerup('AQUA')
                elif animation.description == 'powerdown':
                    powerdown('BLACK')
                else:
                    pass
            time.sleep(5)

    except KeyboardInterrupt:
        if args.clear:
            wipe('BLACK')
