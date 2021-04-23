from model.calcium_dynamics import dCN
import numbers

def dynamics(t, Y, force_model, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, train, tau_c):
    """
    :param t: Time since start of simulation
    :param Y: State vector containing CN, force, force scale factor, Km, and tau_1
    :param force_model: Force muscle model fit with rest parameters
    :param tau_fat: Time constant controlling rate of muscle strength recovery
    :param alpha_scale_factor: Force-driving coefficient for force scale factor
    :param alpha_Km: Force-driving coefficient for Km
    :param alpha_tau_1: Force-driving coefficient for tau_1
    :param train: Array of stimulation pulse times
    :param tau_c: Time constant controlling rise and decay of CN
    :return: Fatigue muscle model system dynamics
    """
    if not isinstance(t, numbers.Number) or not isinstance(tau_fat, numbers.Number) \
            or not isinstance(alpha_scale_factor, numbers.Number) or not isinstance(alpha_Km, numbers.Number) \
            or not isinstance(alpha_tau_1, numbers.Number) or not isinstance(tau_c, numbers.Number) \
            or not hasattr(Y, '__len__'):
        raise TypeError('Parameters are of incorrect type.')
    elif len(Y) != 5 or tau_fat < 0:
        raise Exception('State array must have 5 elements. Fatigue time constant must be positive. ')

    CN = Y[0]
    F = Y[1]
    scale_factor = Y[2]
    Km = Y[3]
    tau_1 = Y[4]

    dA = (alpha_scale_factor * F) - ((scale_factor - force_model.force_scale_factor_rest) / tau_fat)
    dKm = (alpha_Km * F) - ((Km - force_model.Km_rest) / tau_fat)
    dtau_1 = (alpha_tau_1 * F) - ((tau_1 - force_model.tau_1_rest) / tau_fat)

    return [dCN(t, CN, Km=Km, train=train, tau_c=tau_c),
            force_model.dF(F, CN, scale_factor, tau_1, Km),
            dA,
            dKm,
            dtau_1]
