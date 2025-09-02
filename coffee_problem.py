#!/usr/bin/env python3
'''
Solve the coffee problem to learn how to drink coffee effectively.
'''

import numpy as np
import matplotlib.pyplot as plt


def solve_temp(t, T_init=90., T_env=20.0, k=1/300.):
    '''
    This function returns temperature as a function of time using Newton's
    law of cooling.

    Parameters
    ----------
    t: Numpy array
        An array of time values in seconds.
    T_init: floating point, defaults to 90.
        Initial temperature in Celsius.
    T_env: floating point, defaults to 20
        Ambient air temperature in Celsius
    k: floating point, defaults to 1/300.
        Heat transfer coefficient in 1/s.

    Returns
    -------
    t_coffee: Numpy array
        Temperature corresponding to time t

    '''

    t_coffee = T_env + (T_init - T_env) * np.exp(-k*t)

    return t_coffee

