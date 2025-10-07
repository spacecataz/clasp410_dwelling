#!/usr/bin/env python3

'''
Tools and methods for completing Lab 3 which is the best lab.
'''

import numpy as np
import matplotlib.pyplot as plt


def solve_heat(xstop=1, tstop=0.2, dx=0.2, dt=0.02, c2=1):
    '''
    A function for solving the heat equation

    Parameters
    ----------
    Fill this out don't forget. :P
    c2 : float
        c^2, the square of the diffusion coefficient.

    Returns
    -------
    x, t : 1D Numpy arrays
        Space and time values, respectively.
    U : Numpy array
        The solution of the heat equation, size is nSpace x nTime
    '''
    # Get grid sizes:
    N = int(tstop / dt)
    M = int(xstop / dx)

    # Set up space and time grid:
    t = np.linspace(0, tstop, N)
    x = np.linspace(0, xstop, M)

    # Create solution matrix; set initial conditions
    U = np.zeros([M, N])
    U[:, 0] = 4*x - 4*x**2

    # Get our "r" coeff:
    r = c2 * (dt/dx**2)

    # Solve our equation!
    for j in range(N-1):
        U[1:M-1, j+1] = (1-2*r) * U[1:M-1, j] + r*(U[2:M, j] + U[:M-2, j])

    # Return our pretty solution to the caller:
    return t, x, U