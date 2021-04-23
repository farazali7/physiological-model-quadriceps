from model.force_model import ForceModel
from model.simulator import simulate
from utilities.loader import load_model_configuration
from utilities.train_generator import generate_constant_train, generate_variable_train
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

CONFIG_PATH = '../configuration/vft_cft33_configuration.csv'
VALIDATION_FILE_1 = '../validation/validation_data/vft_cft33/first_60_d2015.csv'
VALIDATION_FILE_2 = '../validation/validation_data/vft_cft33/last_60_d2015.csv'


def get_validation_train(cycles=8):
    """
    Creates a sequence of trains to match that of the fatiguing protocol used in Doll et. al. (2015)

     B. D. Doll, N. A. Kirsch, and N. Sharma,
     “Optimization of a stimulation train based on a predictive model of muscle force and fatigue,”
     IFAC-PapersOnLine, vol. 48, no. 20, pp. 338–342, 2015.

    :return: Array of pulse times
    """

    fat_cft = np.array(generate_constant_train(33, 1000))
    all_fat_cft = []
    for i in range(13):
        cft = np.copy(fat_cft)
        if all_fat_cft:
            cft += all_fat_cft[-1] + 1000
        all_fat_cft.extend(cft)
    fat_nfcft = np.array(generate_constant_train(50, num_pulses=20)) + 1000 + all_fat_cft[-1]
    fat_nfvft = np.array(generate_variable_train(12.5, num_pulses=14)) + 1000 + fat_nfcft[-1]
    fat_cycle = []
    fat_cycle.extend(all_fat_cft)
    fat_cycle.extend(fat_nfcft)
    fat_cycle.extend(fat_nfvft)
    full_fat_cycle = []
    for i in range(cycles):
        cycle = np.copy(fat_cycle)
        if full_fat_cycle:
            cycle += full_fat_cycle[-1] + 1000
        full_fat_cycle.extend(cycle)

    train = []
    train.extend(full_fat_cycle)

    return np.array(train)


def validate_vft_cft33_fatigue_protocol():
    validation_train = get_validation_train()

    f60_raw_data = pd.read_csv(VALIDATION_FILE_1, header=None)
    f60_raw_time = np.array(f60_raw_data[0])
    f60_raw_data = np.array(f60_raw_data[1])

    l60_raw_data = pd.read_csv(VALIDATION_FILE_2, header=None)
    l60_raw_time = np.array(l60_raw_data[0])
    l60_raw_data = np.array(l60_raw_data[1])

    _, indices = np.unique(f60_raw_time, return_index=True)
    f60_raw_time = f60_raw_time[np.sort(indices)]
    f60_raw_data = f60_raw_data[np.sort(indices)]
    _, indices = np.unique(l60_raw_time, return_index=True)
    l60_raw_time = l60_raw_time[np.sort(indices)]
    l60_raw_data = l60_raw_data[np.sort(indices)]

    time_raw_data = np.concatenate((f60_raw_time, l60_raw_time)) * 1000

    start = time.time()
    initial_state = [CN0, F0, scale_factor_rest, Km_rest, tau_1_rest]
    CN, F, A, Km, tau_1, t = simulate(force_model, total_time, validation_train,
                                      initial_state, tau_c,
                                      tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1,
                                      t_eval=time_raw_data)
    end = time.time()
    elapsed = end - start
    print(f'Simulation Time: {elapsed}')

    t = t / 1000

    f60_predicted_time = t[np.where(t <= 60)]
    f60_predicted_data = F[np.where(t <= 60)]

    l60_predicted_time = t[np.logical_and(170 <= t, t <= 230)]
    l60_predicted_data = F[np.logical_and(170 <= t, t <= 230)]

    f60_rmse = np.sqrt(np.square(f60_predicted_data - f60_raw_data).mean())
    f60_std = (f60_predicted_data - f60_raw_data).std()

    l60_rmse = np.sqrt(np.square(l60_predicted_data - l60_raw_data).mean())
    l60_std = (l60_predicted_data - l60_raw_data).std()

    plt.plot(t, F)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted Muscle Force During Fatiguing Protocol')
    plt.show()

    plt.plot(f60_predicted_time, f60_predicted_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted Muscle Force at Start of Fatiguing Protocol')
    plt.show()

    plt.plot(f60_raw_time, f60_raw_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Experimental Muscle Force at Start of Fatiguing Protocol')
    plt.show()

    print('--- RMSE & STD FOR FIRST 60s ---')
    print("RMSE = {}".format(f60_rmse))
    print("STD = {}".format(f60_std))
    print('--------------------------------')
    plt.plot(f60_predicted_time, f60_predicted_data)
    plt.plot(f60_raw_time, f60_raw_data)
    plt.legend(['Predicted', 'Experimental'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted vs. Experimental Muscle Force First 60s of Fatiguing Protocol')
    plt.show()

    plt.plot(l60_predicted_time, l60_predicted_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted Muscle Force at End of Fatiguing Protocol')
    plt.show()

    plt.plot(l60_raw_time, l60_raw_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Experimental Muscle Force at End of Fatiguing Protocol')
    plt.show()

    print('--- RMSE & STD FOR LAST 60s ---')
    print("RMSE = {}".format(l60_rmse))
    print("STD = {}".format(l60_std))
    print('--------------------------------')
    plt.plot(l60_predicted_time, l60_predicted_data)
    plt.plot(l60_raw_time, l60_raw_data)
    plt.legend(['Predicted', 'Experimental'])
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Predicted vs. Experimental Muscle Force Last 60s of Fatiguing Protocol')
    plt.show()


config = load_model_configuration(CONFIG_PATH)
tau_c, tau_2, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, \
CN0, F0, scale_factor_rest, tau_1_rest, Km_rest = config.values()

total_time = (0 * 1000, 230 * 1000)

force_model = ForceModel(scale_factor_rest, Km_rest, tau_1_rest, tau_2)

validate_vft_cft33_fatigue_protocol()
