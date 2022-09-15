import RPi.GPIO as GPIO
import time as time


def startStates():

    # script the "light show"

    #State 2
    for i in range(3):
        print("stage 2 \n")
        GPIO.output(BlueT, 0)
        time.sleep(1)
        GPIO.output(BlueT,1 )
        time.sleep(1)
        #flash three times!
    GPIO.output(BlueT, 0)
    #State 3
    print("stage 3 \n")
    time.sleep(1)
    GPIO.output(RedT,1)
    GPIO.output(GreenP,1)
    time.sleep(1)

    # #list of all numbers for 7 segment
    seg7_list = [(A,B,C,F,G), (A,B,C,D,E,F,G), (A, B, C), (A,C,D,E,F,G), (A,C,D,F,G), (B,C,F,G),(A,B,C,D,G), (A,B,D,E,G),(B,C), (A,B,C,D,E,F) ]
    counter = 0
    for i in range(10):
        print("led light show \n")
        GPIO.output((A,B,C,D,E,F,G), 0)
        
        GPIO.output(seg7_list[i], 1)
        
        #State 4
        if(counter == 5): #when counter is 5 we are at 4
            print("stage 4 \n")
            time.sleep(.2)
            GPIO.output(RedT,0)
            GPIO.output(GreenP,0)
            time.sleep(.2)
            # GPIO.output(RedT, 1)
            # time.sleep(.2)
            for i in range(3):
                
                GPIO.output(BlueP, 0)
                time.sleep(.1)
                GPIO.output(BlueP, 1)
                time.sleep(.2)
            counter+=1
            continue

        #State 5
        if(counter == 9): 
            # dont sleep for a extra second if we already slept :)
            print("stage 5 \n")
            GPIO.output(BlueP, 0)
            GPIO.output(RedT, 0)
            GPIO.output(GreenT, 1)
            GPIO.output(RedP, 1)
            time.sleep(1)
            counter +=1
            continue
        print(counter)
        counter+=1
        time.sleep(1)
    GPIO.output((A,B,C,D,E,F,G), 0)






def turnAllOff():
    #turn all pins off

    GPIO.output(GreenT, 0)
    GPIO.output(BlueT,0)
    GPIO.output(RedT,0)
    GPIO.output(GreenP, 0)
    GPIO.output(BlueP,0)
    GPIO.output(RedP,0)
    GPIO.output(A,0)
    GPIO.output(B,0)
    GPIO.output(C,0)
    GPIO.output(D,0)
    GPIO.output(E,0)
    GPIO.output(F,0)
    GPIO.output(G,0)




def main():
    global RedP
    RedP = 4
    global RedT
    RedT = 17
    global BlueP 
    BlueP = 19
    global BlueT 
    BlueT = 27
    global GreenP 
    GreenP = 20
    global GreenT
    GreenT = 18
    global Input 
    Input = 21
    global A
    A = 6
    global B
    B = 23
    global C
    C= 13
    global D 
    D = 5
    global E 
    E = 24 
    global F
    F = 25
    global G 
    G = 12
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GreenT, GPIO.OUT)
    GPIO.setup(BlueT,GPIO.OUT)
    GPIO.setup(RedT,GPIO.OUT)
    GPIO.setup(GreenP, GPIO.OUT)
    GPIO.setup(BlueP,GPIO.OUT)
    GPIO.setup(RedP,GPIO.OUT)
    GPIO.setup(Input,GPIO.IN , pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.setup(E,GPIO.OUT)
    GPIO.setup(F,GPIO.OUT)
    GPIO.setup(G,GPIO.OUT)
    turnAllOff()
    # print("wait")
    # GPIO.output((A,B,C,D,E,F,G), 0)
    # time.sleep(2)
    while(1):
       # print("input ", GPIO.input(Input) , "\n")
        #waitPress = 0
        if(GPIO.input(Input)):
         #   time.sleep(1)

            # start = time.time()
            # time.sleep(20)
            # end = time.time()
            GPIO.output(GreenT, 0)
            waitPress = 0

            startStates()
            print("wait 7 seconds as 13 already passed \n")
            time.sleep(7) # 7 seconds till next press
            GPIO.output(GreenT, 1)
            GPIO.output(RedP, 0)

        else:
            GPIO.output(GreenT, 1)


if ( __name__ == "__main__"):
    counter = 0

    try:
        # here you put your main loop or block of code
        while counter < 9000000:
            # count up to 9000000 - takes ~20s
            main()
            counter += 1
        print ("Target reached: %d" % counter)

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