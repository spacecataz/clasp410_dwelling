#!/usr/bin/env python3

'''
Lab 5: Snowball Earth.
'''

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

# Some constants:
radearth = 6357000.  # Earth radius in meters.
mxdlyr = 50.         # depth of mixed layer (m)
sigma = 5.67e-8      # Steffan-Boltzman constant
C = 4.2e6            # Heat capacity of water
rho = 1020           # Density of sea-water (kg/m^3)


def gen_grid(npoints=18):
    '''
    Create a evenly spaced latitudinal grid with `npoints` cell centers.
    Grid will always run from zero to 180 as the edges of the grid. This
    means that the first grid point will be `dLat/2` from 0 degrees and the
    last point will be `180 - dLat/2`.

    Parameters
    ----------
    npoints : int, defaults to 18
        Number of grid points to create.

    Returns
    -------
    dLat : float
        Grid spacing in latitude (degrees)
    lats : numpy array
        Locations of all grid cell centers.
    '''

    dlat = 180 / npoints  # Latitude spacing.
    lats = np.linspace(dlat/2., 180-dlat/2., npoints)  # Lat cell centers.

    return dlat, lats


def temp_warm(lats_in):
    '''
    Create a temperature profile for modern day "warm" earth.

    Parameters
    ----------
    lats_in : Numpy array
        Array of latitudes in degrees where temperature is required

    Returns
    -------
    temp : Numpy array
        Temperature in Celcius.
    '''
    # Set initial temperature curve:
    T_warm = np.array([-47, -19, -11, 1, 9, 14, 19, 23, 25, 25,
                       23, 19, 14, 9, 1, -11, -19, -47])
    # Get base grid:
    npoints = T_warm.size
    dlat, lats = gen_grid(npoints)

    coeffs = np.polyfit(lats, T_warm, 2)

    # Now, return fitting:
    temp = coeffs[2] + coeffs[1]*lats_in + coeffs[0] * lats_in**2

    return temp


def insolation(S0, lats):
    '''
    Given a solar constant (`S0`), calculate average annual, longitude-averaged
    insolation values as a function of latitude.
    Insolation is returned at position `lats` in units of W/m^2.

    Parameters
    ----------
    S0 : float
        Solar constant (1370 for typical Earth conditions.)
    lats : Numpy array
        Latitudes to output insolation. Following the grid standards set in
        the diffusion program, polar angle is defined from the south pole.
        In other words, 0 is the south pole, 180 the north.

    Returns
    -------
    insolation : numpy array
        Insolation returned over the input latitudes.
    '''

    # Constants:
    max_tilt = 23.5   # tilt of earth in degrees

    # Create an array to hold insolation:
    insolation = np.zeros(lats.size)

    #  Daily rotation of earth reduces solar constant by distributing the sun
    #  energy all along a zonal band
    dlong = 0.01  # Use 1/100 of a degree in summing over latitudes
    angle = np.cos(np.pi/180. * np.arange(0, 360, dlong))
    angle[angle < 0] = 0
    total_solar = S0 * angle.sum()
    S0_avg = total_solar / (360/dlong)

    # Accumulate normalized insolation through a year.
    # Start with the spin axis tilt for every day in 1 year:
    tilt = [max_tilt * np.cos(2.0*np.pi*day/365) for day in range(365)]

    # Apply to each latitude zone:
    for i, lat in enumerate(lats):
        # Get solar zenith; do not let it go past 180. Convert to latitude.
        zen = lat - 90. + tilt
        zen[zen > 90] = 90
        # Use zenith angle to calculate insolation as function of latitude.
        insolation[i] = S0_avg * np.sum(np.cos(np.pi/180. * zen)) / 365.

    # Average over entire year; multiply by S0 amplitude:
    insolation = S0_avg * insolation / 365

    return insolation


def snowball_earth(nlat=18, tfinal=10000, dt=1.0):
    '''
    Solve the snowball Earth problem.

    Parameters
    ----------
    nlat : int, defaults to 18
        Number of latitude cells.
    tfinal : int or float, defaults to 10,000
        Time length of simulation in years.
    dt : int or float, defaults to 1.0
        Size of timestep in years.

    Returns
    --------
    lats : Numpy array
        Latitudes representing cell centers in degrees; 0 is south pole
        180 is north.
    Temp : Numpy array
        Temperature as a function of latitude.
    '''

    # Set up grid:
    dlat, lats = gen_grid(nlat)

    # Set number of time steps:
    nsteps = int(tfinal / dt)

    # Set timestep to seconds:
    dt = dt * 365 * 24 * 3600


def test_functions():
    '''Test our functions'''

    print('Test gen_grid')
    print('For npoints=5:')
    dlat_correct, lats_correct = 36.0, np.array([18., 54., 90., 126., 162.])
    result = gen_grid(5)
    if (result[0] == dlat_correct) and np.all(result[1] == lats_correct):
        print('\tPassed!')
    else:
        print('\tFAILED!')
        print(f"Expected: {dlat_correct}, {lats_correct}")
        print(f"Got: {gen_grid(5)}")