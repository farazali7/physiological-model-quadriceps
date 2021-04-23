import numpy as np
import math
from scipy.integrate import solve_ivp
import numbers


def get_Ri(pulse_array, R0, tau_c):
    """
    :param pulse_array: Array of pulses sent by current time
    :param R0: Magnitude of enhancement in CN from pulses
    :param tau_c: Time constant controlling rise and decay of CN
    :return: Unitless term accounting for nonlinear summation of CN due to closely-spaced pulses
    """
    if not isinstance(R0, numbers.Number) or not isinstance(tau_c, numbers.Number) \
            or not (hasattr(pulse_array, '__len__')):
        raise TypeError('Parameters must be real numbers. Pulses must be in a collection.')
    elif len(pulse_array) < 0 or R0 <= 0 or tau_c <= 0:
        raise Exception('Parameter values must be positive.')

    if len(pulse_array) < 2:
        return 1
    else:
        curr_pulse = pulse_array[-1]
        prev_pulse = pulse_array[-2]
        exp_term = math.exp(-1 * ((curr_pulse - prev_pulse) / tau_c))
        scale_term = R0 - 1
        return 1 + (scale_term * exp_term)


def dCN(t, CN, train, tau_c, Km):
    """
    :param t: Time since start of simulation
    :param CN: Normalized concentration of calcium-troponin in muscle
    :param train: Array of stimulation pulse times
    :param tau_c: Time constant controlling rise and decay of CN
    :param Km: Sensitivity of cross-bridges to CN
    :return: Rate of change of CN
    """
    if not isinstance(t, numbers.Number) or not isinstance(CN, numbers.Number) \
            or not (isinstance(val, numbers.Number) for val in train) \
            or not isinstance(tau_c, numbers.Number) or not isinstance(Km, numbers.Number) \
            or not (hasattr(train, '__len__')):
        raise TypeError('Parameters must be real numbers. Pulses must be in a collection.')
    elif len(train) < 0 or t < 0 or tau_c <= 0 or Km < 0:
        raise Exception('Parameter values must be positive.')

    summation = []
    R0 = Km + 1.04
    pulse_array = [pulse for pulse in train if pulse < t]
    for i in range(len(pulse_array)):
        ti = pulse_array[i]
        exp_term = math.exp(-1 * ((t - ti) / tau_c))
        Ri = get_Ri(pulse_array[:i+1], R0, tau_c)
        summation.append(Ri * exp_term)
    summation = (np.sum(summation) / tau_c) - (CN / tau_c)
    return summation


# Functions below are for testing calcium dynamics independently

def get_CN(CN0, time, args):
    """
    :param CN0: Initial CN state
    :param time: Total time of simulation
    :param args: Additional arguments as required in CN dynamics function
    :return: Analytical CN values
    """

    sol = solve_ivp(dCN, time, CN0, args=args)
    return sol.y.T, sol.t
