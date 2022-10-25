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
songPath = '/Users/rohanlingala/Documents/GitHub/csce462-Rasp-Pi/project/songs/' + userInput + ".wav"
filePathtoParsedSongs = '/Users/rohanlingala/Documents/GitHub/csce462-Rasp-Pi/project/parsedSong/'
JOSH PATH VARIABLES: 
songPath = '/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/songs/' + userInput + '.wav'
filePathtoParsedSongs = '/Users/Joshua/Documents/github/PersonalGit/csce462-Rasp-Pi/project/parsedSong/'
--------------------------------------------------------------------------------------------------------------------------
'''

from playsound import playsound #pip install playsound==1.2.2
import numpy as np
import scipy.io as scipy
import bitHelpers


def buttonSong(parsedSong = dict):
    for i in parsedSong:
        playsound(parsedSong[i])


def writeNewSongs(filePathtoParsedSongs, parsedSong, sampleRate, lowPass, highPass, speedUp, slowDown):
    sampleRate = int( speedUp*sampleRate / slowDown )
    for i in range(len(parsedSong)):

        fileName = filePathtoParsedSongs + 'songPart'+str(i) + '.wav'
        scipy.wavfile.write(fileName,sampleRate,parsedSong[i])
        
        #if(lowPass == 1):
        bitHelpers.lowPass(fileName, sampleRate)
        
def songPicker():
    '''logic to up down and select song'''


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

    backToLast = 0
    filePathtoParsedSongs = './parsedSong/'
    #parsedFN = "16bitsnare"

    # directory control logic here
    userInput = 'drumSounds1'
    songPath = './songs/' + userInput + ".wav"
    
    parsedWavs, sampleRate = parseSongWav(songPath)

    highFilter = 1
    lowFilter = 1   
    highFilterPin = 1
    lowFilterPin = 0

       # test here by changing these values for speedup slowdown 
    speedUpRate = 1
    slowDownRate = 1
    speedUpPin = 0
    slowDownPin  = 0
    
    # replace this block with gpio pin detection
    if (lowFilterPin):
        # dumby values change later 
        # trigger something to filter?
        lowFilter = 2
    if (highFilterPin):
        # some change to apply a filter
        # trigger something to filter?
        highFilter = 2
    
    # if input detected here change list back to old function
    if(backToLast):
        print("shifting back to song select ")

    # replace this block with gpio pin detection
    if (speedUpPin):
        speedUpRate = 2
    if (slowDownPin):
        # this might need logic to better parse the song
        slowDownRate = 2
     
        
    if(backToLast):
        print("shifting back to low/hight")

    
    writeNewSongs(filePathtoParsedSongs,parsedWavs, sampleRate,lowFilter,highFilter,speedUpRate,slowDownRate)
    highFilter = 0
    lowFilter = 0
    speedUp = 1
    slowDown = 1

if (__name__ == "__main__"):
    main()