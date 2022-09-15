
from termios import VEOL
import board
import busio
import RPi.GPIO as GPIO
import adafruit_mcp4725
import time
import math
def sine(dac,voltage,freq):
    t = 0
    denom = 50
    print(voltage , "\n")
    dac.normalized_value = voltage
    while(True):
    #     if( voltage  == 0.4909090909090909 ):
    #             dac.normalized_value = 0.4909090909090909
    #             t += 0.05
    #             time.sleep(freq/denom)
    # # elif ( voltage == 1 ):
    #     #    while True:
    #     #        voltageInc = (math.sin(6.2832*t))/5.5
    #     #        debug = dac.normalized_value + voltageInc
    #     #        print(dac.normalized_value, "\n")
    #     #        if(debug < 0.4909):
    #     #           dac.normalized_value = 0.4909
    #     #        else:
    #     #            dac.normalized_value += voltageInc
    #     #        t += 0.05
    #     #        time.sleep(freq/denom)
    #     if(GPIO.input(inputPress)):
    #         dac.normalized_value = 0
    #         break
        # else:
            # voltageInc = (0.1*(1.0+0.5*math.sin(6.2832*t)))
                voltageInc = (math.sin(6.2832*t))/5.5
                debug = dac.normalized_value + voltageInc
                print(debug, "\n")

                if(debug < 0.4909):
                    dac.normalized_value = 0.4909
                elif(debug > 1):
                    dac.normalized_value = 1
                else:
                    dac.normalized_value += voltageInc
                t += 0.05
                time.sleep(freq/denom)
    

def triangle(dac,voltage, freq):
    #frequency[2]
    #ideal base: 100 ms/div
    #range: 5 V/div
    denom = 50
    voltageInc = voltage/denom
    dac.normalized_value = 0
    while(True):
        for i in range(denom):
            dac.normalized_value += voltageInc
            print(dac.normalized_value , "\n")
            time.sleep(freq/denom)
        for i  in range(denom):
            debug = dac.normalized_value - voltageInc
            if (debug < 0 ):
                dac.normalized_value = 0
            else:
                dac.normalized_value -= voltageInc
            print(dac.normalized_value , "\n")
            time.sleep(freq/denom)
        if(GPIO.input(inputPress)):
                dac.normalized_value = 0
                break
   
def square(dac,voltage,freq):
    while(True):
     #   voltage = 2048*(1.0+0.5*math.sin(6.2832*t))
        dac.normalized_value = voltage

        time.sleep(freq/2)
        dac.normalized_value = 0
        time.sleep(freq/2)
        if(GPIO.input(inputPress)):
            dac.normalized_value = 0
            break
        

def main():
    GPIO.setmode(GPIO.BCM) # set the gpio pins
    global pressButton
    pressButton = 24
    global inputPress
    inputPress = 20
    # global clock
    # clock = 13
    # global voltage
    # voltage = 6
    global frequency
    frequency = [0.1 , 0.25 , 0.02]
    global voltage 
    voltage = [0.4909090909090909 , 0.7454545 , 1]
    GPIO.setup(pressButton, GPIO.OUT)
    # GPIO.setup((clock,voltage), GPIO.OUT)
    GPIO.setup(inputPress , GPIO.IN )


    #pickType(w,v,f)
    while(1):
         if(GPIO.input(inputPress)):
             pickType()
         GPIO.output(pressButton,1)
        
# Initialize I2C bus.
# def module1square():
#     print(" running \n ")
#     for i in range(900000000):
#         GPIO.output((clock, voltage), 1)
#         time.sleep(0.000005)
#         GPIO.output((clock, voltage), 0)
#         time.sleep(0.000005)


def pickType():
    while(1):
        print("Waveform Generator:")
        print("\n")
        print("Enter the waveform type (tri, sine, sq): ")
        w = input()
        print("Input a frequency")
        f = int(input())
        print("Enter the voltage (0 [2.7 V], 1[3.3 V], 2 [5.5 V]): ")
        v = int(input())
        i2c = busio.I2C(board.SCL, board.SDA)
        dac = adafruit_mcp4725.MCP4725(i2c)
        # triangle(dac , voltage[0] , frequency[0])
        #triangle(dac,voltage[2],frequency[2])

        if(v == 0):
            v = voltage[0]
        if(v == 1):
            v = voltage[1]
        if(v == 2):
            v = voltage[2]



        if(w == "sine"):
            sine(dac, v, f)
        if(w == "tri"):
            triangle(dac, v, f)
        if(w == "sq"):
            square(dac, v, f)

    


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
        i2c = busio.I2C(board.SCL, board.SDA)
        dac = adafruit_mcp4725.MCP4725(i2c)
        dac.normalized_value = 0