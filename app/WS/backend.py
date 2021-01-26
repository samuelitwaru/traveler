# -*- coding: utf-8 -*-

"""
Chat Server
===========

This simple application uses WebSockets to run a primitive chat server.
"""

import os
import gevent
from flask import Flask, render_template
from app import app, sockets, redis
from app.utils import parse_json_string
from .handles import *


class SocketBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(app.config.get("REDIS_CHAN"))

    def __iter_data(self):
        for message in self.pubsub.listen():
            # app.logger.info(type(message))
            data = message.get('data')
            if message['type'] == 'message':
                # app.logger.info(u'Sending message: {}'.format(data))
                yield data.decode()

    def register(self, client):
        """Register a WebSocket connection for Redis updates."""
        self.clients.append(client)

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains Redis subscription in the background."""
        gevent.spawn(self.run)


socket_backend = SocketBackend()


@sockets.route('/ws')
def web_socket(ws):
    socket_backend.register(ws)
    """Receives incoming messages, inserts them into Redis."""
    while not ws.closed:
        # Sleep to prevent *constant* context-switches.
        gevent.sleep(0.1)
        message = ws.receive()

        if message:
            # perform action according to message received i.e handle key
            message = parse_json_string(message)
            handle = message["handle"]
            data = message["data"]
            res = HANDLES[handle](data)
            # app.logger.info(u'Inserting message: {}'.format(message))
            redis.publish(app.config.get("REDIS_CHAN"), res)



