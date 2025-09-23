#!/usr/bin/env python3

'''
Series of simple examples for Lecture 2 about turkeys
'''

import numpy as np
import matplotlib.pyplot as plt

dx = 0.25
x = np.arange(0, 6 * np.pi, dx)
sinx = np.sin(x)
cosx = np.cos(x)  # Analytical solution!

# The hard way:
# fwd_diff = np.zeros(x.size - 1)
# for i in range(x.size - 1):
#     fwd_diff[i] = x[i+1] - x[i]

# The easy way:
fwd_diff = (sinx[1:] - sinx[:-1]) / dx
bkd_diff = (sinx[1:] - sinx[:-1]) / dx
cnt_diff = (sinx[2:] - sinx[:-2]) / (2*dx)

plt.plot(x, cosx, label=r'Analytical Derivative of $\sin{x}$')
plt.plot(x[:-1], fwd_diff, label='Forward Diff Approx')
plt.plot(x[1:], bkd_diff, label='Backward Diff Approx')
plt.plot(x[1:-1], cnt_diff, label='Central Diff Approx')
plt.legend(loc='best')

# Our dx values:
dxs = np.array([2**-n for n in range(20)])
err_fwd, err_cnt = [], []

for dx in dxs:
    x = np.arange(0, 2.5 * np.pi, dx)
    sinx = np.sin(x)

    fwd_diff = (sinx[1:] - sinx[:-1]) / dx
    cnt_diff = (sinx[2:] - sinx[:-2]) / (2*dx)

    err_fwd.append(np.abs(fwd_diff[-1] - np.cos(x[-1])))
    err_cnt.append(np.abs(cnt_diff[-1] - np.cos(x[-2])))

fig, ax = plt.subplots(1, 1)
ax.loglog(dxs, err_fwd, '.', label='Foward Diff')
ax.loglog(dxs, err_cnt, '.', label='Central Diff')
ax.set_xlabel(r'$\Delta x$')
ax.set_ylabel('Error')
ax.legend(loc='best')