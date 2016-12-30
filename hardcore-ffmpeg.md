## Client side

### Sending

#### OS X

```
ffmpeg -f avfoundation -framerate 30 -video_size 848x480 -i "default" -f avfoundation -i ":0" -async 1 -c:a aac -vcodec libx264 -tune zerolatency -preset ultrafast -f mpegts - | \
  nc -xlocalhost:9050 -X5 xxxxxxxxxxxxxxxx.onion 9090
```

#### Linux

```
ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i "/dev/video0" -f alsa -thread_queue_size 99999 -i hw:0 -async 1 -c:a aac -vcodec libx264 -tune zerolatency -preset ultrafast -f mpegts - | \
  nc -xlocalhost:9050 -X5 xxxxxxxxxxxxxxxx.onion 9090
```

Ubuntu: add `-strict -2` before `-f mpegts`

### Receiving

```
nc -xlocalhost:9050 -X5 xxxxxxxxxxxxxxxx.onion 9091 | mpv -
```

## Server side

Setup a .onion service, direct port 9090 and 9091 to 127.0.0.1

### Sending

#### OS X

```
socat TCP-LISTEN:9091,reuseaddr,fork EXEC:'ffmpeg -f avfoundation -framerate 30 -video_size 848x480 -i "default" -f avfoundation -i ":0" -async 1 "-c:a" aac -vcodec libx264 -tune zerolatency -preset ultrafast -f mpegts -'
```

#### Linux

```
socat TCP-LISTEN:9091,reuseaddr,fork EXEC:'ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i "/dev/video0" -f alsa -thread_queue_size 99999 -i "hw:0" -async 1 "-c:a" aac -vcodec libx264 -tune zerolatency -preset ultrafast -f mpegts -'
```

Ubuntu: add `-strict -2` before `-f mpegts`

### Receiving

```
socat TCP-LISTEN:9090,reuseaddr,fork EXEC:"mpv -"
```

## TODO

* Stop the stdout from backfeeding
