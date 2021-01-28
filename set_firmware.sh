#!/bin/bash
echo $0

if [ "$#" -ne 1 ]; then
    echo "Usage: set_firmware.sh <filename>"
    exit 1
fi

fullfile=$1
filename="${fullfile##*/}"

(cp $1 ./firmwares) > /dev/null
(rm firmware.bin) > /dev/null
(ln -s ./firmwares/$filename firmware.bin) > /dev/null

echo "Target firmware is set to \"./firmwares/${filename}\""
