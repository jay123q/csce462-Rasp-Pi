import RPi.GPIO as GPIO
import playsound
import time
from os import listdir
from os.path import isfile, join

# helperFiles/Functions
import audioFunctions

# Globals
ioPins = [5,6,13,19,26] # [Press Detection, 000X, 00X0, 0X00, X000]
curState = "0000"
audioSettings = {}
audioList = []
guiStates = [[0,["None","Low","High"]],[0,["None","SpeedUp","SlowDown"]],[0,["Active"]]]
guiStateInd = 0
itr = 0


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in ioPins:
        GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #break

def btnUnpressed():
    global curState
    global itr
    itr+=1
    GPIO.wait_for_edge(ioPins[0], GPIO.RISING) # Waits on any button pressed.
    print("Pressed")
    i = 50000
    bool1, bool2, bool3, bool4 = False, False, False, False
    while (i > 0):
        if (GPIO.input(ioPins[1])):
            bool1 = True
        if (GPIO.input(ioPins[2])):
            bool2 = True
        if (GPIO.input(ioPins[3])):
            bool3 = True
        if (GPIO.input(ioPins[4])):
            bool4 = True
        i-=1
    curState = ("1" if (bool1) else "0") + ("1" if (bool2) else "0") + ("1" if (bool3) else "0") + ("1" if (bool4) else "0")
    print("Button State Pressed", curState)
    print("Total buttons pressed", itr)
    #btnDict[curState]()
    pass
    
def btn_0001():
    # Iterate current setting forward
    if (guiStateInd == 2):
        return
    global guiStates
    guiStates[guiStateInd][0] = (guiStates[guiStateInd][0] + 1) if (guiStates[guiStateInd][0] + 1 < len(guiStates[guiStateInd][1])) else (guiStates[guiStateInd][0])
    pass

def btn_0010():
    # Iterate current setting backward
    if (guiStateInd == 2):
        return
    global guiStates
    guiStates[guiStateInd][0] = (guiStates[guiStateInd][0] - 1) if (guiStates[guiStateInd][0] - 1 > -1) else (guiStates[guiStateInd][0])
    pass

def btn_0011():
    # Advance to next state
    global guiStateInd
    guiStateInd = (guiStateInd + 1) if (guiStateInd + 1 < len(guiStates)) else (guiStateInd)
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
    guiStateInd = 2
    
    inputPath = "./audio/"
    outputPath = "./parsedAudio/"
    inputFNames = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
    for fName in inputFNames:
        audioFunctions.writeSong(inputPath+fName, outputPath, passState = 0, speedMultiplier = 1.0)
        audioList = [outputPath + f for f in listdir(outputPath) if isfile(join(outputPath, f))]
    pass

def btn_0110():
    # Free Button
    pass

def btn_0111():
    # Free Button
    pass

def btn_1000():
    if (guiStateInd != 2):
        return
    playsound(audioList[0])
    pass

def btn_1001():
    if (guiStateInd != 2):
        return
    playsound(audioList[1])
    pass

def btn_1010():
    if (guiStateInd != 2):
        return
    playsound(audioList[2])
    pass

def btn_1011():
    if (guiStateInd != 2):
        return
    playsound(audioList[3])
    pass

def btn_1100():
    if (guiStateInd != 2):
        return
    playsound(audioList[4])
    pass

def btn_1101():
    if (guiStateInd != 2):
        return
    playsound(audioList[5])
    pass

def btn_1110():
    if (guiStateInd != 2):
        return
    playsound(audioList[6])
    pass

def btn_1111():
    if (guiStateInd != 2):
        return
    playsound(audioList[7])
    pass

btnDict = {"0001" : btn_0001,"0010" : btn_0010,"0011" : btn_0011,"0100" : btn_0100,"0101" : btn_0101,"0110" : btn_0110,"0111" : btn_0111,"1000" : btn_1000,"1001" : btn_1001,"1010" : btn_1010,"1011" : btn_1011,"1100" : btn_1100,"1101" : btn_1101,"1110" : btn_1110,"1111" : btn_1111}

def main():
    setup()
    while(True):

        btnUnpressed()
        time.sleep(.5)
        
if (__name__ == "__main__"):
    main()