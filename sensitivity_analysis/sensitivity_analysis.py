from force_model import ForceModel
from simulator import simulate
from loader import load_model_configuration
from train_generator import generate_constant_train, generate_variable_train
import matplotlib.pyplot as plt
import numpy as np


def get_validation_train():
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
    for i in range(8):
        cycle = np.copy(fat_cycle)
        if full_fat_cycle:
            cycle += full_fat_cycle[-1] + 1000
        full_fat_cycle.extend(cycle)

    train = []
    train.extend(full_fat_cycle)

    return np.array(train)


CONFIGS = ['alpha_Km+1STD', 'alpha_Km+2STD', 'alpha_Km-1STD', 'alpha_Km-2STD',
           'alpha_scale_factor+1STD', 'alpha_scale_factor+2STD', 'alpha_scale_factor-1STD', 'alpha_scale_factor-2STD',
           'alpha_tau_1+1STD', 'alpha_tau_1+2STD', 'alpha_tau_1+3STD',
           'Km_rest+1STD', 'Km_rest+2STD', 'Km_rest+3STD', 'Km_rest-HalfSTD',
           'scale_factor_rest+1STD', 'scale_factor_rest+2STD', 'scale_factor_rest-1STD', 'scale_factor_rest-2STD',
           'subject_1', 'subject_2', 'subject_3', 'subject_4', 'subject_5', 'subject_6',
           'tau_1_rest+1STD', 'tau_1_rest+2STD', 'tau_1_rest+3STD',
           'tau_2-1STD', 'tau_2-2STD', 'tau_2+1STD', 'tau_2+2STD',
           'tau_fat+1STD', 'tau_fat+2STD', 'tau_fat-1STD', 'tau_fat-2STD']
SUB_FOLDER = 'sensitivity_analysis/'
CONFIG_FOLDER = 'configs/'
validated_configuration = 'model_configuration.csv'

total_time = (0 * 1000, 230 * 1000)
validation_train = get_validation_train()

config = load_model_configuration(validated_configuration)
tau_c, tau_2, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, \
    CN0, F0, scale_factor_rest, tau_1_rest, Km_rest = config.values()

validated_force_model = ForceModel(scale_factor_rest, Km_rest, tau_1_rest, tau_2)

validated_initial_state = [CN0, F0, scale_factor_rest, Km_rest, tau_1_rest]
V_CN, V_F, V_A, V_Km, V_tau_1, V_t = simulate(validated_force_model, total_time, validation_train,
                                              validated_initial_state, tau_c, tau_fat,
                                              alpha_scale_factor, alpha_Km, alpha_tau_1)
V_t = V_t / 1000
validated_f60_time = V_t[np.where(V_t <= 60)]
validated_f60_data = V_F[np.where(V_t <= 60)]
validated_l60_time = V_t[np.logical_and(170 <= V_t, V_t <= 230)]
validated_l60_data = V_F[np.logical_and(170 <= V_t, V_t <= 230)]

for CONFIG in CONFIGS:
    config = load_model_configuration(SUB_FOLDER + CONFIG_FOLDER + CONFIG + '.csv')
    tau_c, tau_2, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, \
        CN0, F0, scale_factor_rest, tau_1_rest, Km_rest = config.values()

    force_model = ForceModel(scale_factor_rest, Km_rest, tau_1_rest, tau_2)

    initial_state = [CN0, F0, scale_factor_rest, Km_rest, tau_1_rest]
    CN, F, A, Km, tau_1, t = simulate(force_model, total_time, validation_train,
                                      initial_state, tau_c, tau_fat,
                                      alpha_scale_factor, alpha_Km, alpha_tau_1)

    t = t / 1000
    first_60_time = t[np.where(t <= 60)]
    first_60_data = F[np.where(t <= 60)]

    last_60_time = t[np.logical_and(170 <= t, t <= 230)]
    last_60_data = F[np.logical_and(170 <= t, t <= 230)]

    plt.clf()
    plt.plot(t, F, color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Muscle Force During ' + CONFIG)
    plt.savefig(SUB_FOLDER + 'full/full_' + CONFIG + '.png', dpi=1200)

    plt.clf()
    plt.plot(first_60_time, first_60_data, label=CONFIG, color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Muscle Force at Start of ' + CONFIG)
    plt.savefig(SUB_FOLDER + 'start/start_' + CONFIG + ".png", dpi=1200)

    plt.clf()
    plt.plot(last_60_time, last_60_data, label=CONFIG, color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Muscle Force at End of ' + CONFIG)
    plt.savefig(SUB_FOLDER + 'end/end_' + CONFIG + ".png", dpi=1200)

    plt.clf()
    plt.plot(t, F, label=CONFIG, color='red')
    plt.plot(V_t, V_F, label="Validated", color='blue')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Compare Validated Model to ' + CONFIG)
    plt.savefig(SUB_FOLDER + 'full_compare/full_compare_' + CONFIG + ".png", dpi=1200)

    plt.clf()
    plt.plot(first_60_time, first_60_data, label=CONFIG, color='red')
    plt.plot(validated_f60_time, validated_f60_data, label="Validated", color='blue')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Compare First 60 Seconds of the Validated Model to ' + CONFIG)
    plt.savefig(SUB_FOLDER + 'start_compare/start_compare_' + CONFIG + ".png", dpi=1200)

    plt.clf()
    plt.plot(last_60_time, last_60_data, label=CONFIG, color='red')
    plt.plot(validated_l60_time, validated_l60_data, label="Validated", color='blue')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Compare Last 60 Seconds of the Validated Model to ' + CONFIG)
    plt.savefig(SUB_FOLDER + 'end_compare/end_compare_' + CONFIG + ".png", dpi=1200)

    print('Completed ' + CONFIG)
