# Copyright (c) Jack Grigg
# See LICENSE for details.

from functools import wraps
from twisted.python.runtime import Platform
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

def isUbuntu():
    try:
        with open('/etc/lsb-release', 'r') as f:
            return 'Ubuntu' in f.read()
    except:
        return False

def ffmpeg_args():
    ret = ['ffmpeg', '-f']

    p = Platform()
    if p.isMacOSX():
        ret.append('avfoundation')
    elif p.isLinux():
        ret.append('v4l2')
    else:
        raise NotImplementedError

    ret.extend([
        '-framerate', '30',
        '-video_size', '640x480',
    ])

    if p.isMacOSX():
        ret.extend([
            '-i', 'default',
            '-f', 'avfoundation',
            '-i', ':0',
        ])
    elif p.isLinux():
        ret.extend([
            '-i', '/dev/video0',
            '-f', 'alsa',
            '-thread_queue_size', '99999',
            '-i', 'hw:0',
        ])

    ret.extend([
        '-async', '1',
        '-c:a', 'aac',
        '-vcodec', 'libx264',
        '-tune', 'zerolatency',
        '-preset', 'veryfast',
    ])

    # Ubuntu-only?
    if p.isLinux() and isUbuntu():
        ret.extend(['-strict', '-2'])

    ret.extend([
        '-f', 'mpegts',
        '-'
    ])
    return ret
