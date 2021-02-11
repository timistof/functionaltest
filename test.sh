#!/bin/bash

firmware="firmware.bin"

promptclose() {
echo "- Properly place PCB in fixture and make sure PCB switch is in \"on\" position."
echo "- Close fixture and click scanner button to continue."
read -p "" response
    while [[ ! -z "$response" ]]
    do
    echo "Please press button only."
    read -p "" response
    done
}

running() {
echo " _______  _____  _____  ____  _____  ____  _____  _____  ____  _____   ______"
echo "|_   __ \|_   _||_   _||_   \|_   _||_   \|_   _||_   _||_   \|_   _|.' ___  |"
echo "  | |__) | | |    | |    |   \ | |    |   \ | |    | |    |   \ | | / .'   \_|"
echo "  |  __ /  | '    ' |    | |\ \| |    | |\ \| |    | |    | |\ \| | | |   ____"
echo " _| |  \ \_ \ \__/ /    _| |_\   |_  _| |_\   |_  _| |_  _| |_\   |_\ \`.___]  |"
echo "|____| |___| \`.__.'    |_____|\____||_____|\____||_____||_____|\____|\`._____.'"
}

pass() {
echo " _______         _          ______       ______       _"
echo "|_   __ \       / \       .' ____ \    .' ____ \     | |"
echo "  | |__) |     / _ \      | (___ \_|   | (___ \_|    | |"
echo "  |  ___/     / ___ \      _.____\`.     _.____\`.     | |"
echo " _| |_      _/ /   \ \_   | \____) |   | \____) |    |_|"
echo "|_____|    |____| |____|   \______.'    \______.'    (_)"
}
fail() {
echo " ________        _         _____     _____        _"
echo "|_   __  |      / \       |_   _|   |_   _|      | |"
echo "  | |_ \_|     / _ \        | |       | |        | |"
echo "  |  _|       / ___ \       | |       | |   _    | |"
echo " _| |_      _/ /   \ \_    _| |_     _| |__/ |   |_|"
echo "|_____|    |____| |____|  |_____|   |________|   (_)"
}
error() {
echo " ________  _______     _______      ___   _______     _"
echo "|_   __  ||_   __ \   |_   __ \   .'   \`.|_   __ \   | |"
echo "  | |_ \_|  | |__) |    | |__) | /  .-.  \ | |__) |  | |"
echo "  |  _| _   |  __ /     |  __ /  | |   | | |  __ /   | |"
echo " _| |__/ | _| |  \ \_  _| |  \ \_\  \`-'  /_| |  \ \_ |_|"
echo "|________||____| |___||____| |___|\`.___.'|____| |___|(_)"
}


#running
#pass
#fail
#error

clear
echo
echo "Welcome to the Timetosser functional test rig! How are you today?"
echo

scantext_newpcb="Please scan QR-code of next PCB."
scantext_retry_flash="Flashing failed, open fixture and re-scan QR-code to retry."
scantext=$scantext_newpcb

while true
do
echo "****************************************************************************"
echo
echo $scantext
read -p "" serial
clear
echo "Serial number is \"$serial\"";
promptclose

clear
running
echo
real_fimware_name=`readlink -f $firmware`
echo "Flashing $real_fimware_name..."

flash_output="./testresults/${serial}_flash.txt"
./flash.sh $firmware &>> $flash_output
if [ ! $? -eq 0 ]; then
    clear
    cat ${flash_output}
    echo
    error
    echo
    scantext=$scantext_retry_flash
    continue
fi

echo "Are all leds white? press enter to continue or scan a QR code to start over"
read -p "" response
if [[ -z "$response" ]]; then
    continue
fi

echo "Programing serial number \"$serial\" and running tests..."
test_output="./testresults/${serial}_test.txt"
(python3 ./test.py ${serial}) &>> ${test_output}
test_result=$?

#pass
if [ $test_result -eq 0 ]; then
    clear
    pass
    echo
    scantext=$scantext_newpcb
        
# test fail
elif [ $test_result -eq 2 ]; then
    clear
    cat ${test_output}
    echo
    fail
    echo
    scantext=scantext_newpcb
    
# no serial
elif [ $test_result -eq 3 ]; then
    clear
    cat ${test_output}
    echo
    error
    echo
    scantext="Incorrect serial specified, open fixture and re-scan QR-code to retry."

# timeout
elif [ $test_result -eq 4 ]; then
    clear
    cat ${test_output}
    echo
    error
    echo
    scantext="Timeout getting response from PCB, open fixture and re-scan QR-code to retry."
    
#non-recoverable error
else
    clear
    cat ${test_output}
    echo
    error
    echo
    echo "Something is wrong with the fixture, please reboot raspberry pi."
    exit 1
fi
done
