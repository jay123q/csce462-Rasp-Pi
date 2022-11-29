    def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in ioPins:
            GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            #break

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
    
    
        inputPath = "./audio/"
    inputFNames = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
    raspi.guiStates[0][1] = inputFNames
    while(True):
        # print(raspi.guiStates[raspi.guiStateInd])
        # print(raspi.audioList)
        # raspi.btnReady()

        print(raspi.guiStates[raspi.guiStateInd])
        raspi.curState = input("Enter state : ")
        print(raspi.audioList)
        raspi.btnReady()
        
        
        
    WebSocketServer.send_message(
            str(self.guiStateInd) + str(self.guiStates))
        self.btnDict[self.curState]()
    
    
    global curState
    global self.guiStates
    global guiStateInd
    global audioList
    setup()
    inputPath = "./audio/"
    inputFNames = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
    self.guiStates[0][1] = inputFNames
    while(True):
        print(self.guiStates[guiStateInd])
        print(audioList)
        btnReady()