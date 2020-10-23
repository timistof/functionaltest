import time
import rtmidi
from rtmidi.midiutil import open_midiinput
        
def noteOn(note):
    return [0x90, note, 127] #note on, channel 1, "note", velocity 127
def noteOff(note):
    return [0x80, note, 0] # note off, channel 1, "note", velocity 0

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self.received_messages = []

    def __call__(self, event, data=None):
        message, deltatime = event
        print("Received message")
        self.received_messages.append(message)

def midi_test():
    device_name = 'USB MIDI Interface:USB MIDI Interface MIDI 1 20:0'
    sleep_time = 0.01 #one midi message every 10 milliseconds

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if device_name not in available_ports:
        print('Could not find \"' + device_name + '\", listing available devices:')
        print(available_ports)
        print()
        print('please edit \"device_name\" variable to a device that is present.')
        exit()
        
    messages = []
    for x in range(36, 84): #spanning from two octaves below middle c to two octaves above
        messages.append(noteOn(x))
        messages.append(noteOff(x))

    try:
        midiin, port_name = open_midiinput(device_name)
    except (EOFError):
        print('Could not open midi input \"' + device_name + '\"')
        exit()
        
    
    callback = MidiInputHandler(port_name)
    midiin.set_callback(callback)

    midiout.open_port(available_ports.index(device_name))
    with midiout:
        for m in messages:
            midiout.send_message(m)
            time.sleep(sleep_time)

    midiin.close_port()
    midiout.close_port()
    del midiin
    del midiout
        
    if messages == callback.received_messages:
        print("Midi test PASS")
    else:
        print("Midi test FAIL")
        print(callback.received_messages)
        
#midi_test()
