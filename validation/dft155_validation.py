from model.force_model import ForceModel
from model.simulator import simulate
from utilities.loader import load_model_configuration
from utilities.train_generator import generate_doublet_train, ipi_to_frequency
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

CONFIG_PATH = '../configuration/dft155_configuration.csv'
DFT_VALIDATION_FILE_1 = '../validation/validation_data/dft155/first_4_d2002.csv'
DFT_VALIDATION_FILE_2 = '../validation/validation_data/dft155/last_4_d2002.csv'


def get_dft_train():
    """
    Creates a sequence of trains to match that of the DFT155 protocol used in Ding et. al. (2002)

    J. Ding, A. Wexler and S. Binder-Macleod,
    "A predictive fatigue model. I. Predicting the effect of stimulation frequency and pattern on fatigue",
    IEEE Transactions on Neural Systems and Rehabilitation Engineering, vol. 10, no. 1, pp. 48-58, 2002.
    Available: https://ieeexplore-ieee-org.proxy.lib.uwaterloo.ca/stamp/stamp.jsp?tp=&arnumber=1021586&tag=1.
    [Accessed 2 April 2021].

    :return: Array of pulse times
    """

    single_dft = np.array(generate_doublet_train(ipi_to_frequency(155), num_pulses=6, pulse_duration=0.6))
    all_dft = []
    for i in range(150):
        dft = np.copy(single_dft)
        if all_dft:
            dft += all_dft[-1] + 500
        all_dft.extend(dft)

    return np.array(all_dft)


def validate_dft155_protocol():
    dft_train = get_dft_train()

    f4_raw_data = pd.read_csv(DFT_VALIDATION_FILE_1, header=None)
    f4_raw_time = np.array(f4_raw_data[0])
    f4_raw_data = np.array(f4_raw_data[1])

    l4_raw_data = pd.read_csv(DFT_VALIDATION_FILE_2, header=None)
    l4_raw_time = np.array(l4_raw_data[0])
    l4_raw_data = np.array(l4_raw_data[1])

    _, indices = np.unique(f4_raw_time, return_index=True)
    f4_raw_time = f4_raw_time[np.sort(indices)]
    f4_raw_data = f4_raw_data[np.sort(indices)]
    _, indices = np.unique(l4_raw_time, return_index=True)
    l4_raw_time = l4_raw_time[np.sort(indices)]
    l4_raw_data = l4_raw_data[np.sort(indices)]

    time_raw_data = np.concatenate((f4_raw_time, l4_raw_time)) * 1000

    total_time = (0 * 1000, 123 * 1000)

    start = time.time()
    initial_state = [CN0, F0, scale_factor_rest, Km_rest, tau_1_rest]
    CN, F, A, Km, tau_1, t = simulate(force_model, total_time, dft_train,
                                      initial_state, tau_c,
                                      tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1,
                                      t_eval=time_raw_data)
    end = time.time()
    elapsed = end - start
    print(f'Simulation Time: {elapsed}')
    t = t / 1000
    f4_predicted_time = t[np.where(t <= 4)]
    f4_predicted_data = F[np.where(t <= 4)]

    l4_predicted_time = t[np.logical_and(119 <= t, t <= 123)]
    l4_predicted_data = F[np.logical_and(119 <= t, t <= 123)]

    f4_rmse = np.sqrt(np.square(f4_predicted_data - f4_raw_data).mean())
    f4_std = (f4_predicted_data - f4_raw_data).std()

    l4_rmse = np.sqrt(np.square(l4_predicted_data - l4_raw_data).mean())
    l4_std = (l4_predicted_data - l4_raw_data).std()

    plt.plot(t, F)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted Muscle Force During DFT155 Protocol')
    plt.show()

    plt.plot(f4_predicted_time, f4_predicted_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted Muscle Force at Start of DFT155 Protocol')
    plt.show()

    plt.plot(f4_raw_time, f4_raw_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Experimental Muscle Force at Start of DFT155 Protocol')
    plt.show()

    print('--- RMSE & STD FOR FIRST 4s ---')
    print("RMSE = {}".format(f4_rmse))
    print("STD = {}".format(f4_std))
    print('--------------------------------')
    plt.plot(f4_predicted_time, f4_predicted_data)
    plt.plot(f4_raw_time, f4_raw_data)
    plt.legend(['Predicted', 'Experimental'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted vs. Experimental Muscle Force First 4s of DFT155 Protocol')
    plt.show()

    plt.plot(l4_predicted_time, l4_predicted_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted Muscle Force at End of DFT155 Protocol')
    plt.show()

    plt.plot(l4_raw_time, l4_raw_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Experimental Muscle Force at End of DFT155 Protocol')
    plt.show()

    print('--- RMSE & STD FOR LAST 4s ---')
    print("RMSE = {}".format(l4_rmse))
    print("STD = {}".format(l4_std))
    print('--------------------------------')
    plt.plot(l4_predicted_time, l4_predicted_data)
    plt.plot(l4_raw_time, l4_raw_data)
    plt.legend(['Predicted', 'Experimental'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted vs. Experimental Muscle Force Last 4s of DFT155 Protocol')
    plt.show()


config = load_model_configuration(CONFIG_PATH)
tau_c, tau_2, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, \
CN0, F0, scale_factor_rest, tau_1_rest, Km_rest = config.values()

force_model = ForceModel(scale_factor_rest, Km_rest, tau_1_rest, tau_2)

validate_dft155_protocol()
