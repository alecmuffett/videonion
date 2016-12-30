## Sending side

### OS X

```
ffmpeg -f avfoundation -framerate 30 -video_size 848x480 -i "default" -f avfoundation -i ":0" -async 1 -c:a aac -vcodec libx264 -tune zerolatency -preset ultrafast -f mpegts - | \
  nc -xlocalhost:9050 -X5 xxxxxxxxxxxxxxxx.onion 9090
```

### Linux

```
ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i "/dev/video0" -f alsa -thread_queue_size 99999 -i hw:0 -async 1 -c:a aac -vcodec libx264 -tune zerolatency -preset ultrafast -f mpegts - | \
  nc -xlocalhost:9050 -X5 xxxxxxxxxxxxxxxx.onion 9090
```

## Receiving side

Setup a .onion service, direct port 9090 to 127.0.0.1

```
socat TCP-LISTEN:9090,reuseaddr,fork EXEC:"ffplay -"
```
