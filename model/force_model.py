import numbers

class ForceModel:
    """
    Force muscle model adapted from Ding et al. (1997). The
    dynamic model is defined in terms of activation dynamics and force generation
    dynamics. The former is characterized by CN, representing the formation of
    the calcium-troponin complex when muscles contract. The latter is characterized
    by a decay over given time constants.
    """
    def __init__(self, force_scale_factor, Km, tau_1, tau_2):
        """
        :param force_scale_factor: Scale factor for muscle force when muscle is non-fatigued
        :param Km: Sensitivity of cross-bridges to CN when muscle is non-fatigued
        :param tau_1: Time constant for force decline in absence of cross-bridges when muscle is non-fatigued
        :param tau_2: Time constant for force decline in presence of cross-bridges when muscle is non-fatigued
        """
        if not isinstance(force_scale_factor, numbers.Number) or not isinstance(Km, numbers.Number) \
                or not isinstance(tau_1, numbers.Number) or not isinstance(tau_2, numbers.Number):
            raise TypeError('Parameters must be real numbers.')
        elif force_scale_factor < 0 or Km < 0 or tau_1 < 0 or tau_2 <= 0:
            raise Exception('Parameter values must be positive.')

        self.force_scale_factor_rest = force_scale_factor
        self.tau_1_rest = tau_1
        self.tau_2 = tau_2
        self.Km_rest = Km

    def dF(self, F, CN, force_scale_factor, tau_1, Km):
        """
        :param F: Force produced by muscle
        :param CN: Normalized concentration of calcium-troponin in muscle
        :param force_scale_factor: Scale factor for muscle force
        :param tau_1: Time constant for force decline in absence of cross-bridges
        :param Km: Sensitivity of cross-bridges to CN
        :return: Rate of change of force produced by muscle
        """
        if not isinstance(F, numbers.Number) or not isinstance(CN, numbers.Number) \
                or not isinstance(force_scale_factor, numbers.Number) or not isinstance(tau_1, numbers.Number) \
                or not isinstance(Km, numbers.Number):
            raise TypeError('Parameters must be real numbers.')
        elif force_scale_factor < 0 or tau_1 < 0:
            raise Exception('Parameter values must be positive.')
        michaelis_menten_term = (CN / (Km + CN))
        force_development = force_scale_factor * michaelis_menten_term
        force_decay = F / (tau_1 + (self.tau_2 * michaelis_menten_term))
        return force_development - force_decay


