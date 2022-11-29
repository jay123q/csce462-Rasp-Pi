from pygame import mixer as playsound
#import playsound
from os import listdir
from os.path import isfile, join
import RPi.GPIO as GPIO

# helperFiles/Functions


# Globals
ioPins = [5, 6, 13, 19, 26]  # [Press Detection, 000X, 00X0, 0X00, X000]
curState = "0000"
audioSettings = {}
guiStates = [[0, []], [0, ["None", "Low", "High"]], [0, ["None", "SpeedUp", "SlowDown"]], [5, ["1/4", "1/3", "1/2", "2/3", "3/4", "1"],
                                                                                           [1.0/4.0, 1.0/3.0, 1.0/2.0, 2.0/3.0, 3.0/4.0, 1.0]], [0, ["Active"]]]
global btnDict

guiStateInd = 0
audioList = []
itr = 0
playsound.init()

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in ioPins:
        GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #break

def btn_0001():
    # Iterate current setting forward
    print("B")
    pass


def btn_0010():
    # Iterate current setting backward
    print("D")
    pass

def btn_0011():
    # Advance to next state
    print("C")
    pass



def btn_0100():
    # Backtrack to prior state
    print("E")
    pass



def btn_0101():
    # Settings checked, generate audio.
    print("F")
    pass



def btn_0110():
    # Free Button
    print("A")
    pass

def btn_0111():
    # Free Button
    print("G")
    pass

def btn_1000():
    print('H')
    pass


def btn_1001():
    print("I")
    pass


def btn_1010():
    print('J')
    pass


def btn_1011():
    print('K')
    pass


def btn_1100():
    print('L')
    pass


def btn_1101():
    print('M')
    pass


def btn_1110():
    print('N')
    pass


def btn_1111():
    print('O')
    pass
def btnReady():
    global curState
    global itr
    itr+=1
    GPIO.wait_for_edge(ioPins[0], GPIO.RISING) # Waits on any button pressed.
    print("Pressed")
    i = 99999
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
    if (curState not in btnDict):
        return
    print("Button State Pressed", curState)
    print("Total buttons pressed", itr)
    btnDict[curState]()
    pass
btnDict = {"1000": btn_0110 , "0110": btn_0001 , "0101": btn_0011 , "1101": btn_0010 ,"1001": btn_0100 ,"0001": btn_0101 
,"1100": btn_0111 ,"1010": btn_1000 ,"1110":btn_1001,"0010":btn_1010,"0100": btn_1011,"0011":btn_1100,"1011":btn_1101,"0111":btn_1110,"1111":btn_1111}
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
        print(audioList)
        btnReady()
        
if (__name__ == "__main__"):
    main()