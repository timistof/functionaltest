#!/bin/sh
nohup /usr/bin/openocd -s /usr/share/openocd/scripts -f ./openocd.cfg &
sleep 1
{ echo "reset"; echo "shutdown"; sleep 1;} | telnet localhost 4444
exit
