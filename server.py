#!/usr/bin/env python3

import asyncio
from can import notifier
import websockets
import can
import json
import struct
from signal import signal, SIGINT
from sys import exit

def quit(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    loop.stop()
    bus.shutdown()
    bus2.shutdown()
    exit(0)

def little_endian(msg, config):
    start = config['start']
    length = config['length']
    str = '<'
    if length == 16:
        str = str + 'i'

    return struct.unpack_from(str, msg.data, start)[0]

def big_endian(msg, config):
    start = config['start']
    length = config['length']
    str = '>'
    if length == 16:
        str = str + 'i'

    return struct.unpack_from(str, msg.data, start)[0]

def init():  
    #virtual interfaces for development
    global bus
    bus = can.interface.Bus('test', bustype='virtual')

    global bus2
    bus2 = can.interface.Bus('test', bustype='virtual')

    listeners = [
        handleMessage
    ]

    global notifier
    notifier = can.Notifier(bus, listeners, loop=loop)

    with open('config.json', 'r') as myfile:
        data=myfile.read()

    # parse file
    global config
    config = json.loads(data)


async def handleMessage(msg):
    for c in config:
        if (msg.arbitration_id == c['id']):
            value = globals()[c['transformer']](msg, c)
            break
    
    if c['scale']:
        value = value * c['scale']

    response = {
        'key': c['key'],
        'unit': c['unit'],
        'value': value
    }
    print(json.dumps(response))


def mockCanBus():
    msg2 = can.Message(arbitration_id=0x355, data=[0x3C, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0], is_extended_id=False)
    global task 
    task = bus2.send_periodic(msg2, 0.50)

# Create Notifier with an explicit loop to use for scheduling of callbacks
print('Running. Press CTRL-C to exit.')
signal(SIGINT, quit)
global loop
loop = asyncio.get_event_loop()

init()
mockCanBus()

loop.run_forever()
