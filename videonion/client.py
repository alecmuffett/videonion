# Copyright (c) Jack Grigg
# See LICENSE for details.

import click
import struct
import subprocess
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import ProcessProtocol

from . import util


class NCSendProtocol(ProcessProtocol):
    def __init__(self, cp):
        self.cp = cp

    def processExited(self, status):
        self.cp.transport.loseConnection()

class CameraProtocol(ProcessProtocol):
    def __init__(self, reactor, addr, port):
        self.reactor = reactor
        self.addr = addr
        self.port = port

    def connectionMade(self):
        click.echo('ffmpeg started')
        sp = NCSendProtocol(self)
        self.nct = self.reactor.spawnProcess(
            sp, 'nc', [
                'nc',
                '-xlocalhost:9050', '-X5',
                self.addr, self.port
            ])

    def outReceived(self, data):
        self.nct.write(data)

    def processEnded(self, status):
        click.echo('ffmpeg stopped')

class NCRecvProtocol(ProcessProtocol):
    def connectionMade(self):
        click.echo('nc started')
        self.mpvp = subprocess.Popen('mpv -', stdin=subprocess.PIPE, shell=True)

    def outReceived(self, data):
        try:
            self.mpvp.stdin.write(data)
        except IOError:
            self.transport.loseConnection()

    def processEnded(self, status):
        click.echo('nc stopped')

@util.wormholeProto()
@inlineCallbacks
def run_client(reactor, w):
    yield w.input_code('Enter code from the server: ')
    yield w.send('ready')
    b_addr = yield w.get()
    b_recv_port = yield w.get()
    b_send_port = yield w.get()
    addr = b_addr.decode('UTF8')
    recv_port = '%d' % struct.unpack('>H', b_recv_port)[0]
    send_port = '%d' % struct.unpack('>H', b_send_port)[0]

    cp = CameraProtocol(reactor, addr, send_port)
    reactor.spawnProcess(cp, 'ffmpeg', util.ffmpeg_args())

    rp = NCRecvProtocol()
    reactor.spawnProcess(
        rp, 'nc', [
            'nc',
            '-xlocalhost:9050', '-X5',
            addr, recv_port
        ])
