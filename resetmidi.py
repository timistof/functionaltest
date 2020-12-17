#!/usr/bin/python
from usb.core import find as finddev
dev = finddev(idVendor=0x fc02, idProduct=0x0101)
dev.reset()