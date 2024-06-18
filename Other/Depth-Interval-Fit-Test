import numpy as np
import scipy
import matplotlib.pyplot as plt

def exp(x, a, b, c):
    return a + b * np.exp(-c*x)

def logvslinxfit(a, b, c):
    # logarithmic x value fit parameters
    alog = []
    blog = []
    clog = []

    # linear x values fit parameters
    alin = []
    blin = []
    clin = []

    for i in range(100000):
        # initialization for parameters
        d = 10 # divided from noise for scaling
        n = 12
        noise = np.random.rand(n)/d

        # logarithmic x value spacing
        xlog = np.logspace(0, np.log10(60), n)
        ylog = a + b * np.exp(-c*xlog) + noise # exp(xlog, a, b, c) + noise
        par, cov = scipy.optimize.curve_fit(exp, xlog, ylog, p0=[a, b, c])
        alog.append(par[0])
        blog.append(par[1])
        clog.append(par[2])

        # linear x value spacing
        xlin = np.linspace(1, 60, n)
        ylin = a + b*np.exp(-c*xlin) + noise
        par, cov = scipy.optimize.curve_fit(exp, xlin, ylin, p0=[a, b, c])
        alin.append(par[0])
        blin.append(par[1])
        clin.append(par[2])
    print('logarithmic spacing fit parameter difference: a=', abs(np.mean(alog)-a), 'b=', abs(np.mean(blog)-b), 'c=', abs(np.mean(clog)-c))
    print('even spacing fit parameter difference: a=', abs(np.mean(alin)-a), 'b=', abs(np.mean(blin)-b), 'c=', abs(np.mean(clin)-c))

    print('logarithmic spacing fit parameter stdev: a=', np.std(alog), 'b=', np.std(blog), 'c=', np.std(clog))
    print('even spacing fit parameter stdev: a=', np.std(alin), 'b=', np.std(blin), 'c=', np.std(clin))

    print('even spacing fit parameter difference / logarithmic spacing fit parameter difference: a=', abs(np.mean(alin)-a) / abs(np.mean(alog)-a), 'b=', abs(np.mean(blin)-b) / abs(np.mean(blog)-b), 'c=', abs(np.mean(clin)-c) / abs(np.mean(clog)-c))

logvslinxfit(10, 10, 0.1)
