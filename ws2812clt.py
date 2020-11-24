#!/usr/bin/env python
# -*- coding: utf-8 -*

import xmlrpc.client
from rpi_ws281x import Color

BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
TEAL = Color(0, 128, 128)
CYAN = Color(0, 255, 255)
WHITE = Color(255, 255, 255)

ws2812srv = xmlrpc.client.ServerProxy('http://localhost:8000')

print(ws2812srv.chgBrightness(25))
print(ws2812srv.addAnimation('powerup', CYAN, 0, 0))
print(ws2812srv.addAnimation('powerdown', BLACK, 0, 0))
print(ws2812srv.chgBrightness(100))
print(ws2812srv.addAnimation('powerup', CYAN, 0, 0))
print(ws2812srv.addAnimation('powerdown', BLACK, 0, 0))

# print(ws2812srv.addAnimation('powerup', CYAN))
# print(ws2812srv.addAnimation('powerup', CYAN))
# print(ws2812srv.addAnimation('wipe', BLACK))
# print(ws2812srv.clrAnimations())
# print(ws2812srv.addAnimation('powerdown', BLACK))
# print(ws2812srv.addAnimation('chgvolume', GREEN, 25, 25))
# print(ws2812srv.addAnimation('chgvolume', GREEN, 50, -60))
