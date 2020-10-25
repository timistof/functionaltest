import audiofunctions
import os

def create_reference_spectrogram():
    
    test_tone = 'test-tone.wav'
    reference_wavefile = 'reference.wav'
    reference_spectrogram = 'reference.png'
    
    if not os.path.isfile(reference_wavefile) or not os.path.isfile(reference_spectrogram):
        print('Recording \"' + reference_wavefile + '\"')
        audiofunctions.playrecord(test_tone, reference_wavefile)
        print('Creating spectrogram \"' + reference_spectrogram + '\"')
        audiofunctions.create_spectrogram(reference_wavefile, reference_spectrogram)
        print('Done.')
