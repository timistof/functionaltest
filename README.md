# functionaltest description

The functional test assumes a timetosser pcb is inserted into the testfixture and is powered on in test-mode by pulling the TEST8 pin low during power-up.
It communicates over serial to the test-mode firmware to program the serial number and receive the results of the internal tests:
- Keyboard: reports switches that are not detected to be pressed
- Led: reports switch number and color channel (r,g,b) of LED's that are detected to be open circuit
- SDRAM: fills ram with pseudo ramdom sequence and verifies it.
- Internal audio sample rates: measures actual frequencies of all possible audio sample rates

After these tests are concluced, the internal firmware switches to audio / midi passthough and becomes a Full-speed USB HID device.
From this point, the test script takes over and performs external stimuli tests:
- USB HID: opens Timetosser as HID device, writes HID packets an verifies if they are echoed back
- MIDI: writes midi messages and verifies if they are echoed back
- Audio: play test tone, store received audio file. Create spectrogram from recording and compare it against reference spectrogram.

# installation

In file /boot/config.txt:
- remove the line "dtparam=audio=on"
- add the line "dtoverlay=hifiberry-dacplusadcpro"

Install dependencies:
- sudo install.sh

Note that python dependencies are installed for python 3 (pip3) and test scripts will
probably only work on python 3.

I had some issues with the HifiBerry hat, could not get input audio to work until I ran 'alsamixer'

# running

First, create a reference spectrogram:
-python3 create_reference_spectrogram.py
This will overwrite reference.png and reference.wav.

Program serial number and run tests with:
-python3 test.py SERIALNUMBER
