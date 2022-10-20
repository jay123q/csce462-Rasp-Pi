'''
-------------------------------parseSong.py-----------------------------------------------------------------------------
pip install soundfile
all you need to install! Make sure to change directories in the main. 
I am going to send the wav file inside the folder in the Github, place it in whatever directory you want :)
REFERENCES
https://docs.python.org/3/library/wave.html#module-wave
https://stackoverflow.com/questions/69291258/reading-wav-as-bytes
https://stackoverflow.com/questions/45010682/how-can-i-convert-bytes-object-to-decimal-or-binary-representation-in-python
ROHAN PATH VARIABLES:     
songPath = '/Users/rohanlingala/Downloads/proj462/wav/' + userInput + ".wav"
filePathtoParsedSongs = '/Users/rohanlingala/Downloads/proj462/p_wav/' 
JOSH PATH VARIABLES: 
songPath = '/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/songs/' + userInput + '.wav'
filePathtoParsedSongs = '/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/parsedSong/'
--------------------------------------------------------------------------------------------------------------------------
'''

from playsound import playsound #pip install playsound==1.2.2
import wave
import numpy as np
import soundfile as sf
import io
import struct
import scipy.io as scipy

import bitHelpers

def buttonSong(parsedSong = dict):
    for i in parsedSong:
        playsound(parsedSong[i])


def writeNewSongs(filePathtoParsedSongs, parsedSong, sampleRate):
   # print(parsedSong)
    for i in range(len(parsedSong)):

        fileName = filePathtoParsedSongs + 'songPart'+str(i) + '.wav'
        scipy.wavfile.write(fileName,sampleRate,parsedSong[i])

def parseSongWav(songPath):
    """implementation of the scipy waveform and parsing it """
    sampleRate, data = scipy.wavfile.read(songPath)
    #convert to mono
    if (data.ndim == 2):
        # data has two paramaters a data and a channel, set channel to be 0
        data = data[:,0]
    box = np.array_split(data,8)
    print(type(box), type(sampleRate))

    return box, sampleRate
    #scipy.wavfile.write(data[len(data)/2:])
    


def main():

    userInput = 'drumSounds1'
    # here add a polling system to change the song type & get user input
    # the buttons a - d ( first 4 will instantly change the song type )
    songPath = '/Users/rohanlingala/Documents/GitHub/csce462-Rasp-Pi/project/songs/' + userInput + ".wav"
    filePathtoParsedSongs = '/Users/rohanlingala/Documents/GitHub/csce462-Rasp-Pi/project/parsedSong/' 
    parsedWavs, sampleRate = parseSongWav(songPath)
    writeNewSongs(filePathtoParsedSongs,parsedWavs, 2*sampleRate)


if (__name__ == "__main__"):
    main()