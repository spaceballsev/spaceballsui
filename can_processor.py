import json
import json
import struct

def init():
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
    
    return response

def little_endian(msg, config):
    start = config['start']
    length = config['length']
    str = '<'
    if length == 16:
        str = str + 'i'
    elif length == 8:
        str = str + 'B'

    return struct.unpack_from(str, msg.data, int(start/8))[0]

def big_endian(msg, config):
    start = config['start']
    length = config['length']
    str = '>'
    if length == 16:
        str = str + 'i'

    return struct.unpack_from(str, msg.data, start)[0]