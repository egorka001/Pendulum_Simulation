from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
import copy
import math
import json

with open("../sim_logs/theta_night.txt", 'r') as file:
    data = json.load(file)

data = data[35:]
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

def norms(real, theor):
    sz = len(real)
    print(sz)
    l_2 = 0
    l_inf = abs(real[0] - theor[0])
    for i in range(sz):
        err = abs(real[i] - theor[i])
        if (err > l_inf):
            l_inf = err
        l_2 += err**2
    l_2 = math.sqrt(l_2)
    return (l_2, l_inf)

def l_norms(k, time_theor, real_out, temp, ltype):
    theta_theor = symp_euler(rp, [q0, t0], time_theor, k)
    theta_theor = theta_theor[:,0]

    theor_out = []
    for i in temp:
        theor_out.append(theta_theor[i])

    if(ltype):
        return norms(real_out, theor_out)[0]
    else:
        return norms(real_out, theor_out)[1]

time_k = 10000
time_theor = list(range(int(time_real[-1] / time_k)))

q0 = data[0][0]
t0 = data[0][1]
#k = [5.20344118e-03, 1.39553092e-05, 7.00949640e-07]
k = [5.21291531e-03, 1.42566350e-05, 2.02626362e-04]



real_dct = {}
for i in range(len(theta_real)):
    real_dct[int(time_real[i] / time_k)] = theta_real[i]

real_out = []
temp = []
for key in real_dct.keys():
    if key in time_theor:
        real_out.append(real_dct[key])
        temp.append(time_theor.index(key))

theta_theor = symp_euler(rp, [q0, t0], time_theor, k)
theta_theor = theta_theor[:,0]

time_theor_graph = []
for i in time_theor:
    time_theor_graph.append(i * time_k)

l2 = l_norms(k, time_theor, real_out, temp, 1)
linf = l_norms(k, time_theor, real_out, temp, 0)

print("k: ", k)
print("l_2: ", l2)
print("l_inf: ", linf)
print(q0)

to_out = {"k": list(k), "l2": l2, "linf": linf, "real": [], "theor": []}
for i in range(len(theta_real)):
    to_out["real"].append([theta_real[i], time_real[i]])

for i in range(len(theta_theor)):
    to_out["theor"].append([theta_theor[i], time_theor_graph[i]])

#with open('../graph_logs/real_theor_second_data.txt', 'w') as file:
#    json.dump(to_out, file)

plt.plot(time_real, theta_real, label = "Реальный маятник", color='blue',
        linewidth = 2)
plt.plot(time_theor_graph, theta_theor, label = "Теоретический маятник",
         color = 'orange', linewidth = 2)
#plt.title("Угол отклонения реального маятника и теоретического")
plt.xlabel("Время, с", fontsize=22)
plt.ylabel("Отклонение, рад", fontsize=22)
plt.yticks(ticks=[-math.pi/4, -math.pi/6, -math.pi/12, 0, 
                  math.pi/12, math.pi/6, math.pi/4],
           labels=["$-\\frac{\pi}{4}$", "$-\\frac{\pi}{6}$", 
                  "$-\\frac{\pi}{12}$",  "0", 
                   "$\\frac{\pi}{12}$", "$\\frac{\pi}{6}$", 
                   "$\\frac{\pi}{4}$"],
           fontsize=22)
plt.xticks(ticks=np.arange(0, 3.2*10**7, 2*10**6),
           labels=np.arange(0, 32, 2), fontsize=22)
plt.grid(True)
plt.legend(fontsize=22)
plt.show()
