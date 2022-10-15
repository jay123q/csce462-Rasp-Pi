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
import scipy.io.wavfile
from scipy.io.wavfile import write
import bitConversion

def buttonSong(parsedSong = dict):
    for i in parsedSong:
        playsound(parsedSong[i])


def writeNewSongs(filePathtoParsedSongs, parsedSong, nchan, swidth, fr, header):
    '''Rohan: BRAIN EXPANSION!'''

    counter = 0

    for i in parsedSong:

        fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
        arr = np.array(parsedSong[i])
        arr = arr.astype('<U32')
        headerAddPart = np.concatenate((header.astype('<U32'),arr), axis=0)
        headerAddPart = headerAddPart.astype('float32')
        #headerAddPart = convert_bytearray_to_wav_ndarray(headerAddPart)
        mem_buf = io.BytesIO( )
        mem_buf.name = (fileName)
        sf.write( mem_buf, headerAddPart, fr, format='WAV' )
        mem_buf.seek( 0 )
        data, samplerate = sf.read(mem_buf)
        #fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
        p_data = sf.write(fileName, data , samplerate, subtype='PCM_16')
        counter+=1


def parseSong(songPath, parseFileName):

    wf = wave.open(songPath, 'rb')
    nchan = wf.getparams().nframes
    swidth = wf.getparams().sampwidth
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

    return partSongs,nchan,swidth,fr,parsedHeader


def main():
    global nchan
    nchan = 0

    global swidth 
    swidth = 0
    global fr 
    fr = 0

    userInput = 'dl1'
    songPath = '/Users/rohanlingala/Downloads/proj462/wav/' + userInput + ".wav"
    filePathtoParsedSongs = '/Users/rohanlingala/Downloads/proj462/p_wav/' 
    parsedFN = "16bitsnare"

    organizedDict, nchan, swidth, fr,parsedHeader = parseSong(songPath, parsedFN)
    writeNewSongs(filePathtoParsedSongs,organizedDict, nchan, swidth, fr, parsedHeader)


if (__name__ == "__main__"):
    main()