import matplotlib.pyplot as plt
import numpy as np
import math
import json

with open("../sim_logs/theta_logs_1.txt", 'r') as file:
    data = json.load(file)

data = data[10:]
curr_theta = 0
while (data[curr_theta][0] <= data[curr_theta + 3][0]):
    curr_theta += 1

data = data[curr_theta:]

null_time = data[0][1]
for i in range(len(data)):
    data[i][1] -= null_time

for i in range(len(data)):
    data[i][0] = (data[i][0] - data[-1][0]) / 1023 * 2 * math.pi 

time = []
theta_real = []

for i in data:
    theta_real.append(i[0])
    time.append(i[1])

print(theta_real[0])

to_out = []
for i in range(len(theta_real)):
    to_out.append([theta_real[i], time[i]])

with open('../graph_logs/real_graph_data.txt', 'w') as file:
    json.dump(to_out, file)

plt.plot(time, theta_real, label = "real", color = 'black',
        linewidth=3)
#plt.title("Угол отклонения реального маятника")
plt.xlabel("Время, c", fontsize=22)
plt.ylabel("Отклонение, рад", fontsize=22)
plt.yticks(ticks=[-math.pi/6, -math.pi/12, 0, math.pi/12, math.pi/6],
           labels=["$-\\frac{\pi}{6}$", "$-\\frac{\pi}{12}$",  "0", 
                   "$\\frac{\pi}{12}$", "$\\frac{\pi}{6}$"],
           fontsize=22)
plt.xticks(ticks=np.arange(0, 3*10**7, 10**6),
           labels=np.arange(0, 30, 1), fontsize = 22)
plt.grid(True)
plt.show()
