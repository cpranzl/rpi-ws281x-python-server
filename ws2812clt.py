#!/usr/bin/env python
# -*- coding: utf-8 -*

import xmlrpc.client

ws2812srv = xmlrpc.client.ServerProxy('http://localhost:8000')

print(ws2812srv.addAnimation(5, 'powerup'))
print(ws2812srv.addAnimation(5, 'powerup'))
print(ws2812srv.addAnimation(1, 'wipe'))
print(ws2812srv.clrAnimations())
print(ws2812srv.addAnimation(5, 'powerdown'))
