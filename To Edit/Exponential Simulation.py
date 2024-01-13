import numpy as np
import scipy
import matplotlib.pyplot as plt

def exp(x, a, b, c):
    return a + b * np.exp(-c*x)

# logarithmic spacing fit parameters
alog = []
blog = []
clog = []

# even spacing fit parameters
aspace = []
bspace = []
cspace = []

for i in range(50000):
    # initialization for parameters
    a = 0
    b = 1
    c = 1
    d = 10 # ***This is divided from the noise for scaling***
    n = 500
    noise = np.random.rand(n)/d
    #logarithmic x value spacing
    xlog = np.logspace(0, np.log10(6), n)
    ylog = a + b*np.exp(-c*xlog) + noise
    par, cov = scipy.optimize.curve_fit(exp, xlog, ylog, p0=[0, 1, 1])
    alog.append(par[0])
    blog.append(par[1])
    clog.append(par[2])
    #even x value spacing
    xspace = np.linspace(1, 6, n)
    yspace = a + b*np.exp(-c*xspace) + noise
    par, cov = scipy.optimize.curve_fit(exp, xspace, yspace, p0=[0, 1, 1])
    aspace.append(par[0])
    bspace.append(par[1])
    cspace.append(par[2])
# print('logarithmic spacing', np.mean(alog), abs(np.mean(blog)-1), abs(np.mean(clog)-1))
# print('even spacing', np.mean(aspace), abs(np.mean(bspace)-1), abs(np.mean(cspace)-1))

# print('logarithmic spacing', np.std(alog), abs(np.std(blog)-1), abs(np.std(clog)-1))
# print('even spacing', np.std(aspace), abs(np.std(bspace)-1), abs(np.std(cspace)-1))

print('even spacing / logarithmic spacing', np.mean(aspace) / np.mean(alog), abs(np.mean(bspace)-1) / abs(np.mean(blog)-1), abs(np.mean(cspace)-1) / abs(np.mean(clog)-1))
