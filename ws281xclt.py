#!/usr/bin/env python3
# -*- coding: utf-8 -*

import xmlrpc.client

ws281xsrv = xmlrpc.client.ServerProxy('http://localhost:8000')

print(ws281xsrv.powerup())
print(ws281xsrv.powerdown())
