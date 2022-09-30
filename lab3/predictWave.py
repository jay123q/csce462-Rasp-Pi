from genericpath import sameopenfile
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep, time
from math import floor, ceil
import numpy as np
import scipy as sy
import scipy.fftpack as syfp
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

#THIS DOES NOT WORK ON THE PI 4
def raw_data( channel ):
    start_time = time()
    timeList = []
    sampleVoltage = []
    for i in range(2000):
        sampleVoltage.append(channel.voltage)
        timeList.append(time() - start_time)
    sampleRate = 1/(np.mean(np.diff(timeList)))
    purifiedVoltage = []
    newTime=[]
    oldBit = 0
    firstInstance = False
    for i in range(len(sampleVoltage)):
        # start counting ratio at right input
        if( oldBit < sampleVoltage[i] -1):
            firstInstance = True
        if (firstInstance):
            purifiedVoltage.append(sampleVoltage[i])
            newTime.append(timeList[i])
    
    #print(purifiedVoltage, "/n")
    return (newTime,purifiedVoltage,sampleRate)
def find_ratio(time, voltage):
    H = 0
    L = 0
    # take the exact point and partion based off of the high and low
    low = max(voltage)/2
    for i in range(len(voltage)):
        if(voltage[i] < low):
            L+=1
        else:
            H+=1
    #return our ratio 25H, 67L  10 hz sine  to 10H,13L high 50 hz sine L/(H+L)
    #return our ratio 51H,56L  10 hz sq to 12H,11L 50 hz sq L/(H+L)
    #return our ratio  42H, 73L 10 hz tri to 8 hz, 14L tri L/(H+L)
    ratioL = L/(H+L)
    ratioH = H/(H+L)
    ratioLoH = L/H
    return ratioL,ratioH, ratioLoH
def find_waves(x: list, y: list ,  frequency):
    ratioL,ratioH,ratioLoH = find_ratio(x,y)
    print(ratioL, " ratio  Low \n")
    print(ratioLoH, "ratio low\high \n")
    # the idea is that a sin wave has a different low to high ratio than a square and a tri wave
    
    if( ratioL < 0.52 and ratioL > 0.47):
        return "square"
    print("average",sum(y)/len(y))
    if( 0.580 < ratioL and ratioL < 0.6931 and 1.375 < ratioLoH and ratioLoH < 2.3):
     #changed ratio Loh from 1.43
        #This catches the input of tri of 5 for all, the average is btwn 1.09 and 1.4 of all votls

     #if(max(y) <= 3.29):
     
     average = sum(y)/len(y)
     if( average < 1.4 and average > 1.25):
             return "sin"
     elif(average > 1.09):
             return "tri"
     return "sin"



    else:
        #this hits all tri at 3 volts this was found with extensive testing
        return "tri"

        

def find_freq(x: list, y: list):
    time = np.array(x)
    data = np.array(y)

    # Do FFT analysis of array
    fastTransform = np.fft.fft(data)

    freqs = syfp.fftfreq(
        len(data),
        np.mean(np.diff(time))).tolist()[1:401]
    # Convert Discrete Fourier Transform to amplitude log10(|H(s)|)
    freqs_amp = np.log10(abs(fastTransform)).tolist()[1:401]

    # Find the frequency with peak amplitude
    freq = freqs[freqs_amp.index(max(freqs_amp))]

    # Plot functions
    dydt = np.diff(data)/np.diff(time)
    d2ydt2 = np.diff(dydt)/np.diff(time[1::])
    #print("dydt max: ", max(dydt))
    print("d2ydt2 abs add: ",abs(max(d2ydt2)) + abs(min(d2ydt2)))
    print("---------------------")
    #print("dy2dt2 max: ", max(d2ydt2))
    #print("dy2dt2 min: ", min(d2ydt2))
    fig, axs = plt.subplots(4, figsize=(8, 6), dpi=80)
    axs[0].plot(time, data)  # Original wave
    axs[1].plot(time[1::], dydt)  # First derivative
    axs[2].plot(time[2::], d2ydt2)  # Second derivative
    axs[3].plot(syfp.fftfreq(len(data), np.mean(np.diff(time))), np.log10(
        np.abs(fastTransform)), '.')  # Frequency domain

    # zoom into see what's going on at the peak of frequency domain

    plt.xlim(1, 50)
    plt.show()
    plt.savefig('current_wave.png')
    plt.clf()
    

    return freq*1.01


def main():
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D22)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    chan0 = AnalogIn(mcp, MCP.P0)
    global inputPin
    inputPin = 26
    GPIO.setmode(GPIO.BCM)
    #, pull_up_down=GPIO.PUD_DOWN
    GPIO.setup(inputPin, GPIO.IN)
    while(True):
        timeList,sampleVoltage,sampleRate = raw_data( chan0 )

        frequency = find_freq(timeList , sampleVoltage)
        waveGuess = find_waves(timeList, sampleVoltage,frequency)
        output = "The sample rate is {} \n The waveform is {} \n The frequency is {} ".format( sampleRate , waveGuess, frequency )
        print(output)   
        sleep(1)

if ( __name__ == "__main__"):
    counter = 0

    try:
        # here you put your main loop or block of code
        while counter < 100:
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
        print()