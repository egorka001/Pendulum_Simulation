import serial
import json
import matplotlib.pyplot as plt
from datetime import datetime as dt

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

with open('../sim_logs/theta_logs.txt', 'w') as file:
    json.dump(full_data, file)

theta = []
time = []

for i in full_data:
    theta.append(i[0])
    time.append(i[1])

plt.plot(time, theta)
plt.grid(True)
plt.show()
        

