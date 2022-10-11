'''
-------------------------------parseSong.py-----------------------------------------------------------------------------
pip install soundfile

all you need to install! Make sure to change directories in the main. 
I am going to send the wav file inside the folder in the Github, place it in whatever directory you want :)


REFERENCES

https://docs.python.org/3/library/wave.html#module-wave

https://stackoverflow.com/questions/69291258/reading-wav-as-bytes

https://stackoverflow.com/questions/45010682/how-can-i-convert-bytes-object-to-decimal-or-binary-representation-in-python
--------------------------------------------------------------------------------------------------------------------------
'''
from playsound import playsound #pip install playsound==1.2.2
import wave
import numpy as np
import soundfile as sf

def buttonSong(parsedSong = dict):
    """In this final design this will  be a interupt method that allows us to assign the press to 8 gpio pins drive 3 volts and the button press triggers a input
    IN ALHPA it will be a simple player"""
    # first create the new wav
    for i in parsedSong:
        playsound(parsedSong[i])





def writeNewSongs(filePathtoParsedSongs, parsedSong):
    """this will write the new song and create several using the parsed song dictionary"""
        #parseFile = filePathtoParsedSongs + userInput + '.wav' 
    
    
    '''using soundfile.read, you are able to return the data (audioframes, 
    just blackbox it )and return the samplerate (used for sf.write). We can 
    then use this 32 bit formatted data to write to a new file directory (parseFile) 
    in order to create a new 16 bit wav file.'''
    counter = 0
    fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
    for i in parsedSong:
        samplerate = sf.read(parsedSong[i])
        fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
        p_data = sf.write(fileName, parsedSong[i] , samplerate, subtype='PCM_16')
        counter+=1
    '''create the new 16 bit wave object.'''





def parseSong(songPath, parseFileName):
    
    #parseFile = parsePath + parseFileName + '.wav' 
    
    '''create string that is the directory of new file, we create the path first
    and then create the wav file that belongs in that path in line 24. The reason 
    we do is because we need to create a new wav file that has 16 bit format, and we 
    need to make sure it is 16 bit by creating a new file we can use.'''

    """Josh here simplifying this to be a more clean function"""
    #writeNewSongs(songPath, parseFile) this does what was here
    
    wf = wave.open(songPath, 'rb')
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
      '''Josh here
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
    # while (True):
    #     userInput = int(input("enter a song 1-8 being the order they appear"))
    #     if(userInput > 0 and userInput <= 8 ):
    #         break
    userInput = "drumSounds1"
    #songPath = '/Users/rohanlingala/Downloads/proj462/wav/' + userInput + ".wav"
    #filePathtoParsedSongs = '/Users/rohanlingala/Downloads/proj462/p_wav/' 
    #songPath = 'C:/Users/Joshua/Documents/cscs462_Rasp_Pi/project/songs/' + userInput + ".wav"
    #filePathtoParsedSongs = 'C:/Users/Joshua/Documents/cscs462_Rasp_Pi/project/parsedSong/'     
    songPath = 'C:/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/songs/' + userInput + ".wav"
    filePathtoParsedSongs = 'C:/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/parsedSong/'
    #parseFile = filePathtoParsedSongs + userInput + '.wav' 

    parsedFN = "16bitsnare"
    organizedDict = parseSong(songPath, parsedFN)
    writeNewSongs(filePathtoParsedSongs,organizedDict)
    #playsound(organizedDict)
    
    ''' POTENTIAL ISSUES: 
        file when created, does not cleanup in directory, it stays there forever, 
        might cause a memory issue on the Pi which will increase slowdown.
        
        '''
    
if (__name__ == "__main__"):
    main()
