import board
import busio
import adafruit_mpu6050
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math


# perf_counter is more precise than time() for dt calculation
from time import sleep, time

i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
G = 9.8
MAG_OFFSET = 10.348987

def takemeasurements():
    a_x, a_y, a_z = mpu.acceleration
    # print("Acceleration: X: %.2f, Y: %.2f, Z: %.2f m/s^2" %(a_x, a_y, a_z))
    # print("Gyro X: %.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    mag = math.sqrt(a_x*a_x + a_y*a_y + a_z*a_z) - MAG_OFFSET
    # print("Magnitude: {:f}".format(mag))
    return [a_x, a_y, a_z, mag]

def step_detector():
    x_accel = []
    y_accel = []
    z_accel = []
    mags = []
    timestamps = []
    start_timestamp = time()


    for i in range(500):
        
        measurements = takemeasurements()
        
        timestamp = time() - start_timestamp
        timestamps.append(timestamp)
        x_accel.append(measurements[0])
        y_accel.append(measurements[1])
        z_accel.append(measurements[2])
        mags.append(measurements[3])

    
    ax1.clear()
    ax1.plot(timestamps, x_accel, label="x_acceleration")
    ax1.plot(timestamps, y_accel, label="y_acceleration")
    ax1.plot(timestamps, z_accel, label="z_acceleration")
    ax1.plot(timestamps, mags, label = "magnitude")
    plt.legend()
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    return int(max(mags) > 2)

if __name__ == '__main__':
    step_counter = 0
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    while True:
        step_counter += step_detector()
        print('\x1b[2J')
        print('step counter:', step_counter)
        sleep(0.5) 
