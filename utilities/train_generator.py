import numpy as np
import matplotlib.pyplot as plt


def generate_constant_train(frequency, total_time=10000, num_pulses=-1):
    """
    :param frequency: Frequency of stimulation pulses in Hz
    :param total_time: Time duration of entire stimulation train in ms
    :param num_pulses: Total number of pulses
    :return: Array of pulse times in Constant frequency train format
    """

    period = (1 / frequency) * 1000
    time = 0
    constant_train = []
    iterator = lambda: time < total_time
    if not num_pulses < 1:
        iterator = lambda: len(constant_train) < num_pulses
    while iterator():
        constant_train.append(time)
        time += period

    return constant_train


def generate_variable_train(frequency, total_time=10000, initial_ipi=5, num_pulses=-1):
    """
    :param frequency: Frequency of stimulation pulses in Hz
    :param total_time: Time duration of entire stimulation train in ms
    :param initial_ipi: Inter-pulse interval between first and only pulse pair in ms
    :param num_pulses: Total number of pulses
    :return: Array of pulse times in Variable frequency train format
    """

    period = (1 / frequency) * 1000
    time = 0
    variable_train = [time, time + initial_ipi]
    time += initial_ipi + period
    iterator = lambda: time < total_time
    if not num_pulses < 1:
        iterator = lambda: len(variable_train) < (num_pulses - 1)
    while iterator():
        variable_train.append(time)
        time += period

    return variable_train


def generate_doublet_train(frequency, total_time=10000, doublet_ipi=5, num_pulses=-1, pulse_duration=0):
    """
    :param frequency: Frequency of stimulation pulses in Hz
    :param total_time: Time duration of entire stimulation train in ms
    :param doublet_ipi: Inter-pulse interval between pulse pairs in ms
    :param num_pulses: Total number of pulses
    :return: Array of pulse times in Doublet frequency train format
    """

    period = (1 / frequency) * 1000
    time = 0
    doublet_train = []
    iterator = lambda: time < total_time
    if not num_pulses < 1:
        iterator = lambda: len(doublet_train) < num_pulses
    while iterator():
        doublet_train.append(time)
        time += doublet_ipi + pulse_duration
        doublet_train.append(time)
        time += period + pulse_duration

    return doublet_train


def ipi_to_frequency(ipi):
    """
    :param ipi: Inter-pulse interval in ms
    :return: Frequency in Hz
    """

    return 1 / (ipi / 1000)


def get_mean_frequency(train):
    """
    :param train: Array of pulse times
    :return: Average frequency in entire train
    """

    return ipi_to_frequency(train[-1] / (len(train) - 1))


def plot_train(train):
    """
    :param train: Array of pulse times
    """

    end_time = train[-1] + 1000
    time = np.arange(0, end_time, 0.01)
    pulses = np.zeros(shape=(len(time)))
    pulses[np.where(np.isin(time, train))] = 1
    plt.plot(time, pulses)
    plt.show()
