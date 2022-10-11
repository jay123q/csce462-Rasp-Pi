'''
-------------------------------parseSong.py-----------------------------------------------------------------------------
pip install soundfile

all you need to install! Make sure to change directories in the main. 
I am going to send the wav file over email, place it in whatever directory you want :)


REFERENCES

https://docs.python.org/3/library/wave.html#module-wave

https://stackoverflow.com/questions/69291258/reading-wav-as-bytes

https://stackoverflow.com/questions/45010682/how-can-i-convert-bytes-object-to-decimal-or-binary-representation-in-python
--------------------------------------------------------------------------------------------------------------------------
'''

import wave
import numpy as np
import soundfile as sf


def parseSong(songPath, parsePath, parseFileName):
    
    parseFile = parsePath + parseFileName + '.wav' 
    
    '''create string that is the directory of new file, we create the path first
    and then create the wav file that belongs in that path in line 24. The reason 
    we do is because we need to create a new wav file that has 16 bit format, and we 
    need to make sure it is 16 bit by creating a new file we can use.'''

    data, samplerate = sf.read(songPath) 
    '''using soundfile.read, you are able to return the data (audioframes, 
    just blackbox it )and return the samplerate (used for sf.write). We can 
    then use this 32 bit formatted data to write to a new file directory (parseFile) 
    in order to create a new 16 bit wav file.'''
    
    p_data = sf.write(parseFile, data, samplerate, subtype='PCM_16')
    '''create the new 16 bit wave object.'''
    
    wf = wave.open(parseFile, 'rb')
    bin_data = wf.readframes(wf.getparams().nframes)
    '''open the filepath with the newly constructed wave file to read bytes. 
    Inside bin_data, i am using getparams() which returns a tuple, inside that 
    tuple I can call nframes as a thing inside the tuple to give me the number
    of audio frames inside the new file, and then i use readframes() to return
    the audio frames as a byte object. this will spit out a huge array of hex
    values. '''
    bd = []
    for my_byte in bin_data:
      bd.append(f'{my_byte:0>8b}')
      
    #print(bd)
    ''' I am taking my bytes object, and using this to convert the hex into 
    binary data then Using a for loop, I am append each 8 bit string as a 
    value into a list.'''
    

def main():
    userInput = "snare"
    songPath = '/Users/rohanlingala/Downloads/proj462/wav/' + userInput + ".wav"
    filePathtoParsedSongs = '/Users/rohanlingala/Downloads/proj462/p_wav/' 
    parsedFN = "16bitsnare"
    parseSong(songPath, filePathtoParsedSongs, parsedFN)
    
    ''' POTENTIAL ISSUES: 
        file when created, does not cleanup in directory, it stays there forever, 
        might cause a memory issue on the Pi which will increase slowdown.
        
        '''
    
if (__name__ == "__main__"):
    main()
