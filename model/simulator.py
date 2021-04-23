from model.calcium_dynamics import dCN
from model.fatigue_model import dynamics
from scipy.integrate import solve_ivp


def simulate_non_fatigued_model(force_model, total_time, train, tau_c, t_eval=None):
    """
    :param force_model: Force muscle model fit with rest parameters
    :param total_time: Total simulation time in ms
    :param train: Array of stimulation pulse times
    :return: Analytical values for CN, force, and respective simulation times
    """

    def f(t, x):
        """
        :param t: Simulation time
        :param x: State vector containing CN and force
        :return: Rate of change array for CN and force
        """

        CN = x[0]
        F = x[1]
        return [dCN(t, CN, train, tau_c, force_model.Km_rest),
                force_model.dF(F, CN, force_model.force_scale_factor_rest, force_model.tau_1_rest, force_model.Km_rest)]

    sol = solve_ivp(f, total_time, [0, 0], t_eval=t_eval)

    return sol.y.T[:, 0], sol.y.T[:, 1], sol.t


def simulate(force_model, total_time, train, initial_state, tau_c,
             tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1,
             t_eval=None):
    """
    :param force_model: Force muscle model fit with rest parameters
    :param total_time: Total simulation time in ms
    :param train: Array of stimulation pulse times
    :return: Analytical values for CN, force, force_scale_factor, Km, tau_1, and respective simulation times
    """
    sol = solve_ivp(dynamics, total_time, initial_state,
                    args=(force_model, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, train, tau_c),
                    t_eval=t_eval)

    return sol.y.T[:, 0], sol.y.T[:, 1], sol.y.T[:, 2], sol.y.T[:, 3], sol.y.T[:, 4], sol.t
