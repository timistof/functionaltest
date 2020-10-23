import audiofunctions
import os

test_tone = 'test-tone.wav'
reference_wavefile = 'reference.wav'
reference_spectrogram = 'reference.png'

print('Recording \"' + reference_wavefile + '\"')
audiofunctions.playrecord(test_tone, reference_wavefile)
print('Creating spectrogram \"' + reference_spectrogram + '\"')
audiofunctions.create_spectrogram(reference_wavefile, reference_spectrogram)
print('Done.')
