import json
import matplotlib.pyplot as plt
import numpy as np
import math
import copy

with open("../sim_logs/theta_logs_1.txt", 'r') as file:
    data = json.load(file)

data = data[10:]
begin_theta = 0
while (data[begin_theta][0] <= data[begin_theta + 3][0]):
    begin_theta += 1
data = data[begin_theta:-300]

null_time = data[0][1]
for i in range(len(data)):
    data[i][1] -= null_time

for i in range(len(data)):
    data[i][0] = (data[i][0] - data[-1][0]) / 1023 * 2 * math.pi 

time_real = []
theta_real = []

for i in data:
    theta_real.append(i[0])
    time_real.append(i[1])


def rp(x, k):
    tau = np.sign(x[1])
    return [x[1], -k[0] * math.sin(x[0]) - k[1] * tau - k[2] * x[1]]

def symp_euler(fun, start_cond, time_arr, k):
    c_cond = copy.copy(start_cond)
    out = np.array(c_cond)
    for i in range(len(time_arr) - 1):
        dt = (time_arr[i + 1] - time_arr[i])
        c_cond[1] += fun(c_cond, k)[1] * dt
        c_cond[0] += c_cond[1] * dt
        out = np.vstack((out, c_cond))
    return out 

time_k = 1000
time_theor = list(range(int(time_real[-1] / time_k)))

q0 = data[0][0]
t0 = data[0][1]

print(q0)

g = 9.8 * 10**(-6)
L = 0.25

k = [g / L, 0, 3*10**(-4)] 

theta_theor = symp_euler(rp, [q0, t0], time_theor, k)
theta_theor = theta_theor[:,0]

time_theor_graph = []
for i in time_theor:
    time_theor_graph.append(i * time_k)

to_out = []
for i in range(len(theta_theor)):
    to_out.append([theta_theor[i], time_theor_graph[i]])

with open('../graph_logs/theor_graph_data.txt', 'w') as file:
    json.dump(to_out, file)

plt.plot(time_theor_graph, theta_theor, label = "theor", color='black',
        linewidth=3)
#plt.title("Угол отклонения теоретического маятника")
plt.xlabel("Время, c", fontsize=22)
plt.ylabel("Отклонение, рад", fontsize=22)
plt.yticks(ticks=[-math.pi/6, -math.pi/12, 0, math.pi/12, math.pi/6],
           labels=["$-\\frac{\pi}{6}$", "$-\\frac{\pi}{12}$",  "0", 
                   "$\\frac{\pi}{12}$", "$\\frac{\pi}{6}$"],
           fontsize=22)
plt.xticks(ticks=np.arange(0, 3*10**7, 10**6),
           labels=np.arange(0, 30, 1),
           fontsize=22)
plt.grid(True)
#plt.legend()
plt.show()
