import pytest
import numbers
from model.calcium_dynamics import get_Ri, dCN


@pytest.mark.parametrize("pulse_array, R0, tau_c, Ri", [
    ([1, 5, 10], 2, 1, 1.0067379),
    ([1], 2, 1, 1),
    ([1], 2, 0, 0),
    ([1], 0, 1, 0),
    ([0], 2, 1, 1),
    ([1], 2, -1, 0),
    ([1], -2, 1, 0),
    (["1"], "1", "test", 0)
])
def test_get_Ri(pulse_array, R0, tau_c, Ri):
    if not isinstance(R0, numbers.Number) or not isinstance(tau_c, numbers.Number) \
            or not (hasattr(pulse_array, '__len__')):
        with pytest.raises(TypeError):
            get_Ri(pulse_array, R0, tau_c)
    elif len(pulse_array) < 0 or R0 <= 0 or tau_c <= 0:
        with pytest.raises(Exception):
            get_Ri(pulse_array, R0, tau_c)
    else:
        assert round(get_Ri(pulse_array, R0, tau_c), 5) == round(Ri, 5)


@pytest.mark.parametrize("t, CN, train, tau_c, Km, dCN_result", [
    (11, 20, [1, 5, 10], 2, 1, -9.63908),
    (2, 20, [1], 2, 1, -9.69673),
    (0, 20, [1], 2, 1, -10.0),
    (2, 0, [1], 2, 1, 0.30327),
    (2, 20, [1], 2, 0, -9.69673),
    (2, 20, [1], 0, 1, 0),
    (2, 20, [0], 2, 1, -9.81606),
    (2, 20, [1], 2, -1, 0),
    (2, 20, [1], -2, 1, 0),
    (-2, 20, [1], -2, 1, 0),
    (2, -20, [1], -2, 1, 0),
    ("2", "20", ["1"], "1", "test", 0)
])
def test_dCN(t, CN, train, tau_c, Km, dCN_result):
    if not isinstance(t, numbers.Number) or not isinstance(CN, numbers.Number) \
            or not isinstance(tau_c, numbers.Number) or not isinstance(Km, numbers.Number) \
            or not (hasattr(train, '__len__')):
        with pytest.raises(TypeError):
            dCN(t, CN, train, tau_c, Km)
    elif len(train) < 0 or t < 0 or tau_c <= 0 or Km < 0:
        with pytest.raises(Exception):
            dCN(t, CN, train, tau_c, Km)
    else:
        assert round(dCN(t, CN, train, tau_c, Km), 5) == round(dCN_result, 5)
