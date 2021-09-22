#!/usr/bin/env python3
from sys import exit
from signal import signal, SIGINT

import asyncio
import can
from spaceballs_ws_server.ws_data_server import WebSocketDataServer


class CANServer:

    def quit(self, signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        self.loop.stop()
        self.bus.shutdown()

        for t in self.tasks:
            t.stop()

        exit(0)

    def __init__(self, config_path, bustype="socketcan_native"):
        """
            Initialise the bus interface, reader, listeners and web socket server
            args:
                config_path (filepath): A path to a json file specifying the config (see examples)
                bystype (str): 'socketcan_native' or 'virtual'. Defaults to socketcan_native
            returns:
                None
        """
        #virtual interfaces for development
        self.bus = can.interface.Bus('can0', bustype=bustype)

        self.reader = can.AsyncBufferedReader()

        self.listeners = [
            self.reader
        ]

        self.tasks = [] # stores messges being sent

        self.loop = asyncio.get_event_loop()

        self.notifier = can.Notifier(self.bus, self.listeners, loop=self.loop)

        self.web_socket_server = WebSocketDataServer(config_path, self.reader, self.loop)

    def run(self):
        """
        Run the server
        """
        self.loop.run_until_complete(self.web_socket_server.run())
        self.loop.run_forever()
