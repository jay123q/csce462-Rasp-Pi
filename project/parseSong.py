
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


JOSH PATH VARIABLES: /*TODO*/
--------------------------------------------------------------------------------------------------------------------------
'''
from playsound import playsound #pip install playsound==1.2.2
import wave
import numpy as np
import soundfile as sf
import io
def buttonSong(parsedSong = dict):
    """Josh: In this final design this will  be a interupt method that allows us to assign the press to 8 gpio pins drive 3 volts and the button press triggers a input
    IN ALHPA it will be a simple player"""
    # first create the new wav
    for i in parsedSong:
        playsound(parsedSong[i])



def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

def writeNewSongs(filePathtoParsedSongs, parsedSong):
    """Josh: this will write the new song and create several using the parsed song dictionary"""
        #parseFile = filePathtoParsedSongs + userInput + '.wav' 
    
    
    '''Josh: using soundfile.read, you are able to return the data (audioframes, 
    just blackbox it )and return the samplerate (used for sf.write). We can 
    then use this 32 bit formatted data to write to a new file directory (parseFile) 
    in order to create a new 16 bit wav file.'''
    
    counter = 0
    fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
    
    '''attached below from lines 44 - 56 is me attempting to take the 0th index 
    of the parsedSong and turning it into a array of bytes. '''
    parse_test = parsedSong[0]
    #print(type(parse_test[0]))
    loop_len = (len(parse_test))
    
    chop_list = np.array([])
    '''below, I am looping through the 0th index and turning each bitstring into a byte using some
    stack overflow magic! '''
    
    for i in range(1,loop_len):
        #chop_list= np.append(chop_list,((int(parse_test[i],2)).to_bytes(8, byteorder='little')))
        chop_list= np.append(chop_list,bitstring_to_bytes(parse_test[i]))
    #chop_list = bytes(chop_list)
    #print(bytearray(chop_list))
    '''turn this array into a biggggg byte array!'''
    chop_list = bytearray(chop_list)
    #print(chop_list)
    
    '''at this point in the code, I THINK I have an array of bytes that should represent
    a wav file, but I am suspecting it is not being recognized and spitting out:
        
    LibsndfileError: Error opening <_io.BytesIO object at 0x7fdbb866e270>: Format not recognised.
    
    This is probably because it does not have the header that wav files are supposed to have. 
    https://docs.fileformat.com/audio/wav/ has information on what belongs in the first 44 bytes 
    of the wav file, we need to add these to the beginning of the byte array in order for this 
    byte array to be considered a "WAV" file.
        '''
    
    for i in parsedSong:
        data, samplerate = sf.read(io.BytesIO(chop_list))
        fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
        p_data = sf.write(fileName, data , samplerate, subtype='PCM_16')
        counter+=1
        
    '''Josh: create the new 16 bit wave object.'''
    
    '''Rohan: What you could do to fix line 46 is to maybe take the list of bits, 
    turn it into a bytes object, and find a way to to THAT back into a wav file. 
    I think what I would do it create a filepath for the wave file, then create
    said wave file into that wave path, its a similar implementation to my original
    parseSongs however it is much smarter to do that compartmentalized here :)'''
    

def parseSong(songPath, parseFileName):
    
    '''Rohan: create string that is the directory of new file, we create the path first
    and then create the wav file that belongs in that path in line 24. The reason 
    we do is because we need to create a new wav file that has 16 bit format, and we 
    need to make sure it is 16 bit by creating a new file we can use.'''

    """Josh: simplifying this to be a more clean function"""
    
    wf = wave.open(songPath, 'rb')
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
    parsingIndex = len(bd)/8 # 8 buttons
    parsingKeyCount=0
    dictKeyIndex = 0
    partSongs = {0: [],1 : [],2:[],3:[],4:[],5:[],6:[],7:[]}
    
    for i in range(len(bd)):
        if(parsingIndex < parsingKeyCount):
            # the idea is we take the song binary and then partion it into bits here, and after it pases the divison point we reset
            dictKeyIndex +=1
            parsingKeyCount = 0
        partSongs[dictKeyIndex].append( bd[i])
        parsingKeyCount+=1
    ''' I am taking my bytes object, and using this to convert the hex into 
    binary data then Using a for loop, I am append each 8 bit string as a 
    value into a list.'''
    return partSongs

    

def main():
    userInput = "snare"
    songPath = '/Users/rohanlingala/Downloads/proj462/wav/' + userInput + ".wav"
    filePathtoParsedSongs = '/Users/rohanlingala/Downloads/proj462/p_wav/' 
    parsedFN = "16bitsnare"
    
    organizedDict = parseSong(songPath, parsedFN)
    writeNewSongs(filePathtoParsedSongs,organizedDict)

    
    ''' POTENTIAL ISSUES: 
        file when created, does not cleanup in directory, it stays there forever, 
        might cause a memory issue on the Pi which will increase slowdown.
        
        '''
    
if (__name__ == "__main__"):
    main()
