#!/bin/sh
if [ -z "$1" ]
then 
    echo "firmware path not specified.";
else
    /usr/bin/openocd -s /usr/share/openocd/scripts -f ./openocd.cfg -c "program $1 verify reset exit 0x08000000"
fi
