# Copyright (c) Jack Grigg
# See LICENSE for details.

import click
import struct
import subprocess
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import (
    ProcessProtocol,
    Protocol,
    ServerFactory,
)

from . import util


class CameraProtocol(ProcessProtocol):
    def __init__(self, sp):
        self.sp = sp

    def outReceived(self, data):
        self.sp.transport.write(data)

class SendProtocol(Protocol):
    def connectionMade(self):
        click.echo('recipient connected')
        cp = CameraProtocol(self)
        self.cpt = self.factory.reactor.spawnProcess(cp, 'ffmpeg', util.ffmpeg_args())

    def connectionLost(self, reason):
        self.cpt.loseConnection()
        self.factory.client_disconnected()

class RecvProtocol(Protocol):
    def connectionMade(self):
        click.echo('sender connected')
        self.mpvp = subprocess.Popen('mpv -', stdin=subprocess.PIPE, shell=True)

    def dataReceived(self, data):
        try:
            self.mpvp.stdin.write(data)
        except IOError:
            self.transport.loseConnection()

class SendFactory(ServerFactory):
    protocol = SendProtocol

    def __init__(self, reactor, *args):
        self.reactor = reactor
        self.args = args

    def client_disconnected(self):
        self.reactor.callLater(1, get_client, self.reactor, *self.args)

class RecvFactory(ServerFactory):
    protocol = RecvProtocol

@inlineCallbacks
def run_server(reactor, addr, send_port, recv_port):
    sep = serverFromString(reactor, 'tcp:%d' % send_port)
    sep.listen(SendFactory(reactor, addr, send_port, recv_port))

    rep = serverFromString(reactor, 'tcp:%d' % recv_port)
    rep.listen(RecvFactory())

    yield get_client(reactor, addr, send_port, recv_port)

@util.wormholeProto()
@inlineCallbacks
def get_client(_, w, addr, send_port, recv_port):
    code = yield w.get_code()
    click.echo('Give this code to the client: %s' % code)
    yield w.get()
    yield w.send(addr.encode('UTF8'))
    yield w.send(struct.pack('>H', send_port))
    yield w.send(struct.pack('>H', recv_port))
