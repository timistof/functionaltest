import audiofunctions
import os

def audio_test(serial_number):
    if not os.path.exists('testresults'):
        os.makedirs('testresults')
    test_tone = 'test-tone.wav'
    recording = 'testresults/' + serial_number + '.wav'
    spectrogram = 'testresults/' + serial_number + '.png'
    reference = 'reference.png'
    
    audiofunctions.playrecord(test_tone, recording)
    audiofunctions.create_spectrogram(recording, spectrogram)
    
    score = audiofunctions.correlate_images(spectrogram, reference)
    if score >= 0.95:
        print('Audio Test PASS')
        return True
    else:
        print('Audio Test FAIL')
        print(score)
        return False
    
#test_audio("2020-00001")
