#!/usr/bin/env python3

'''
A module for burning forests and making pestilence.
What a happy coding time.
'''

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Set plot style:
plt.style.use('fivethirtyeight')

# Generate our custom segmented color map for this project.
# We can specify colors by names and then create a colormap that only uses
# those names. We have 3 funadmental states, so we want only 3 colors.
# Color info: https://matplotlib.org/stable/gallery/color/named_colors.html
colors = ['tan', 'forestgreen', 'crimson']
forest_cmap = ListedColormap(colors)


def forest_fire(isize=3, jsize=3, nstep=4, pspread=1.0, pignite=0.0, pbare=0):
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
    pignite : float, defaults to 0.0
        Set the chance that a point starts the simulation on fire (or infected)
        from 0 to 1 (0% to 100%).
    pbare : float, defaults to 0.0
        Set the chance that a point starts the simulation on bare (or
        immune) from 0 to 1 (0% to 100%).
    '''

    # Creating a forest and making all spots have trees.
    forest = np.zeros((nstep, isize, jsize)) + 2

    # Set initial conditions for BURNING/INFECTED and BARE/IMMUNE
    # Start with BURNING/INFECTED:
    if pignite > 0:  # Scatter fire randomly:
        loc_ignite = np.zeros((isize, jsize), dtype=bool)
        while loc_ignite.sum() == 0:
            loc_ignite = rand(isize, jsize) <= pignite
        print(f"Starting with {loc_ignite.sum()} points on fire or infected.")
        forest[0, loc_ignite] = 3
    else:
        # Set initial fire to center:
        forest[0, isize//2, jsize//2] = 3

    # Set bare land/immune people:
    loc_bare = rand(isize, jsize) <= pbare
    forest[0, loc_bare] = 1

    # Loop through time to advance our fire.
    for k in range(nstep-1):
        # Assume the next time step is the same as the current:
        forest[k+1, :, :] = forest[k, :, :]
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

                # Change buring to burnt:
                forest[k+1, i, j] = 1

    return forest


def plot_progression(forest):
    '''Calculate the time dynamics of a forest fire and plot them.'''

    # Get total number of points:
    ksize, isize, jsize = forest.shape
    npoints = isize * jsize

    # Find all spots that have forests (or are healthy people)
    # ...and count them as a function of time.
    loc = forest == 2
    forested = 100 * loc.sum(axis=(1, 2))/npoints

    loc = forest == 1
    bare = 100 * loc.sum(axis=(1, 2))/npoints

    plt.plot(forested, label='Forested')
    plt.plot(bare, label='Bare/Burnt')
    plt.xlabel('Time (arbitrary units)')
    plt.ylabel('Percent Total Forest')


def plot_forest2d(forest_in, itime=0):
    '''
    Given a forest of size (ntime, nx, ny), plot the itime-th moment as a
    2d pcolor plot.
    '''

    # Create figure and axes
    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    fig.subplots_adjust(left=.117, right=.974, top=.929, bottom=0.03)

    # Add our pcolor plot, save the resulting mappable object.
    map = ax.pcolor(forest_in[itime, :, :], vmin=1, vmax=3, cmap=forest_cmap)

    # Add a colorbar by handing our mappable to the colorbar function.
    cbar = plt.colorbar(map, ax=ax, shrink=.8, fraction=.08,
                        location='bottom', orientation='horizontal')
    cbar.set_ticks([1, 2, 3])
    cbar.set_ticklabels(['Bare/Burnt', 'Forested', 'Burning'])

    # Flip y-axis (corresponding to the matrix's X direction)
    # And label stuff.
    ax.invert_yaxis()
    ax.set_xlabel('Eastward ($km$) $\\longrightarrow$')
    ax.set_ylabel('Northward ($km$) $\\longrightarrow$')
    ax.set_title(f'The Seven Acre Wood at T={itime:03d}')

    # Return figure object to caller:
    return fig


def make_all_2dplots(forest_in, folder='results/'):
    '''
    For every time frame in `forest_in`, create a 2D plot and save the image
    in folder.
    '''

    import os

    # Check to see if folder exists, if not, make it!
    if not os.path.exists(folder):
        os.mkdir(folder)

    # Make a buncha plots.
    ntime, nx, ny = forest_in.shape
    for i in range(ntime):
        print(f"\tWorking on plot #{i:04d}")
        fig = plot_forest2d(forest_in, itime=i)
        fig.savefig(f"{folder}/forest_i{i:04d}.png")
        plt.close('all')