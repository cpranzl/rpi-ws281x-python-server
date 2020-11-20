#!/usr/bin/env python
# -*- coding: utf-8 -*

import time
import threading
import queue
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New job: {0}'.format(description))
        return

    def __cmp__(self, other):
        return (self.priority > other.priority) - \
               (self.priority < other.priority)


# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class RemoteProcedures:
    def mul(self, x, y):
        job_queue.put(Job(3, 'Mid-level job'))
        return x * y

    def add(self, x, y):
        job_queue.put(Job(10, 'Low-level job'))
        return x + y

    def pow(self, x, y):
        job_queue.put(Job(1, 'High-level job'))
        return x ** y


# Create a class to encapsulate the XMLRPCServer
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localServer = SimpleXMLRPCServer(('localhost', 8000),
                                              requestHandler=RequestHandler)
        self.localServer.register_introspection_functions()
        self.localServer.register_instance(RemoteProcedures())

    def run(self):
        self.localServer.serve_forever()


# Create the queue
job_queue = queue.PriorityQueue()

# Create server thread and start it
server = ServerThread()
server.start()

while True:
    print('Main thread')
    while not job_queue.empty():
        next_job = job_queue.get()
        print('Processing job: {0}'.format(next_job.description))
    time.sleep(5)
