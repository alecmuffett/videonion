# Copyright (c) Jack Grigg
# See LICENSE for details.

from functools import wraps
from wormhole.cli.public_relay import RENDEZVOUS_RELAY
from wormhole.wormhole import wormhole

APPID = u'str4d.xyz/videonion'


def wormholeProto(relay=RENDEZVOUS_RELAY):
    def _decorator(proto):
        @wraps(proto)
        def _wormhole(reactor, *argv):
            w = wormhole(APPID, relay, reactor)
            d = proto(reactor, w, *argv)
            d.addBoth(w.close)
            return d
        return _wormhole
    return _decorator

def ffmpeg_args():
    return [
        'ffmpeg',
        '-f', 'v4l2',
        '-framerate', '30',
        '-video_size', '640x480',
        '-i', '/dev/video0',
        '-f', 'alsa',
        '-thread_queue_size', '99999',
        '-i', 'hw:0',
        '-async', '1',
        '-c:a', 'aac',
        '-vcodec', 'libx264',
        '-tune', 'zerolatency',
        '-preset', 'veryfast',
        '-strict',
        '-2',
        '-f', 'mpegts',
        '-'
    ]
