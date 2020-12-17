#!/usr/bin/python
from usb.core import find as finddev
dev = finddev(idVendor=0xfc02, idProduct=0x0101)
dev.reset()
