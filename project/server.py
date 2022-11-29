import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

#from pygame import mixer as playsound
import playsound
from os import listdir
from os.path import isfile, join, dirname
#import RPi.GPIO as GPIO

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
    # Note that `clients` is a class variable and `send_message` is a
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
        settings = {
            "static_path": join(dirname(__file__), "static"),
        }
        
        self.app = tornado.web.Application(
            handlers = [(r"/", MainHandler),(r"/filterselect", fs),(r"/songselect", ss),(r"/timestrechselect", ts),
            (r"/websocket/", WebSocketServer),
            (r"/(.*)",tornado.web.StaticFileHandler, {"path": "./html_css"},),
             ],
            
            websocket_ping_interval=100,
            websocket_ping_timeout=300,
            **settings
        )
        
        self.app.listen(8888)

        self.io_loop = tornado.ioloop.IOLoop.current()

        periodic_callback = tornado.ioloop.PeriodicCallback(
            lambda: WebSocketServer.send_message(str(1)), 100
        )
        periodic_callback.start()
        self.io_loop.start()

        # [Press Detection, 000X, 00X0, 0X00, X000]
        self.ioPins = [5, 6, 13, 19, 26]
        self.curState = "0000"
        self.audioSettings = {}
        self.guiStates = [[0, []], [0, ["None", "Low", "High"]], [0, ["None", "SpeedUp", "SlowDown"]], [5, [
            "1/4", "1/3", "1/2", "2/3", "3/4", "1"], [1.0/4.0, 1.0/3.0, 1.0/2.0, 2.0/3.0, 3.0/4.0, 1.0]], [0, ["Active"]]]
        self.guiStateInd = 0
        self.audioList = []
        self.itr = 0
        # playsound.init()
        self.setup()
        self.btnDict = {"011X": self.btn_0001, "0101": self.btn_0010, "1101": self.btn_0011, "1001": self.btn_0100, "0100": self.btn_0101, "0110": self.btn_0110, "1111": self.btn_0111,
                        "0111": self.btn_1000, "1011": self.btn_1001, "0011": self.btn_1010, "0100": self.btn_1011, "0010": self.btn_1100, "1110": self.btn_1101, "1010": self.btn_1110, "1000": self.btn_1111}

    def sample(self):
        return None

    def setup(self):
        pass

    def btnReady(self):

        WebSocketServer.send_message(
            str(self.guiStateInd) + str(self.guiStates))
        self.btnDict[self.curState]()
        pass

    def btn_0001(self):
        # Iterate current setting forward
        if (self.guiStateInd == len(self.guiStates)-1):
            return
        self.guiStates[self.guiStateInd][0] = (self.guiStates[self.guiStateInd][0] + 1) if (self.guiStates[self.guiStateInd]
                                                                                            [0] + 1 < len(self.guiStates[self.guiStateInd][1])) else (self.guiStates[self.guiStateInd][0])
        pass

    def btn_0010(self):
        # Iterate current setting backward
        if (self.guiStateInd == len(self.guiStates)-1):
            return
        self.guiStates[self.guiStateInd][0] = (self.guiStates[self.guiStateInd][0] - 1) if (
            self.guiStates[self.guiStateInd][0] - 1 > -1) else (self.guiStates[self.guiStateInd][0])
        pass

    def btn_0011(self):
        # Advance to next state
        self.guiStateInd
        self.guiStateInd = (self.guiStateInd + 1) if (self.guiStateInd +
                                                      1 < len(self.guiStates)) else (self.guiStateInd)
        if (self.guiStateInd == len(self.guiStates)-1):
            self.btn_0101()
        pass

    def btn_0100(self):
        # Backtrack to prior state
        self.guiStateInd
        self.guiStateInd = (
            self.guiStateInd - 1) if (self.guiStateInd-1 > -1) else (self.guiStateInd)
        pass

    def btn_0101(self):
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

    def btn_0110(self):
        # Free Button
        pass

    def btn_0111(self):
        # Free Button
        pass

    def btn_1000(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[0])
        # playsound.music.play()
        print("Passed")
        pass

    def btn_1001(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[1])
        # playsound.music.play()
        print("Passed")
        pass

    def btn_1010(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[2])
        # playsound.music.play()
        print("Passed")
        pass

    def btn_1011(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[3])
        # playsound.music.play()
        print("Passed")
        pass

    def btn_1100(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[4])
        # playsound.music.play()
        print("Passed")
        pass

    def btn_1101(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[5])
        # playsound.music.play()
        print("Passed")
        pass

    def btn_1110(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[6])
        # playsound.music.play()
        print("Passed")
        pass

    def btn_1111(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        # playsound.music.load(self.audioList[7])
        # playsound.music.play()
        print("Passed")
        pass


def main():
    raspi = mainRaspi()
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


if __name__ == "__main__":
    main()
