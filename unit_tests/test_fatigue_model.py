import pytest
import numbers
from model.force_model import ForceModel
from model.fatigue_model import dynamics


@pytest.mark.parametrize("t, Y, force_model, tau_fat, alpha_scale_factor, "
                         "alpha_Km, alpha_tau_1, train, tau_c, result", [
                             (1, [1, 1, 1, 1, 1], ForceModel(1, 2, 1, 1), 1, 1, 1, 1, [1], 1, [1, 2, 1]),
                             (1, [1, 1, 1, 1], ForceModel(1, 2, 1, 1), 1, 1, 1, 1, [1], 1, [1, 1, 1]),
                             (1, [1, 1, 1, 1, 1], ForceModel(1, 2, 1, 1), -1, 1, 1, 1, [1], 1, [1, 1, 1]),
                             ("1", ["1", 1, 1, 1, 1], ForceModel(1, 2, 1, 1), "1", "1", 1, "1", [1], "1", [1, 1, 1]),
                         ])
def test_dynamics(t, Y, force_model, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, train, tau_c, result):
    if not isinstance(t, numbers.Number) or not isinstance(tau_fat, numbers.Number) \
            or not isinstance(alpha_scale_factor, numbers.Number) or not isinstance(alpha_Km, numbers.Number) \
            or not isinstance(alpha_tau_1, numbers.Number) or not isinstance(tau_c, numbers.Number) \
            or not hasattr(Y, '__len__'):
        with pytest.raises(TypeError):
            dynamics(t, Y, force_model, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, train, tau_c)
    elif len(Y) != 5 or tau_fat < 0:
        with pytest.raises(Exception):
            dynamics(t, Y, force_model, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, train, tau_c)
    else:
        dynamic_result = dynamics(t, Y, force_model, tau_fat, alpha_scale_factor, alpha_Km, alpha_tau_1, train, tau_c)
        for idx, val in enumerate(dynamic_result[2:]):
            assert round(val, 5) == round(result[idx], 5)
