import audiofunctions

def audio_test(serial_number):
    
    test_tone = 'test-tone.wav'
    recording = 'testresults/' + serial_number + '.wav'
    spectrogram = 'testresults/' + serial_number + '.png'
    reference = 'reference.png'
    
    audiofunctions.playrecord(test_tone, recording)
    audiofunctions.create_spectrogram(recording, spectrogram)
    
    score = audiofunctions.correlate_images(spectrogram, reference)
    if score >= 0.997:
        print('Audio Test PASS')
    else:
        print('Audio Test FAIL')
        print(score)
    
#test_audio("2020-00001")
