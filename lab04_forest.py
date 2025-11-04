#!/usr/bin/env python3

'''
A module for burning forests and making pestilence.
What a happy coding time.
'''

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt


def forest_fire(isize=3, jsize=3, nstep=4, pspread=1.0):
    '''
    Create a forest fire.

    Parameters
    ----------
    isize, jsize : int, defaults to 3
        Set size of forest in x and y direction, respectively.
    nstep : int, defaults to 4
        Set number of steps to advance solution.
    pspread : float, defaults to 1.0
        Set chance that fire can spread in any direction, from 0 to 1
        (i.e., 0% to 100% chance of spread.)
    '''

    # Creating a forest and making all spots have trees.
    forest = np.zeros((nstep, isize, jsize)) + 2

    # Set initial fire to center [NEED TO UPDATE THIS FOR LAB]:
    forest[0, isize//2, jsize//2] = 3

    # Loop through time to advance our fire.
    for k in range(nstep-1):
        # Search every spot that is on fire and spread fire as needed.
        for i in range(isize):
            for j in range(jsize):
                # Are we on fire?
                if forest[k, i, j] != 3:
                    continue
                # Ah! it burns. Spread fire in each direction.
                # Spread "up" (i to i-1)
                if (pspread > rand()) and (i > 0) and (forest[k, i-1, j] == 2):
                    forest[k+1, i-1, j] = 3
                # Spread "Down"
                # Spread "East"
                # Spread "West"

    return forest
