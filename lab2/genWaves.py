

import board
import busio
import RPi.GPIO as GPIO
import adafruit_mcp4725
import time
import math

def sine(dac,voltage,freq):
    # if voltage not in range(0,2049):
    #     print("REEEEEEEEEEEEEEEEEEEEE \n")
    #     return 0
    
    t = 0
    # denom = 50
    t_step = 0.05
    votageMax = voltage
    dac.raw_value = 1 # set to the minimum output of 2.7 
    maxVoltage = voltage
    while(True):
                voltageInc = voltage*math.sin(1.05*((1/1.45)*freq/34)*6.2832*t)
                print(voltageInc)
                if(voltageInc > votageMax):
                    dac.raw_value=4095
                elif(voltageInc < 1):
                    dac.raw_value=1
                else:
                    dac.raw_value=int(voltageInc)
                t += t_step
                time.sleep(0.0005)
                if(GPIO.input(inputPress)):
                    dac.raw_value = 0
                    break
    

def triangle(dac,voltage, freq):
    #frequency[2]
    #ideal base: 100 ms/div
    #range: 5 V/div
    dac.raw_value = 0
    while(True):
        if(GPIO.input(inputPress)):
            dac.raw_value = 0
            break
        # print(int((20/27)*1.001*voltage/(1/(2*freq)*1000)))
        print(voltage)
        for i in range(0 , voltage , int((20/32.5)*1.001*voltage/(1/(2*freq)*1000))):
            print(i , "RAMP UP")
            dac.raw_value = i      
        for i in range(0 , voltage , int((20/32.5)*1.001*voltage/(1/(2*freq)*1000))):
             print(i , "RAMP DOWN")
             dac.raw_value = voltage-i
   
def square(dac,voltage,freq):

    while(True):
     #   voltage = 2048*(1.0+0.5*math.sin(6.2832*t))
        dac.raw_value = voltage
        time.sleep(1/(2*freq))
        dac.raw_value = 0
        time.sleep(1/(2*freq))
        if(GPIO.input(inputPress)):
            dac.raw_value = 0
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
    frequency = 0
    # frequency = [0.1 , 0.25 , 0.02]
    global voltage 
    voltage = 0
    # voltage = [0.4909090909090909 , 0.7454545 , 1]
    GPIO.setup(pressButton, GPIO.OUT)
    # GPIO.setup((clock,voltage), GPIO.OUT)
    GPIO.setup(inputPress , GPIO.IN )


    #pickType(w,v,f)
    while(1):
         if(GPIO.input(inputPress)):
             pickType()
         GPIO.output(pressButton,1)


def pickType():
    while(1):
        print("Waveform Generator:")
        print("\n")
        print("Enter the waveform type (tri, sine, sq): ")
        w = input()
        print("Input a frequency")
        f = int(input())
        print("input a voltage 1-4096")
        v = int(input())

        i2c = busio.I2C(board.SCL, board.SDA)
        dac = adafruit_mcp4725.MCP4725(i2c)
        # triangle(dac , voltage[0] , frequency[0])
        #triangle(dac,voltage[2],frequency[2])
        dac.raw_value = 1
        print(dac.normalized_value)
        if(w == "sine"):
            sine(dac, v, f)
           #print(1)
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
        dac.raw_value = 0