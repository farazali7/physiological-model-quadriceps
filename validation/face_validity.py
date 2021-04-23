from model.force_model import ForceModel
from model.simulator import simulate
from utilities.loader import load_model_configuration
from utilities.train_generator import generate_constant_train
import matplotlib.pyplot as plt
import time

CONFIG_PATH = '../configuration/vft_cft33_configuration.csv'


def face_validity():
    constant_fatiguing_train = generate_constant_train(frequency=50, total_time=30*1000)

    start = time.time()
    initial_state = [CN0, F0, scale_factor_rest, Km_rest, tau_1_rest]
    CN, F, A, Km, tau_1, t = simulate(force_model, total_time, constant_fatiguing_train,
                                      initial_state, tau_c,
                                      tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1)
    end = time.time()
    elapsed = end - start
    print(f'Simulation Time: {elapsed}')

    t = t / 1000

    fig, ax = plt.subplots(5, 1, sharex=True, figsize=(10, 8))
    ax[0].plot(t, F)
    ax[0].set_ylabel('Force (N)')
    ax[1].plot(t, CN)
    ax[1].set_ylabel('CN')
    ax[2].plot(t, A)
    ax[2].set_ylabel('A (N/ms)')
    ax[3].plot(t, Km)
    ax[3].set_ylabel('Km')
    ax[4].plot(t, tau_1)
    ax[4].set_ylabel('tau_1 (ms)')
    plt.xlabel('Time (s)')
    plt.show()

    constant_spaced_train = generate_constant_train(frequency=1, total_time=30*1000)

    start = time.time()
    CN, F, A, Km, tau_1, t = simulate(force_model, total_time, constant_spaced_train,
                                      initial_state, tau_c,
                                      tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1)
    end = time.time()
    elapsed = end - start
    print(f'Simulation Time: {elapsed}')

    t = t / 1000

    fig, ax = plt.subplots(5, 1, sharex=True, figsize=(10, 8))
    ax[0].plot(t, F)
    ax[0].set_ylabel('Force (N)')
    ax[1].plot(t, CN)
    ax[1].set_ylabel('CN')
    ax[2].plot(t, A)
    ax[2].set_ylabel('A (N/ms)')
    ax[3].plot(t, Km)
    ax[3].set_ylabel('Km')
    ax[4].plot(t, tau_1)
    ax[4].set_ylabel('tau_1 (ms)')
    plt.xlabel('Time (s)')
    plt.show()

    train_1 = [50, 60, 380, 390, 400, 500]
    CN, F, A, Km, tau_1, t = simulate(force_model, (0, 1000), train_1,
                                      initial_state, tau_c,
                                      tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1)
    fig, ax = plt.subplots(2, sharex=True)
    ax[0].plot(t, CN, '-bD')
    ax[0].set_ylabel('CN')
    ax[1].plot(t, F, '-bD')
    ax[1].set_ylabel('Force (N)')
    plt.xlabel('Time (ms)')
    plt.tight_layout()
    plt.show()


config = load_model_configuration(CONFIG_PATH)
tau_c, tau_2, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, \
CN0, F0, scale_factor_rest, tau_1_rest, Km_rest = config.values()

total_time = (0 * 1000, 30 * 1000)

force_model = ForceModel(scale_factor_rest, Km_rest, tau_1_rest, tau_2)

face_validity()
