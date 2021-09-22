#!/usr/bin/env python3
import os
from sys import exit
import json
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
        self.config_path = config_path
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

    def mockCanBus(self):
        """
        Create some test messages. TODO: MOve this to a proper unit test.
        """
        self.bus2 = can.interface.Bus('can0', bustype='virtual')
        bus_dir = os.path.join(os.path.dirname(self.config_path), '..', 'busses', 'dev.json')

        with open(bus_dir, 'r') as f:
            bus_data = json.load(f)
        for bus in bus_data['busses']:
            msg = can.Message(
                arbitration_id=int(bus['arbitration_id'], 16),
                data=[int(i, 16) for i in bus['data']],
                is_extended_id=False)
            self.tasks.append(self.bus2.send_periodic(msg, 0.50))
