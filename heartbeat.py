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
fig, (ax) = plt.subplots(1,1)
line,  = ax.plot(np.random.randn(100))
plt.show(block = False)

PData= PlotData(500)
ax.set_ylim(320,350)

# plot parameters
print ('plotting data...')
# open serial port
strPort='com3'
ser = serial.Serial(strPort, 9600)
ser.flush()

start = time.time()
count = 0
counta = 0

while True:
    arr = 0
    for ii in range(10):
        try:
            data = float(ser.readline())
            PData.add(time.time() - start, data)
            arr += data
            avg = arr/10
        except:
            pass
    
    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    
    if PData.axis_y[0] > avg:
        counta = 1
    if PData.axis_y[0] < avg and counta == 1:
        count += 1

    beat = int(count/PData.axis_x[0] *60)/5
    
    plt.title(beat)
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    