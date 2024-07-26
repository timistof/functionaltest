#https://answers.opencv.org/question/15842/how-to-find-correlation-coefficient-for-two-images/
from multiprocessing import Process
import os
import time
import cv2
import numpy as np

def record(file):
    os.system('rec -c 2 ' + file + ' trim 1 1 >/dev/null 2>&1')
    #os.system('rec -c 2 ' + file + ' trim 1 1')
    
def play(file):
    os.system('play ' + file + ' >/dev/null 2>&1 gain -2.5') # -2dB to avoid clipping

def playrecord(playfile, recordfile):
    if __name__ == 'audiofunctions':
        recordProcess = Process(target=record, args=(recordfile,))
        playProcess = Process(target=play, args=(playfile,))
        
        recordProcess.start()
        time.sleep(0.5)
        playProcess.start()
        
        recordProcess.join()
        playProcess.join()
        
def create_spectrogram(audiofile, imagefile):
    os.system('sox ' + audiofile + ' -n spectrogram -z 70 -o ' + imagefile)

def correlate_images(fileA, fileB):
    a = cv2.imread(fileA,0)
    b = cv2.imread(fileB,0)
    result = cv2.matchTemplate(a, b, cv2.TM_CCORR_NORMED);
    return result[0,0];
