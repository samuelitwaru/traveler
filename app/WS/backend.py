# -*- coding: utf-8 -*-

"""
Chat Server
===========

This simple application uses WebSockets to run a primitive chat server.
"""

import logging
import gevent
from flask import Flask, render_template
from app import app, sockets
from app.utils import parse_json_string
from .handles import *


def send(client, message):
    client.ws.send(message)

@sockets.route('/submit')
def inbox(ws):
    """Receives incoming messages, inserts them into Redis."""
    while not ws.closed:
        # Sleep to prevent *constant* context-switches.
        # gevent.sleep(0.1)
        message = ws.receive()

        if message:
            # perform action according to message received i.e handle key
            message = parse_json_string(message)
            print(">>>>>>>>>>>>>>>>>>>", message)
            handle = message["handle"]
            data = message["data"]
            res = HANDLES[handle](data)
            clients = ws.handler.server.clients.values()
            for client in clients:
                gevent.spawn(send, client, res)
            # app.logger.info(u'Inserting message: {}'.format(message))
            # redis.publish(REDIS_CHAN, res)

@sockets.route('/receive')
def outbox(ws):
    """Sends outgoing messages, via `ChatBackend`."""
    # socket_backend.register(ws)

    while not ws.closed:
        # Context switch while `ChatBackend.start` is running in the background.
        gevent.sleep(0.1)



