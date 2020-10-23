import hid #https://github.com/apmorton/pyhidapi/blob/master/hid/__init__.py
import random

vid = 0x16D0    # MCS
pid = 0x0FA5    # Timetosser
      
def hid_test():
    result = True
    
    # first byte is report id 3 to indicate big packet.
    # This packet would normally be 64 bytes, but for some bug in ST's usb code it won't receive it unless we send
    # something smaller first...
    # So we test with a packet of 56 bytes.
    bigReport =  [3,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0,
                  0,0,0,0,0,0,0,0]

    # fill bigreport (except for report Id) with random bytes
    for i in range(1, len(bigReport)):
        bigReport[i] = random.randint(0, 255)
    
    result = True
    try:
        with hid.Device(vid, pid) as h:
            outpacket = bytes(bigReport)
            
            # we perform the test twice, because first received HID packet is corrupt because of ST firmware (grr)
            h.write(outpacket)
            inpacket = h.read(64, 100) # read maximum of 64 bytes, 100 ms timeout
            
            h.write(outpacket)
            inpacket = h.read(64, 100) # read maximum of 64 bytes, 100 ms timeout
            
            if len(bytearray(inpacket)) == 0:
                print("HID Test failed: timeout while reading device. FAIL")
                result = False;
                
            elif outpacket != inpacket:
                print("HID Test failed, packets are not equal. FAIL")
                print("Sent:")
                print(outpacket)
                print("Received:")
                print(inpacket)
                result = False
    except:
        print("HID Test failed, could not open device. FAIL")
        result = False
    
    if result == True:
        print("HID Test PASS")

#test HID functionality of timetosser in usb-application mode (not in test-mode)
#read key state and send led state
def hid_application(vid, pid):
    # packet sent for led state (not available during test firmware), 1st byte is report Id (1)
    ledReport = [1, 
                 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0,
                 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0,
                 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0,
                 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0, 0, 0xff, 0, #16 x 3 bytes for rgb led color
                 0, 0] # plus 2 bytes for "on" state, 51 bytes total
    outPacket = bytearray(ledReport)
    
    with hid.Device(vid, pid) as h:
        while(True):
           receivedBytes = h.read(64, 100) # read 64 bytes max, 100 ms timeout
           if len(bytearray(receivedBytes)) == 3 and receivedBytes[0] == 1: # check size and report id
               
               #print key state
               print('********')
               printKeyRow(receivedBytes[2])
               printKeyRow(receivedBytes[1])
               
               #set key state in led state
               outPacket[49] = receivedBytes[1]
               outPacket[50] = receivedBytes[2]
               try:
                   h.write(bytes(outPacket))
               except Exception as e:
                   print(outPacket)
                   pass

def printKeyRow(byte):
    keys = ''
    for i in range(8):
        if byte & (1 << i):
            keys += '1'
        else:
            keys += '0'
    print(keys)
    
def printDevices():
    print(hid.enumerate())

def printDevice(vid, pid):
    with hid.Device(vid, pid) as h:
        print(f'Device manufacturer: {h.manufacturer}')
        print(f'Product: {h.product}')
        print(f'Serial Number: {h.serial}')
        
#functional test: during test-firmware, timetosser enumerates as full-speed (12MBit) device
#it should echo back what you send to it, test if this works
#hid_test(vid, pid)

#when timetosser is not in testmode: read keystate and send back led data
#hid_application(vid, pid)

#print(hid.enumerate())
#printDevice(vid, pid)
