#!/usr/bin/env python
import os
import sys
import click
import logging
import coloredlogs
import socket
import time
import math
import scrollphathd

coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)

class Context(object):
    def __init__(self):
        self.logging_level = logger

pass_context = click.make_pass_decorator(Context, ensure=True)

@click.command()
def cli():
    """TCP Socket"""

    TCP_IP = '127.0.0.1'
    TCP_PORT = 42000
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print "received data:", data
        if data == 'plasma':
            plasma()
            

    conn.close()

    def plasma():
        i = 0

        while True:
            i += 2
            s = math.sin(i / 50.0) * 2.0 + 6.0

            for x in range(0, 17):
                for y in range(0, 7):
                    v = 0.3 + (0.3 * math.sin((x * s) + i / 4.0) * math.cos((y * s) + i / 4.0))

                    scrollphathd.pixel(x, y, v)

            time.sleep(0.01)
            scrollphathd.show()