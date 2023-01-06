import struct
import time
import os

login = ['192.243.45.237:16768', '127.0.0.1:30000']
image = ['192.243.45.166:21238', ]


class Parser:

    def __init__(self, file):
        self._data = open(file, 'rb')
        self._indexer = Indexer()

        self._packet = None
        self._gen = None
        self._metadata = None

    def next(self):
        if not self._packet:
            if not self._indexer.packet_available():
                # d = os.read(self._data.fileno(), 4096)
                d = self._data.read(4096)
                if d == b'':
                    raise EOFError
                self._indexer.feed(d)

            self._packet = self._indexer.next_packet()
            if not self._packet:
                return None

            self._gen = get_events(self._packet)
            self._metadata = get_metadata(self._packet)

        ev = next(self._gen, None)
        if ev:
            code, = struct.unpack_from('H', ev, 0)
            metadata = self._metadata
            metadata = metadata + [code, len(ev) - 2]
            return (metadata, ev[2:])

        self._packet = None
        self._gen = None
        self._metadata = None
        return None


def get_metadata(data):
    ts, hip, hop, pip, pop, op, = struct.unpack_from('Q4sH4sHB', data, 4)

    peer_ip = []
    for i in pip:
        peer_ip.append(str(i))
    peer = '.'.join(peer_ip) + ':' + str(int(pop))

    type = "Game"
    if str(peer) in login:
        type = "Login"
    elif str(peer) in image:
        type = "Image"
    sender = 'Server'
    if op == 0x01:
        sender = 'Client'

    return [ts, str(peer), str(type), str(sender)]


def get_events(packet):
    data = packet[29:]

    if not is_handshake(packet):
        for moff, mlen in get_moffsets(packet):
            buf = packet[moff + 2:moff + 2 + mlen]
            yield buf


import binascii


def is_handshake(packet):
    seq, = struct.unpack_from('h', packet, 29 + 2)
    return seq == -1


def get_moffsets(packet):
    off = 29 + 6
    end = len(packet) - 4

    while off < end:
        mlen, = struct.unpack_from('H', packet, off)
        yield off, mlen
        off += 2 + mlen


class Indexer:

    def __init__(self):
        self._buffer = bytearray()

    def packet_available(self):
        if len(self._buffer) < 29:
            return False

        plen, = struct.unpack_from('I', self._buffer, 0)
        if len(self._buffer) < plen:
            return False

        return plen

    def _extract_packet(self):
        plen = self.packet_available()
        if not plen:
            return None

        packet = self._buffer[:plen]
        self._buffer = self._buffer[plen:]
        return packet

    def feed(self, data):
        self._buffer += data

    def next_packet(self):
        return self._extract_packet()


if __name__ == '__main__':
    p = Parser('../short.bin')
    while True:
        el = p.next()
        time.sleep(1)
