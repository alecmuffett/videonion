#!/bin/sh

tor=/Applications/TorBrowser.app/Contents/MacOS/Tor/tor.real # HACK THIS?

root=`dirname $0`

cd $root

root=`pwd`

hs=hsvideo

dir=$root/$hs.d

test -d $dir || mkdir $dir || exit 1

chmod 700 $dir

(
    echo DataDirectory $dir

    echo HiddenServiceDir $dir

    echo ControlPort unix:$dir/control.sock

    echo SocksPort 0 # disable SOCKS

    echo Log info file $dir/log.txt

    echo SafeLogging 0 # noisy logging

    echo HeartbeatPeriod 60 minutes

    for port in 1337 1338 1339
    do
        echo HiddenServicePort $port localhost:$port
    done

) > $dir/config

$tor --hush -f $dir/config
