#from pygame import mixer as playsound
#import playsound
from os import listdir
from os.path import isfile, join

# helperFiles/Functions
import audioFunctions

# Globals
ioPins = [5, 6, 13, 19, 26]  # [Press Detection, 000X, 00X0, 0X00, X000]
curState = "0000"
audioSettings = {}
guiStates = [[0, []], [0, ["None", "Low", "High"]], [0, ["None", "SpeedUp", "SlowDown"]], [5, ["1/4", "1/3", "1/2", "2/3", "3/4", "1"],
                                                                                           [1.0/4.0, 1.0/3.0, 1.0/2.0, 2.0/3.0, 3.0/4.0, 1.0]], [0, ["Active"]]]
guiStateInd = 0
audioList = []
#playsound.init()




def setup():
    pass


def btnReady():
    btnDict[curState]()
    pass


def btn_0001():
    # Iterate current setting forward
    global guiStates
    if (guiStateInd == len(guiStates)-1):
        return
    guiStates[guiStateInd][0] = (guiStates[guiStateInd][0] + 1) if (guiStates[guiStateInd]
                                                                    [0] + 1 < len(guiStates[guiStateInd][1])) else (guiStates[guiStateInd][0])
    pass


def btn_0010():
    # Iterate current setting backward
    global guiStates
    if (guiStateInd == len(guiStates)-1):
        return
    guiStates[guiStateInd][0] = (guiStates[guiStateInd][0] - 1) if (
        guiStates[guiStateInd][0] - 1 > -1) else (guiStates[guiStateInd][0])
    pass


def btn_0011():
    # Advance to next state
    global guiStateInd
    guiStateInd = (guiStateInd + 1) if (guiStateInd +
                                        1 < len(guiStates)) else (guiStateInd)
    if (guiStateInd == len(guiStates)-1):
        btn_0101()
    pass


def btn_0100():
    # Backtrack to prior state
    global guiStateInd
    guiStateInd = (guiStateInd - 1) if (guiStateInd-1 > -1) else (guiStateInd)
    pass


def btn_0101():
    # Settings checked, generate audio.
    global guiStateInd
    global audioList

    guiStateInd = len(guiStates)-1
    speedMultiplier = 1.0
    inputPath = "./audio/"
    outputPath = "./parsedAudio/"

    inputFNames = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
    speedMultiplier *= 1.5 if (guiStates[2][0] == 1) else 1.0
    speedMultiplier *= 0.75 if (guiStates[2][0] == 2) else 1.0
    print(speedMultiplier)
    fName = guiStates[0][1][guiStates[0][0]]
    audioFunctions.writeSong(inputPath, outputPath, fName,
                             guiStates[0][0], speedMultiplier, guiStates[3][2][guiStates[3][0]])
    audioList = [outputPath +
                 f for f in listdir(outputPath) if isfile(join(outputPath, f))]
    pass


def btn_0110():
    # Free Button
    pass


def btn_0111():
    # Free Button
    pass


def btn_1000():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[0])
    playsound.music.play()
    print("Passed")
    pass


def btn_1001():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[1])
    playsound.music.play()
    print("Passed")
    pass


def btn_1010():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[2])
    playsound.music.play()
    print("Passed")
    pass


def btn_1011():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[3])
    playsound.music.play()
    print("Passed")
    pass


def btn_1100():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[4])
    playsound.music.play()
    print("Passed")
    pass


def btn_1101():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[5])
    playsound.music.play()
    print("Passed")
    pass


def btn_1110():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[6])
    playsound.music.play()
    print("Passed")
    pass


def btn_1111():
    if (guiStateInd != (len(guiStates)-1)):
        return
    print("LoadingPlayFile")
    playsound.music.load(audioList[7])
    playsound.music.play()
    print("Passed")
    pass


btnDict = {"0001": btn_0001, "0010": btn_0010, "0011": btn_0011, "0100": btn_0100, "0101": btn_0101, "0110": btn_0110, "0111": btn_0111,
           "1000": btn_1000, "1001": btn_1001, "1010": btn_1010, "1011": btn_1011, "1100": btn_1100, "1101": btn_1101, "1110": btn_1110, "1111": btn_1111}


def main():
    global curState
    global guiStates
    global guiStateInd
    global audioList
    setup()
    inputPath = "./audio/"
    inputFNames = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
    guiStates[0][1] = inputFNames
    while(True):
        print(guiStates[guiStateInd])
        curState = input("Enter state : ")
        print(audioList)
        btnReady()


if (__name__ == "__main__"):
    main()
