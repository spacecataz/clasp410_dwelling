#!/usr/bin/env python3

'''
This file solves the N-Layer atmosphere problem for Lab 01 and all subparts.

TO REPRODUCE THE VALUES AND PLOTS IN MY REPORT, DO THIS:
<tbd>
'''

import numpy as np
import matplotlib.pyplot as plt

# Physical Constants
sigma = 5.67E-8  # Units: W/m2/K−4

def n_layer_atmos(nlayers, epsilon=1, albedo=0.33, s0=1350, debug=False):
    '''
    docstring!

    debug : bool, defaults to False
        Turn on debug print outs.
    '''

    # Create array of coefficients, an N+1xN+1 array:
    A = np.zeros([nlayers+1, nlayers+1])
    b = np.zeros(nlayers+1)

    # Populate based on our model:
    for i in range(nlayers+1):
        for j in range(nlayers+1):
            if i == j:  # Handle diagonal.
                A[i, j] = -2 + 1 * (j == 0)
            else:
                A[i, j] = epsilon**(i>0) * (1-epsilon)**(np.abs(j - i) -1 )
    if debug:
        print(A)

    b[0] = -0.25 * s0 * (1-albedo)

    # Invert matrix:
    Ainv = np.linalg.inv(A)
    # Get solution:
    fluxes = np.matmul(Ainv, b)  # Note our use of matrix multiplication

    # Turn fluxes into temperatures.
    # Return temperatures to caller.
    # VERIFY!

def time_logic():
    '''Try to answer the question about how slow "if" statements are...'''

    import datetime as dt

    now = dt.datetime.now()
    n_layer_atmos(10000)
    print(f'That took {(dt.datetime.now()-now).total_seconds()}s')