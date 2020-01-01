import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal

#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)


#initial
fig, (ax2,ax3) = plt.subplots(2,1)
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
plt.show(block = False)

PData= PlotData(500)
ax2.set_ylim(0,1000)
ax3.set_ylim(-20,20)

# plot parameters
print ('plotting data...')
# open serial port
strPort='com3'
ser = serial.Serial(strPort, 9600)
ser.flush()

start = time.time()

while True:
    for ii in range(10):
        try:
            data = float(ser.readline())
            PData.add(time.time() - start, data)
        except:
            pass
    
    fs = 250
    f = (PData.axis_x[0]*fs)
    ecgf = np.fft.fft(PData.axis_y)
    ecg_max = np.max(PData.axis_y)
    
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax3.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(abs(ecgf))
    line3.set_xdata(PData.axis_x)
    line3.set_ydata(np.angle(ecgf))
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    