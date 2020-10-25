import serial
import testhid
import testmidi
import testaudio
import create_reference_spectrogram
import time
import sys

if len(sys.argv) != 2:
    print('No serial number specified!')
    exit()
    
serialnumber = sys.argv[1]

# first the embedded test is performed:
# - program serial number
# - test keyboard
# - test leds
# - test sdram
# - test all possible audio sample rates
# After this, we perform the rest of the tests
# Look for the following line in serial output to indicate the internal tests have finished:
finishline = 'Tests finished, now starting USB HID device and audio/midi passthrough.'

device = '/dev/ttyUSB0'
baudrate = 115200
ser = serial.Serial(device, baudrate, timeout=10)

#kickstart internal tests by entering serial number
ser.write(bytes(serialnumber + '\n', 'utf-8'))
    
#print out received serial data from test firmware
while True:
    raw = ser.readline() 
    if len(bytearray(raw)) == 0:
        print("ERROR: timeout reading serial data from timetosser, exiting.")
        exit()
    line = raw.decode('utf-8')[:-1]
    print(line)
    if line == finishline:
        break
        
#give timetosser some time to switch to HID USB device mode and start
#midi & audio passthrough
time.sleep(1)

#create reference spectrogram if not available
create_reference_spectrogram.create_reference_spectrogram()

#perform the rest of the tests
testhid.hid_test()
testmidi.midi_test()
#saves test result 'serialnumber.wav' and 'serialnumber.png'
testaudio.audio_test(serialnumber)
