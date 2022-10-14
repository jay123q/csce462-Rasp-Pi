
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

def write_header(_bytes, _nchannels, _sampwidth, _framerate):
    WAVE_FORMAT_PCM = 0x0001
    initlength = len(_bytes)
    bytes_to_add = b'RIFF'
    #print(_nchannels, _sampwidth, _framerate)
    _nframes = initlength // (_nchannels * _sampwidth)
    _datalength = _nframes * _nchannels * _sampwidth

    bytes_to_add += struct.pack('<L4s4sLHHLLHH4s',
        36 + _datalength, b'WAVE', b'fmt ', 16,
        WAVE_FORMAT_PCM, _nchannels, _framerate,
        _nchannels * _framerate * _sampwidth,
        _nchannels * _sampwidth,
        _sampwidth * 8, b'data')

    bytes_to_add += struct.pack('<L', _datalength)

    return bytes_to_add + _bytes

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

def buttonSong(parsedSong = dict):
    """Josh: In this final design this will  be a interupt method that allows us to assign the press to 8 gpio pins drive 3 volts and the button press triggers a input
    IN ALHPA it will be a simple player"""
    # first create the new wav
    for i in parsedSong:
        playsound(parsedSong[i])


def writeNewSongs(filePathtoParsedSongs, parsedSong, nchan, swidth, fr, header):
    '''Rohan: BRAIN EXPANSION!'''

    counter = 0
    fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
    arr = np.array(parsedSong[0])
    arr = arr.astype('int32')
    headerAddPart = np.concatenate((header.astype('int32'),arr), axis=0)
    headerAddPart = headerAddPart.astype('int32')
    mem_buf = io.BytesIO( )
    mem_buf.name = (fileName)
    sf.write( mem_buf, headerAddPart, fr, format='WAV' )
    mem_buf.seek( 0 )
    data, samplerate = sf.read(mem_buf)

    for i in parsedSong:
        
        fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
        p_data = sf.write(fileName, data , samplerate, subtype='PCM_16')
        counter+=1
        

def parseSong(songPath, parseFileName):
    
    '''Rohan: create string that is the directory of new file, we create the path first
    and then create the wav file that belongs in that path in line 24. The reason 
    we do is because we need to create a new wav file that has 16 bit format, and we 
    need to make sure it is 16 bit by creating a new file we can use.'''

    """Josh: simplifying this to be a more clean function"""
    
    wf = wave.open('snare.wav', 'rb')
    
    nchan = wf.getparams().nframes
    swidth = wf.getparams().sampwidth
    fr = wf.getparams().framerate
    bin_data = wf.readframes(wf.getparams().nframes)
    
    '''Rohan: open the filepath with the newly constructed wave file to read bytes. 
    Inside bin_data, i am using getparams() which returns a tuple, inside that 
    tuple I can call nframes as a thing inside the tuple to give me the number
    of audio frames inside the new file, and then i use readframes() to return
    the audio frames as a byte object. this will spit out a huge array of hex
    values. '''
    bd = []
    for my_byte in bin_data:
      bd.append(f'{my_byte:0>8b}')
      '''Josh:
      The code below divides the song into 8 indexes, and puts each part into a button  0 - 7 
      '''
    countHeaderIndex = 0
    parsedHeader = np.array([])
    #print("len bd",len(bd),"bd at 42", bd[42]," bd at 43 ", bd[43],"bd at 44 ", bd[44],"bd at 45 ", bd[45])
    
    for i in range(len(bd)):
        if(countHeaderIndex > 43):
            break
        else:
            countHeaderIndex+=1
            #parsedHeader.append(bd[i])
            parsedHeader = np.append(parsedHeader,bd[i])
            #print(bd[i], " counter ", countHeaderIndex)
            #bd.remove(bd[i])
    #print("bd after remove ", len(bd))   
    countPosRemove = 0
    ''' for i in range(len(bd)):
        if countPosRemove > 43:
            break
        else:
            countPosRemove+=1
            bd.remove(bd[i])'''
    parsingIndex = (len(bd) - 44 ) /8 # 8 buttons
    parsingKeyCount=0
    dictKeyIndex = 0
    #print("header ", parsedHeader)

    partSongs = {0: [],1 : [],2:[],3:[],4:[],5:[],6:[],7:[]}
    #print(bd,"bin data")
    for i in range(44,len(bd)):
            if(parsingIndex < parsingKeyCount):
                # the idea is we take the song binary and then partion it into bits here, and after it pases the divison point we reset
                dictKeyIndex +=1
                parsingKeyCount = 0
            partSongs[dictKeyIndex].append( bd[i])
            parsingKeyCount+=1


    #print(bd[44:])
    #print(parsedHeader)
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

    
    ''' POTENTIAL ISSUES: 
        file when created, does not cleanup in directory, it stays there forever, 
        might cause a memory issue on the Pi which will increase slowdown.
        
        '''
    
if (__name__ == "__main__"):
    main()
