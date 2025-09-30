#!/usr/bin/env python3
'''
Solve the coffee problem to learn how to drink coffee effectively.
'''

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')


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


def time_to_temp(T_final, T_init=90., T_env=20.0, k=1/300.):
    '''
    Given a target temperature, determine how long it takes to reach
    the target temp using Newton's law of cooling.

    Parameters
    ----------
    T_final: floating point
        Final goal temperature of coffee.
    T_init: floating point, defaults to 90.
        Initial temperature in Celsius.
    T_env: floating point, defaults to 20
        Ambient air temperature in Celsius
    k: floating point, defaults to 1/300.
        Heat transfer coefficient in 1/s.

    Returns
    -------
    t : float
        time, in seconds, to cool to target T_final
    '''

    t = (-1/k) * np.log((T_final - T_env) / (T_init - T_env))

    return t


def solve_euler(dfx, dt=.25, f0=90., t_start=0., t_final=300., **kwargs):
    '''
    Solve an ordinary diffyQ using Euler's method.
    Extra kwargs are passed to the dfx function.

    Parameters
    ----------
    dfx : function
        A function representing the time derivative of our diffyQ. It should
        take 2 arguments: the current time and current function value
        and return 1 value: the time derivative at time `t`.
    f0 : float
        Initial condition for our differential equation
    t_start, t_final : float, 0 and 300. respectively
        The start and final times for our solver in seconds
    dt : float, defaults to 0.25
        Time step in seconds.

    Returns
    -------
    t : Numpy array
        Time in seconds over the entire solution.
    fx : Numpy array
        The solution as a function of time.
    '''

    # Configure our problem:
    time = np.arange(t_start, t_final, dt)
    fx = np.zeros(time.size)
    fx[0] = f0

    # Solve!
    for i in range(time.size - 1):
        fx[i+1] = fx[i] + dt * dfx(time[i], fx[i], **kwargs)

    return time, fx


def solve_rk8(dfx, dt=.25, f0=90., t_start=0., t_final=300., **kwargs):
    '''
    Solve an ordinary diffyQ using Euler's method.
    Extra kwargs are passed to the dfx function.

    Parameters
    ----------
    dfx : function
        A function representing the time derivative of our diffyQ. It should
        take 2 arguments: the current time and current function value
        and return 1 value: the time derivative at time `t`.
    f0 : float
        Initial condition for our differential equation
    t_start, t_final : float, 0 and 300. respectively
        The start and final times for our solver in seconds
    dt : float, defaults to 0.25
        Time step in seconds.

    Returns
    -------
    t : Numpy array
        Time in seconds over the entire solution.
    fx : Numpy array
        The solution as a function of time.
    '''

    from scipy.integrate import solve_ivp

    result = solve_ivp(dfx, [t_start, t_final], [f0], method='DOP853',
                       max_step=dt)

    return result.t, result.y[0, :]


def newtcool(t, Tnow, k=1/300., T_env=20.0):
    '''
    Newton's law of cooling: given time t, Temperature now (Tnow), a cooling
    coefficient (k), and an environmental temp (T_env), return the rate of
    cooling (i.e., dT/dt)
    '''

    return -k * (Tnow - T_env)


def verify_code():
    '''
    Verify that our implementation is correct.
    Using example problem from
    https://www.wssd.k12.pa.us/downloads/calculus%20%20%20%20%20newton%20law%20of%20cooling%20solutions.pdf
    '''
    t_real = 60. * 10.76
    k = np.log(95./110.) / -120.0
    t_code = time_to_temp(120, T_init=180, T_env=70, k=k)

    print("Target solution is: ", t_real)
    print("Numerical solution is ", t_code)
    print("Difference is ", t_real - t_code)


def answer_coffee_problem():
    '''
    Using the functions above, answer the question of when I should add
    cream to my coffee: now or later.
    '''
    # Solve the actual problem using the functions declared above.
    # First, do it quantitatively to the screen:
    t_1 = time_to_temp(65)             # Add cream at T=65 to get to 60.
    t_2 = time_to_temp(60, T_init=85)  # Add cream immediately.
    t_c = time_to_temp(60)             # Control case: No cream.

    print("TIME TO DRINKABLE COFFEE:")
    print(f"\tControl case = {t_c:.2f}s")
    print(f"\tAdd cream later = {t_1:.1f}\n\tAdd cream now = {t_2:.1f}")

    # Create time series of temperatures for cooling coffee.
    t = np.arange(0, 600., 0.5)
    temp1 = solve_temp(t)  # also the same as control case.
    temp2 = solve_temp(t, T_init=85.)

    # Create our figure and plot stuff!
    fig, ax = plt.subplots(1, 1)
    ax.plot(t, temp1, label=f'Add Cream Later (T={t_1:.1f}s')
    ax.plot(t, temp2, label=f'Add Cream Now (T={t_2:.1f}s')

    ax.legend()
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature (C)')
    ax.set_title('When to add cream: \nGetting coffee cooled quickly')
    fig.tight_layout()


def explore_numerical_solve(dt=1.0):
    '''
    Compare numerical vs. analytical solution for Newton's law of cooling.

    Parameters
    ---------
    dt : float, defaults to 1.0
        Set the time step for the Euler solver.
    '''

    # Create ANALYTICAL time series of temperatures for cooling coffee.
    t = np.arange(0, 300., 0.5)
    temp1 = solve_temp(t)  # also the same as control case.

    # Obtain Euler solver numerical solution.
    etime, etemp = solve_euler(newtcool, t_final=300., dt=dt)
    etime2, etemp2 = solve_rk8(newtcool, t_final=300., dt=dt)

    # Make a beautiful plot to illustrate how the numerical solution
    # performs.
    fig, ax = plt.subplots(1, 1, figsize=[10.24,  5.91])
    # Plot lines we want to show:
    ax.plot(t, temp1, label='Analytical Solution')
    ax.plot(etime, etemp, 'o--', label=f'Euler Solution for $\Delta t={dt}s$')
    ax.plot(etime2, etemp2, 'o--', label=f'RK8 Solution$')

    ax.legend()
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature (C)')
    ax.set_title('Analytical vs. Numerical: The Greatest Battle of Our Time')
    fig.tight_layout()

    return fig
