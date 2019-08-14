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
from scrollphathd.fonts import font5x5

coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__name__)

class Context(object):
    def __init__(self):
        self.logging_level = logger

pass_context = click.make_pass_decorator(Context, ensure=True)


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

def clock():
    DISPLAY_BAR = False
    BRIGHTNESS = 0.3

    while True:
        scrollphathd.clear()

        float_sec = (time.time() % 60) / 59.0
        seconds_progress = float_sec * 15

        if DISPLAY_BAR:
            for y in range(15):
                current_pixel = min(seconds_progress, 1)
                scrollphathd.set_pixel(y + 1, 6, current_pixel * BRIGHTNESS)
                seconds_progress -= 1
                if seconds_progress <= 0:
                    break

        else:
            scrollphathd.set_pixel(int(seconds_progress), 6, BRIGHTNESS)
        scrollphathd.write_string(
            time.strftime("%H:%M"),
            x=0,                   # Align to the left of the buffer
            y=0,                   # Align to the top of the buffer
            font=font5x5,          # Use the font5x5 font we imported above
            brightness=BRIGHTNESS  # Use our global brightness value
        )
        if int(time.time()) % 2 == 0:
            scrollphathd.clear_rect(8, 0, 1, 5)
        scrollphathd.show()
        time.sleep(0.1)


@click.command()
def cli():
    """TCP Socket"""

    TCP_IP = '0.0.0.0'
    TCP_PORT = 42000
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    logger.debug('Socket open.')
    conn, addr = s.accept()
    logger.info('Connection address: %s', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        logger.info('received data: %s', data)
        if data == 'plasma': plasma()
        if clock == 'clock': clock()
        else: pass
            
    logger.debug('Socket closed.')
    conn.close()

    