from utilities.loader import load_model_configuration
from utilities.train_generator import generate_constant_train, generate_doublet_train, generate_variable_train
from model.simulator import simulate
from model.force_model import ForceModel
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import os
from scipy.integrate import cumulative_trapezoid, simps

CONFIG_PATH = 'configuration/vft_cft33_configuration.csv'

config = load_model_configuration(CONFIG_PATH)
tau_c, tau_2, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, \
CN0, F0, scale_factor_rest, tau_1_rest, Km_rest = config.values()
CONFIG_PATH = 'dft155_configuration.csv'

config = load_model_configuration(CONFIG_PATH)
tau_c, tau_2, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, \
CN0, F0, scale_factor_rest, tau_1_rest, Km_rest = config.values()

total_time = (0, 60 * 1000)
force_model = ForceModel(scale_factor_rest, Km_rest, tau_1_rest, tau_2)
initial_state = [CN0, F0, scale_factor_rest, Km_rest, tau_1_rest]

simulation_trains = [0,0,0,0,0,0,0,0,0]

simulation_trains[0] = generate_constant_train(20, 10 * 1000)
simulation_trains[1] = generate_constant_train(50, 10 * 1000)
simulation_trains[2] = generate_constant_train(80, 10 * 1000)
simulation_trains[3] = generate_variable_train(20, 10 * 1000)
simulation_trains[4] = generate_variable_train(50, 10 * 1000)
simulation_trains[5] = generate_variable_train(80, 10 * 1000)
simulation_trains[6] = generate_doublet_train(20, 10 * 1000)
simulation_trains[7] = generate_doublet_train(50, 10 * 1000)
simulation_trains[8] = generate_doublet_train(80, 10 * 1000)

for i in range(9):
    simulation_train = simulation_trains[i]
    train = simulation_train

    for j in range(10500, 60 * 1000, 10500):
        train = np.append(train, [t+j for t in simulation_train])

    CN, F, A, Km, tau_1, t = simulate(force_model, total_time, train,
                                    initial_state, tau_c, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1)

    title = str(i) + '.csv'
    df = pd.DataFrame({"Time (ms)" : t, "Force (N)" : F})
    df.to_csv(title, index=False)

    plt.figure()
    plt.plot(t, F)
    plt.xlabel('Time (ms)')
    plt.ylabel('Force (N)')
    plt.savefig(title)


def calculate_strength_index(file):
    data = np.array(pd.read_csv(file))
    forces = data[:, 1]
    times = data[:, 0]
    peak_force = np.max(forces)
    avg_force = forces.mean()
    force_integral = simps(forces, x=times)
    max_start = np.max(forces[np.where(times <= 10 * 1000)])
    max_end = np.max(forces[np.where(times > 52.5 * 1000)])
    fatigue_index = 1 - ((max_start - max_end) / max_start)
    strength_index = force_integral * fatigue_index
    rmse = np.sqrt(np.square(forces - peak_force).mean())
    nrmse = rmse / peak_force
    strength_index = avg_force*(1-nrmse)
    return strength_index


cft_vft_validated_dir = './Simulations/cft_vft_validated/Time & Force Values'
dft_validated_dir = './Simulations/dft_validated/Time & Force Values'

cft_names = []
cft_strengths = []
for f in os.listdir(cft_vft_validated_dir):
    file_path = os.path.join(cft_vft_validated_dir, f)
    strength_index = calculate_strength_index(file_path)
    cft_strengths.append(strength_index)
    cft_names.append(f)

dft_names = []
dft_strengths = []
for f in os.listdir(dft_validated_dir):
    file_path = os.path.join(dft_validated_dir, f)
    strength_index = calculate_strength_index(file_path)
    dft_strengths.append(strength_index)
    dft_names.append(f)

arr = np.array([cft_names, cft_strengths, dft_names, dft_strengths]).T
df = pd.DataFrame(arr)
df.to_csv('results/strength_index_results.csv', index=False, header=False)

