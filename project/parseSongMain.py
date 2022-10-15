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
    '''This is'''

    print(parsedSong)

    for i in range(len(parsedSong)):

        fileName = filePathtoParsedSongs + 'songPart'+str(i) + '.wav'
        scipy.wavfile.write(fileName,sampleRate,parsedSong[i])
        ''' parsedSongNumpy = np.array(parsedSong[i])
        parsedSongNumpy = parsedSongNumpy.astype('<U32')
        headerAddPart = np.concatenate((header.astype('<U32'),parsedSongNumpy), axis=0)
        headerAddPart = headerAddPart.astype('float32')
        #headerAddPart = convert_bytearray_to_wav_ndarray(headerAddPart)
        mem_buf = io.BytesIO( ) # we are converting to a mp3 then back to wav
        mem_buf.name = (fileName)
        sf.write( mem_buf, headerAddPart, fr, format='WAV' )
        mem_buf.seek( 0 )
        data, samplerate = sf.read(mem_buf)
        #fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
        p_data = sf.write(fileName, data , samplerate, subtype='PCM_16')'''


def parseSongOLDFAILED(songPath):
    '''THIS IS OUTDATED might make a bin file for it later'''
    wf = wave.open(songPath, 'rb')
    #nchan = wf.getparams().nframes
    #swidth = wf.getparams().sampwidth
    fr = wf.getparams().framerate
    bin_data = wf.readframes(wf.getparams().nframes)

    bd = []
    for my_byte in bin_data:
      bd.append(f'{my_byte:0>8b}')

    countHeaderIndex = 0
    parsedHeader = np.array([])

    for i in range(len(bd)):
        if(countHeaderIndex > 43):
            break
        else:
            countHeaderIndex+=1
            parsedHeader = np.append(parsedHeader,bd[i])

    countPosRemove = 0

    parsingIndex = (len(bd) - 44 ) /8 # 8 buttons
    parsingKeyCount=0
    dictKeyIndex = 0

    partSongs = {0: [],1 : [],2:[],3:[],4:[],5:[],6:[],7:[]}
    for i in range(44,len(bd)):
            if(parsingIndex < parsingKeyCount):
                dictKeyIndex +=1
                parsingKeyCount = 0
            partSongs[dictKeyIndex].append( bd[i])
            parsingKeyCount+=1

    return partSongs,fr,parsedHeader

def parseSongWav(songPath):
    """implementation of the scipy waveform and parsing it """
    sampleRate, data = scipy.wavfile.read(songPath)
    #convert to mono
    if (data.ndim == 2):
        # data has two paramaters a data and a channel, set channel to be 0
        data = data[:,0]
    box = np.array_split(data,8)
    return box, sampleRate

    #scipy.wavfile.write(data[len(data)/2:])
    


def main():

    userInput = 'drumSounds1'
    # here add a polling system to change the song type & get user input
    # the buttons a - d ( first 4 will instantly change the song type )
    songPath = '/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/songs/' + userInput + '.wav'
    filePathtoParsedSongs = '/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/parsedSong/'
    #parsedFN = "16bitsnare"
    parsedWavs, sampleRate = parseSongWav(songPath)
    writeNewSongs(filePathtoParsedSongs,parsedWavs, sampleRate)
    #organizedDict, fr,parsedHeader = parseSongWav(songPath)
    #writeNewSongs(filePathtoParsedSongs,organizedDict, fr, parsedHeader)


if (__name__ == "__main__"):
    main()