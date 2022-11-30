import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import asyncio
import json
from tornado import gen
import time

from pygame import mixer as playsound
# import playsound
from os import listdir
from os.path import isfile, join, dirname
import RPi.GPIO as GPIO

# helperFiles/Functions
import audioFunctions


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./html_css/frontpage.html")


class fs(tornado.web.RequestHandler):
    def get(self):
        self.render("./html_css/filterselect.html")


class ss(tornado.web.RequestHandler):
    def get(self):
        self.render("./html_css/songselect.html")


class ts(tornado.web.RequestHandler):
    def get(self):
        self.render("./html_css/timestrechselect.html")


class WebSocketServer(tornado.websocket.WebSocketHandler):
    # Note that `clients` is forwardState class variable and `send_message` is forwardState
    # classmethod.
    clients = set()

    def open(self):
        WebSocketServer.clients.add(self)

    def on_close(self):
        WebSocketServer.clients.remove(self)

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message {message} to {len(cls.clients)} client(s).")
        for client in cls.clients:
            print(str(client))
            client.write_message(message)


class mainRaspi:

    def __init__(self):

        # [Press Detection, 000X, 00X0, 0X00, X000]
        self.ioPins = [5, 6, 13, 19, 26]
        self.curState = "0000"
        self.audioSettings = {}
        self.guiStates = [[0, []], [0, ["None", "Low", "High"]], [0, ["None", "SpeedUp", "SlowDown"]], [5, [
            "1/4", "1/3", "1/2", "2/3", "3/4", "1"], [1.0/4.0, 1.0/3.0, 1.0/2.0, 2.0/3.0, 3.0/4.0, 1.0]], [0, ["Active"]]]
        self.guiStateInd = 0
        self.audioList = []
        self.itr = 0
        inputPath = "./audio/"
        inputFNames = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
        self.guiStates[0][1] = inputFNames
        playsound.init()
        self.setup()

        self.btnDict = {
            "1001": self.forwardState, 
            "0101": self.leftOption, 
            "1101": self.rightOption, 
            "0110": self.backState,
            "0001": self.confirmGenerate,
            "1100": self.resetPref,
            "1000": self.playAll,
            "1010": self.play1,
            "1110": self.play2,
            "0010": self.play3,
            "0100": self.play4,
            "0011": self.play5,
            "1011": self.play6,
            "0111": self.play7,
            "1111": self.play8
            }
        # self.btnDict = {"011": self.forwardState, "0101": self.leftOption, "1101": self.rightOption, "1001": self.backState, "0100": self.confirmGenerate, "0110": self.playAll, "1111": self.resetPref,
        #                 "0111": self.play1, "1011": self.play2, "0011": self.play3, "0100": self.play5, "0010": self.play5, "1110": self.play6, "1010": self.play7, "1000": self.play8}

        self.appStart()

    def appStart(self):
        settings = {
            "static_path": join(dirname(__file__), "static"),
        }
        self.app = tornado.web.Application(
            handlers=[(r"/", MainHandler), (r"/filterselect", fs), (r"/songselect", ss), (r"/timestrechselect", ts),
                      (r"/websocket", WebSocketServer),
                      (r"/(.*)", tornado.web.StaticFileHandler,
                       {"path": "./html_css"},),
                      ],

            websocket_ping_interval=100,
            websocket_ping_timeout=300,
            **settings
        )
        
        
        self.app.listen(8888)

        self.io_loop = tornado.ioloop.IOLoop.current()
        periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: self.btnReady(), 1)
        periodic_callback.start()
        self.io_loop.start()
        
    def sample(self):
        return None

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.ioPins:
            GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            #break

            
    def btnReady(self):
        if not (GPIO.input(self.ioPins[0])):
            return
        i = 99999
        bool1, bool2, bool3, bool4 = False, False, False, False
        while (i > 0):
            if (GPIO.input(self.ioPins[1])):
                bool1 = True
            if (GPIO.input(self.ioPins[2])):
                bool2 = True
            if (GPIO.input(self.ioPins[3])):
                bool3 = True
            if (GPIO.input(self.ioPins[4])):
                bool4 = True
            i-=1
        self.curState = ("1" if (bool1) else "0") + ("1" if (bool2) else "0") + ("1" if (bool3) else "0") + ("1" if (bool4) else "0")
        if (self.curState not in self.btnDict):
            return
        print("Button State Pressed", self.curState)
        print("Total buttons pressed", self.itr)
        WebSocketServer.send_message(str(json.dumps([self.guiStateInd,self.guiStates])))
        self.btnDict[self.curState]()
        time.sleep(0.5)
        pass




    def forwardState(self):
        # Iterate current setting forward
        if (self.guiStateInd == len(self.guiStates)-1):
            return
        self.guiStates[self.guiStateInd][0] = (self.guiStates[self.guiStateInd][0] + 1) if (self.guiStates[self.guiStateInd]
                                                                                            [0] + 1 < len(self.guiStates[self.guiStateInd][1])) else (self.guiStates[self.guiStateInd][0])
        pass

    def leftOption(self):
        # Iterate current setting backward
        if (self.guiStateInd == len(self.guiStates)-1):
            return
        self.guiStates[self.guiStateInd][0] = (self.guiStates[self.guiStateInd][0] - 1) if (
            self.guiStates[self.guiStateInd][0] - 1 > -1) else (self.guiStates[self.guiStateInd][0])
        pass

    def rightOption(self):
        # Advance to next state
        self.guiStateInd
        self.guiStateInd = (self.guiStateInd + 1) if (self.guiStateInd +
                                                      1 < len(self.guiStates)) else (self.guiStateInd)
        if (self.guiStateInd == len(self.guiStates)-1):
            self.confirmGenerate()
        pass

    def backState(self):
        # Backtrack to prior state
        self.guiStateInd
        self.guiStateInd = (
            self.guiStateInd - 1) if (self.guiStateInd-1 > -1) else (self.guiStateInd)
        pass

    def confirmGenerate(self):
        # Settings checked, generate audio.
        self.guiStateInd
        self.audioList

        self.guiStateInd = len(self.guiStates)-1
        speedMultiplier = 1.0
        inputPath = "./audio/"
        outputPath = "./parsedAudio/"

        inputFNames = [f for f in listdir(
            inputPath) if isfile(join(inputPath, f))]
        speedMultiplier *= 1.5 if (self.guiStates[2][0] == 1) else 1.0
        speedMultiplier *= 0.75 if (self.guiStates[2][0] == 2) else 1.0
        print(speedMultiplier)
        fName = self.guiStates[0][1][self.guiStates[0][0]]
        audioFunctions.writeSong(inputPath, outputPath, fName,
                                 self.guiStates[0][0], speedMultiplier, self.guiStates[3][2][self.guiStates[3][0]])
        self.audioList = [outputPath +
                          f for f in listdir(outputPath) if isfile(join(outputPath, f))]
        pass

    def playAll(self):
        # play all audio with presets
        playsound.music.load(self.audioList[8])
        playsound.music.play()
        pass

    def resetPref(self):
        # reset presets
        
        self.guiStateInd = len(self.guiStates)-1
        speedMultiplier = 1.0
        inputPath = "./audio/"
        outputPath = "./parsedAudio/"

        inputFNames = [f for f in listdir(
            inputPath) if isfile(join(inputPath, f))]
        speedMultiplier = 1

        fName = self.guiStates[0][1][self.guiStates[0][0]]
        audioFunctions.writeSong(inputPath, outputPath, fName,
                                 self.guiStates[0][0], speedMultiplier, self.guiStates[3][2][self.guiStateInd])
        self.audioList = [outputPath +
                          f for f in listdir(outputPath) if isfile(join(outputPath, f))]
        pass

    def play1(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[0])
        playsound.music.play()
        print("Passed")
        pass

    def play2(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[1])
        playsound.music.play()
        print("Passed")
        pass

    def play3(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[2])
        playsound.music.play()
        print("Passed")
        pass

    def play4(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[3])
        playsound.music.play()
        print("Passed")
        pass

    def play5(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[4])
        playsound.music.play()
        print("Passed")
        pass

    def play6(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[5])
        playsound.music.play()
        print("Passed")
        pass

    def play7(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[6])
        playsound.music.play()
        print("Passed")
        pass

    def play8(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        playsound.music.load(self.audioList[7])
        playsound.music.play()
        print("Passed")
        pass


def main():
    raspi = mainRaspi()
    print("Halted")



if __name__ == "__main__":
    main()
