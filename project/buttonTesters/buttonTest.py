import RPi.GPIO as GPIO
import time as t


def pin5():
    print("event 5 occured ")
def pin6():
    print("event 6 occured ")
def pin13():
    print("event 13 occured ")
def pin26():
    print("event 26 occured ")
def pin19():
    print("event 19 occured ")
def main():
    ioPins = [5,6,13,19,26] # [Press Detection, 000X, 00X0, 0X00, X000]
    curState = "0000"
    audioSettings = {}
    audioList = []
    # guiStates = [[0,["None","Low","High"]],[0,["None","SpeedUp","SlowDown"]],[0,["Active"]]]
    guiStateInd = 0
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    itr = 0
    
    for pin in ioPins:
        GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(5 , GPIO.RISING, callback=pin5 , bouncetime=200)
    # GPIO.add_event_detect(6 , GPIO.RISING, callback=pin6 , bouncetime=200)
    # GPIO.add_event_detect(13 , GPIO.RISING, callback=pin13 , bouncetime=200)
    # GPIO.add_event_detect(19 , GPIO.RISING, callback=pin19 , bouncetime=200)
    # GPIO.add_event_detect(26 , GPIO.RISING, callback=pin26 , bouncetime=200)
    while True: # Run forever
        pushed = False
        if GPIO.input(5):
            print("Button was pushed! 5")
            pushed = True
        # if GPIO.input(6):
        #     print("Button was pushed! 6")
        #     t.sleep(1)
        if GPIO.input(13):
            print("Button was pushed! 13")
            pushed = True
        if GPIO.input(19):
            print("Button was pushed! 19")
            pushed = True
        if GPIO.input(26):
            print("Button was pushed! 26")
            pushed = True
        if (pushed):
            itr+=1
            print("BUTTONPUSHAMT",itr)

            t.sleep(1)

if ( __name__ == "__main__"):
    counter = 0
    global step
    step = 0

    try:
        # here you put your main loop or block of code
        while counter < 10000:
            # count up to 9000000 - takes ~20s
            #main()
            main()
            counter += 1
        print ("Target reached: %d" % counter)
        #print("tolerance ",step * 100 / len(magList))

    except KeyboardInterrupt:
        # here you put any code you want to run before the program
        # exits when you press CTRL+C
        print ("\n", counter) # print value of counter


   # except:
        # this catches ALL other exceptions including errors.
        # You won't get any error messages for debugging
        # so only use it once your code is working
       # print ("Other error or exception occurred!")
    finally:
        GPIO.cleanup() # this ensures a clean exit