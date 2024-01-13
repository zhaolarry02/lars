import scipy.optimize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# df = pd.read_csv("C:\\Users\\lzvio\\triplet_data.txt", header=None)

f = open("C:\\Users\\lzvio\\triplet_data5.txt", "r")
data = f.read()
d = data.split('\n', )
f.close()
y = [float(i) for i in d]

def exp(x, m, a, b):
    return (a * np.exp(np.array([-i for i in x]) * m) + b)

x = range(0,2046)
y = np.array([item-1510 for item in y])

# print(y)

plt.plot(x, y, label='Mean Waveform minus Pedestal');
plt.yscale("log")

par, cov = scipy.optimize.curve_fit(exp, x[600:1300], y[600:1300], p0=[0.00475215556, 6.06369377*10**2, 0.823153580], maxfev=100000)
plt.plot(x[600:1300], exp(x[600:1300], *par), label='Curve Fit, Lifetime = '+str(round(1/par[0]*6.6667, 2))+' ns')
plt.yscale("log")

plt.title('Triplet Lifetime Ch 5')
plt.xlabel('SSP Time Tick (6.667 ns / Tick)')
plt.ylabel('Waveform Signal minus Pedestal')
plt.legend()
plt.show()

print(par, 'Triplet Lifetime=', 1/par[0]*6.6667)

# Ch 1: 1402.879 ns
# Ch 4: 1398.364 ns
# Ch 5: 
# Ch 6: 1657.21 ns