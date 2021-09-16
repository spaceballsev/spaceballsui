import json
import struct

class CANProcessor:
    def __init__(self, config_path):

        self.config = None

        with open(config_path, 'r') as myfile:
            self.config = json.load(myfile)

    async def handle_message(self, msg):
        #Dont break on a match, a single ID might have multiple messages we're interested in
        for c in self.config:
            if msg.arbitration_id == c['id']:
                #TODO: We should make an explicit registry instead of doing it this way
                value = getattr(self, c['transformer'])(msg, c)

                if c.get("scale") is not None:
                    value = value * c['scale']

                response = {
                    'key': c['key'],
                    'unit': c['unit'],
                    'value': value
                }

                return response

        return None #TODO: is this correct?

    def unpack(self, msg, fmt, msg_config):
        start = msg_config['start']
        length = msg_config['length']
        if length == 16:
            fmt = fmt + 'i'
        elif length == 8:
            fmt = fmt + 'B'

        return struct.unpack_from(fmt, msg.data, int(start/8))[0]

    def little_endian(self, msg, msg_config):
        fmt = '<'
        return self.unpack(msg, fmt, msg_config)


    def big_endian(self, msg, msg_config):
        fmt = '>'
        return self.unpack(msg, fmt, msg_config)

    def value_map(self, msg, msg_config):
        #unpack to one big number
        fmt = '<q'
        value = struct.unpack(fmt, msg.data)[0]

        #mask off the required bytes
        mask = msg_config['length'] << msg_config['start'] - 2
        hex_val = (value & mask) >> msg_config['start'] - 2

        #lookup result
        for k, v in msg_config["map"].items():
            if hex_val == int(k, 16):
                return v
        return "0x" + str(hex_val)
