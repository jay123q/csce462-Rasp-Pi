
from playsound import playsound
#import libfmp.b
#http://pydub.com/
# pip install AudioSegment
#pip install playsound==1.2.2
def parseSong(songPath):
    """this is where the pain begins"""
    parseFile = []
    with open(songPath) as file:
        data = file.read()
        parseFile.append(data)
    print(parseFile)
def main():
    """main for playing sounds"""
    #print("hallo")
    # while (True):
    #     userInput = int(input("enter a song 1-8 being the order they appear"))
    #     if(userInput > 0 and userInput <= 8 ):
    #         break
    userInput = "drumSoundTest"
    songPath = 'C:/Users/Joshua/Documents/cscs462_Rasp_Pi/project/songs/' + userInput + ".mp3"
    filePathtoParsedSongs = 'C:/Users/Joshua/Documents/cscs462_Rasp_Pi/project/parsedSong/' 
    #parseSong(songPath)
if (__name__ == "__main__"):
    main()
