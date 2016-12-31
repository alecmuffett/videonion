# Copyright (c) Jack Grigg
# See LICENSE for details.

import click
from twisted.internet import reactor

APP_NAME = 'videonion'


@click.group()
def videonion():
    pass

@videonion.command()
@click.option('--send_port', default=9091,
              help='port we send video on')
@click.option('--recv_port', default=9090,
              help='port we receive video on')
@click.argument('address')
def start(send_port, recv_port, address):
    from server import run_server
    d = run_server(reactor, address, send_port, recv_port)
    reactor.run()

@videonion.command()
def join():
    from client import run_client
    d = run_client(reactor)
    reactor.run()
