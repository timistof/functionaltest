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
        self.received_messages.append(message)

#https://stackoverflow.com/questions/20789412/check-if-all-elements-of-one-array-is-in-another-array
def is_slice_in_list(s,l):
    len_s = len(s) #so we don't recompute length of s on every iteration
    return any(s == l[i:len_s+i] for i in xrange(len(l) - len_s+1))

def midi_test():
    result = False
    device_name = 'USB MIDI Interface:USB MIDI Interface MIDI 1 20:0'
    sleep_time = 0.01 #one midi message every 10 milliseconds

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if device_name not in available_ports:
        print('Could not find \"' + device_name + '\", listing available devices:')
        print(available_ports)
        print()
        print('please edit \"device_name\" variable to a device that is present.')
        exit(1)
        
    messages = []
    for x in range(36, 84): #spanning from two octaves below middle c to two octaves above
        messages.append(noteOn(x))
        messages.append(noteOff(x))

    try:
        midiin, port_name = open_midiinput(device_name)
    except (EOFError):
        print('Could not open midi input \"' + device_name + '\"')
        exit(1)
        
    
    callback = MidiInputHandler(port_name)
    midiin.set_callback(callback)
    midiout.open_port(available_ports.index(device_name))
    
    #clear out any midi messages still in the rx-buffer before sending
    callback.received_messages = []
    
    with midiout:
        for m in messages:
            midiout.send_message(m)
            time.sleep(sleep_time)

    midiin.close_port()
    midiout.close_port()
    del midiin
    del midiout
        
    if messages == callback.received_messages:
        result = True
    else:
        if len(callback.received_messages) > len(messages):
            result = is_slice_in_list(message, callback.received_messages)
        else:
            result = False

    if result == True:
        print("Midi test PASS")
        return True

    print("Midi test FAIL")
    print("Number of sent messages: " + str(len(messages)) + ", number of received messages: " + str(len(callback.received_messages)))
    print("Sent messages:")
    print(messages)
    print("Received messages:")
    print(callback.received_messages)
    return False
        
        
#midi_test()
