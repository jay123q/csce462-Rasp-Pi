import tornado.ioloop
import tornado.web
import tornado.websocket

#from pygame import mixer as playsound
#import playsound
from os import listdir
from os.path import isfile, join
#import RPi.GPIO as GPIO

# helperFiles/Functions
import audioFunctions




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
            client.write_message(message)


class mainRaspi:
    
    
    def __init__(self):
        self.ioPins = [5, 6, 13, 19, 26]  # [Press Detection, 000X, 00X0, 0X00, X000]
        self.curState = "0000"
        self.audioSettings = {}
        self.guiStates = [[0, []], [0, ["None", "Low", "High"]], [0, ["None", "SpeedUp", "SlowDown"]], [5, ["1/4", "1/3", "1/2", "2/3", "3/4", "1"], [1.0/4.0, 1.0/3.0, 1.0/2.0, 2.0/3.0, 3.0/4.0, 1.0]], [0, ["Active"]]]
        self.guiStateInd = 0
        self.audioList = []
        self.itr = 0
        self.playsound.init()
        self.setup()
        
    def sample(self):
        return None

    def setup(self):
        pass

    def btnReady(self):
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
        self.guiStateInd = (self.guiStateInd - 1) if (self.guiStateInd-1 > -1) else (self.guiStateInd)
        pass


    def btn_0101(self):
        # Settings checked, generate audio.
        self.guiStateInd
        self.audioList

        self.guiStateInd = len(self.guiStates)-1
        speedMultiplier = 1.0
        inputPath = "./audio/"
        outputPath = "./parsedAudio/"

        inputFNames = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
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
        self.playsound.music.load(self.audioList[0])
        self.playsound.music.play()
        print("Passed")
        pass


    def btn_1001(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        self.playsound.music.load(self.audioList[1])
        self.playsound.music.play()
        print("Passed")
        pass


    def btn_1010(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        self.playsound.music.load(self.audioList[2])
        self.playsound.music.play()
        print("Passed")
        pass


    def btn_1011(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        self.playsound.music.load(self.audioList[3])
        self.playsound.music.play()
        print("Passed")
        pass


    def btn_1100(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        self.playsound.music.load(self.audioList[4])
        self.playsound.music.play()
        print("Passed")
        pass


    def btn_1101(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        self.playsound.music.load(self.audioList[5])
        self.playsound.music.play()
        print("Passed")
        pass


    def btn_1110(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        self.playsound.music.load(self.audioList[6])
        self.playsound.music.play()
        print("Passed")
        pass


    def btn_1111(self):
        if (self.guiStateInd != (len(self.guiStates)-1)):
            return
        print("LoadingPlayFile")
        self.playsound.music.load(self.audioList[7])
        self.playsound.music.play()
        print("Passed")
        pass


    btnDict = {"0110": btn_0001, "0101": btn_0010, "1101": btn_0011, "1001": btn_0100, "0100": btn_0101, "0110": btn_0110, "1111": btn_0111,
               "0111": btn_1000, "1011": btn_1001, "0011": btn_1010, "0100": btn_1011, "0010": btn_1100, "1110": btn_1101, "1010": btn_1110, "1000": btn_1111}


        



def main():

    app = tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)

    # Create an event loop (what Tornado calls an IOLoop).
    io_loop = tornado.ioloop.IOLoop.current()

    WebSocketServer.send_message(str("inputDataHere"))

    # Start the event loop.
    io_loop.start()


if __name__ == "__main__":
    main()