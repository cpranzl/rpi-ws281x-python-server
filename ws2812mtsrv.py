#!/usr/bin/env python
# -*- coding: utf-8 -*

import time
import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'mul').
class RemoteProcedures:
    def mul(self, x, y):
        return x * y

    def add(self, x, y):
        return x + y


# Create a class to encapsulate the XMLRPCServer
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localServer = SimpleXMLRPCServer(('localhost', 8000),
                                              requestHandler=RequestHandler)
        self.localServer.register_introspection_functions()
        self.localServer.register_function(pow)
        self.localServer.register_instance(RemoteProcedures())

    def run(self):
        self.localServer.serve_forever()


# Create server thread and start it
server = ServerThread()
server.start()

while True:
    print("Main thread")
    time.sleep(5)
