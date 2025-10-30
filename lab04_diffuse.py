#!/usr/bin/env python3

'''
Tools and methods for completing Lab 3 which is the best lab.
this is the first time ive acc had fun with homework wow :D 


im gonna get roasted for being a nerd lollllllllllllllll
'''

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

# Solution to problem 10.3 from fink/matthews
sol10p3 = [[0.000000, 0.640000, 0.960000, 0.960000, 0.640000, 0.000000],
           [0.000000, 0.480000, 0.800000, 0.800000, 0.480000, 0.000000],
           [0.000000, 0.400000, 0.640000, 0.640000, 0.400000, 0.000000],
           [0.000000, 0.320000, 0.520000, 0.520000, 0.320000, 0.000000],
           [0.000000, 0.260000, 0.420000, 0.420000, 0.260000, 0.000000],
           [0.000000, 0.210000, 0.340000, 0.340000, 0.210000, 0.000000],
           [0.000000, 0.170000, 0.275000, 0.275000, 0.170000, 0.000000],
           [0.000000, 0.137500, 0.222500, 0.222500, 0.137500, 0.000000],
           [0.000000, 0.111250, 0.180000, 0.180000, 0.111250, 0.000000],
           [0.000000, 0.090000, 0.145625, 0.145625, 0.090000, 0.000000],
           [0.000000, 0.072812, 0.117813, 0.117813, 0.072812, 0.000000]]
sol10p3 = np.array(sol10p3).transpose()


def solve_heat(xstop=1, tstop=0.2, dx=0.2, dt=0.02, c2=1, lowerbound=0,
               upperbound=0):
    '''
    A function for solving the heat equation.
    Apply Neumann boundary conditions such that dU/dx = 0.

    Parameters
    ----------
    Fill this out don't forget. :P

     ------------- fill out your dern docstring dan, you forgot hehehehehehehe 
     remember the meme: 'mfw Dan forgets to fill out his docstring' :)
    c2 : float
        c^2, the square of the diffusion coefficient.
    Parameters
    ----------
    initial : func
        A function of position; sets the intial conditions at t=`trange[0]`
        Must accept an array of positions and return temperature at those
        positions as an equally sized array.
    upperbound, lowerbound : None, scalar, or func
        Set the lower and upper boundary conditions. If either is set to
        None, then Neumann boundary condtions are used and the boundary value
        is set to be equal to its neighbor, producing zero gradient.
        Otherwise, Dirichlet conditions are used and either a scalar constant
        is provided or a function should be provided that accepts time and
        returns a value.

    Returns
    -------
    x, t : 1D Numpy arrays
        Space and time values, respectively.
    U : Numpy array
        The solution of the heat equation, size is nSpace x nTime
    '''

    # Check our stability criterion:
    dt_max = dx**2 / (2*c2) / dt
    if dt > dt_max:
        raise ValueError(f'DANGER: dt={dt} > dt_max={dt_max}.')

    # Get grid sizes (plus one to include "0" as well.)
    N = int(tstop / dt) + 1
    M = int(xstop / dx) + 1

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

        # Apply boundary conditions:
        # Lower boundary
        if lowerbound is None:  # Neumann
            U[0, j+1] = U[1, j+1]
        elif callable(lowerbound):  # Dirichlet/constant
            U[0, j+1] = lowerbound(t[j+1])
        else:
            U[0, j+1] = lowerbound

        # Upper boundary
        if upperbound is None:  # Neumann
            U[-1, j+1] = U[-2, j+1]
        elif callable(upperbound):  # Dirichlet/constant
            U[-1, j+1] = upperbound(t[j+1])
        else:
            U[-1, j+1] = upperbound


    # Return our pretty solution to the caller:
    return t, x, U


def plot_heatsolve(t, x, U, title=None, **kwargs):
    '''
    Plot the 2D solution for the `solve_heat` function.

    Extra kwargs handed to pcolor.

    Paramters
    ---------
    t, x : 1D Numpy arrays
        Space and time values, respectively.
    U : Numpy array
        The solution of the heat equation, size is nSpace x nTime
    title : str, default is None
        Set title of figure.

    Returns
    -------
    fig, ax : Matplotlib figure & axes objects
        The figure and axes of the plot.

    cbar : Matplotlib color bar object
        The color bar on the final plot
    '''

    # Check our kwargs for defaults:
    # Set default cmap to hot
    if 'cmap' not in kwargs:
        kwargs['cmap'] = 'hot'

    # Create and configure figure & axes:
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    # Add contour to our axes:
    contour = ax.pcolor(t, x, U, **kwargs)
    colorbar = plt.colorbar(contour) # change cbar to colorbar so i really know whats going on

    # Add labels to stuff!
    colorbar.set_label(r'Temperature ($^{\circ}C$)') # repeat line 147 
    ax.set_xlabel('Time ($s$)')
    ax.set_ylabel('Position ($m$)')
    ax.set_title(title)
    # ------------------------------------------------------------------------------------------------------
    # here is ALEX's commit for lab 3-4 (whatever you wanna call it lolololol)
    # add graph for the depth profiles as an additional extension for this lab.
    # i added literally other things to my own lab in order to get that secondary plot to come up on both axes.
    # if we wanted the profile of a city, you can add in a solver in the beginning of the code in order
    # to plot both the heatmap and the graph profile for said city.
    # docstrings look very healthy and detailed as if i know exactly what's going on. i love it.





    # fin.
    # ------------------------------------------------------------------------------------------------------
    fig.tight_layout()

    return fig, ax, cbar