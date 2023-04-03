import serial
import json
import matplotlib.pyplot as plt
from datetime import datetime as dt
import math
import numpy as np

def to_microsec(curr_time):
    out = curr_time.minute * 60
    out += curr_time.second
    out *= 10**6
    out += curr_time.microsecond
    return out

s = serial.Serial('/dev/ttyACM0')

out = 0
full_data = []

null_time = to_microsec(dt.now())

try:
    while True:
        res = s.read()
        if res >= b'0' and res <= b'9':
            out = out * 10 + int(res)   
        elif res == b'\r':
            curr_time = to_microsec(dt.now())
            full_data.append([out, curr_time - null_time])
            out = 0
except KeyboardInterrupt:
    pass

for i in full_data:
    if i[0] > 1023:
        full_data.remove(i)

theta = []
time = []

for i in full_data:
    theta.append(i[0])
    time.append(i[1])

plt.plot(time, theta, label='с шумами', color = 'blue', linewidth=2)

flag = 0

while True:
    for i in range(1, len(full_data) - 1):
        if full_data[i-1][0] == full_data[i][0] + 1 == full_data[i + 1][0]:
            full_data[i][0] = full_data[i - 1][0]
            flag = 0
        if full_data[i-1][0] == full_data[i][0] - 1 == full_data[i + 1][0]:
            full_data[i][0] = full_data[i - 1][0]
            flag = 0
    if flag:
        break
    flag = 1

theta = []
time = []

for i in full_data:
    theta.append(i[0])
    time.append(i[1])

plt.plot(time, theta, label='без шумов', color='orange', linewidth=2)

with open('../sim_logs/theta_night.txt', 'w') as file:
    json.dump(full_data, file)

plt.xlabel("Время, с", fontsize=22)
plt.ylabel("Отклонение, рад", fontsize=22)

plt.yticks(ticks=[-math.pi/6, -math.pi/12, 0, math.pi/12, math.pi/6],
           labels=["$-\\frac{\pi}{6}$", "$-\\frac{\pi}{12}$",  "0", 
                   "$\\frac{\pi}{12}$", "$\\frac{\pi}{6}$"],
           fontsize=22)

plt.xticks(ticks=np.arange(0, 3*10**7, 10**6),
           labels=np.arange(0, 60, 2), fontsize=22)

plt.legend(fontsize=22)
plt.grid(True)
plt.show()
        

