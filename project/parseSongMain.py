from random import sample
from playsound import playsound #pip install playsound==1.2.2
import numpy as np
import scipy.io as scipy
import bitHelpers

def writeSong(pathOutput, parsedSong, sampleRate, passState = 0, speedMultiplier = 1.0):
    sampleRate = int(sampleRate*speedMultiplier)
    for i in range(len(parsedSong)):
        fName = pathOutput + str(i+1) + '.wav'
        scipy.wavfile.write(fName, sampleRate, parsedSong[i])
        if (passState == 1):
            bitHelpers.lowPass(fName,sampleRate)
        elif (passState == 2):
            bitHelpers.highPass(fName,sampleRate)

def parseSongWav(songPath):
    sampleRate, data = scipy.wavfile.read(songPath)    
    if (data.ndim == 2):
        data = data[:,0]
    box = np.array_split(data,8)
    return box, sampleRate

def main():

    backToLast = 0
    pathOutput = './parsedSong/'
    #parsedFN = "16bitsnare"

    songPath = "./songs/drumSounds1.wav"

    parsedWavs, sampleRate = parseSongWav(songPath)

    writeSong(pathOutput,parsedWavs, sampleRate,lowFilter,highFilter,speedUpRate,slowDownRate)
    highFilter = 0
    lowFilter = 0
    speedUp = 1
    slowDown = 1
if (__name__ == "__main__"):
    main()