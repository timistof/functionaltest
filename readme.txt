In file /boot/config.txt:
- remove the line "dtparam=audio=on"
- add the line "dtoverlay=hifiberry-dacplusadcpro"

Install dependencies:
- sudo install.sh

Note that python dependencies are installed for python 3 (pip3) and test scripts will
probably only work on python 3.

First, create a reference spectrogram:
-python3 create_reference_spectrogram.py
This will overwrite reference.png and reference.wav.

Program serial number and run tests with:
-python3 test.py SERIALNUMBER