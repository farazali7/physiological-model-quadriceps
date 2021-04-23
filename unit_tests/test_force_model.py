import pytest
import numbers
from model.force_model import ForceModel


@pytest.fixture
def force_model():
    """Returns a ForceModel object"""
    return ForceModel(1, 2, 1, 1)


@pytest.mark.parametrize("force_scale_factor, Km, tau_1, tau_2", [
    (1, 2, 1, 1),
    (-1, 2, 1, 1),
    (1, -2, 1, 1),
    (1, 2, -1, 1),
    (1, 2, 1, -1),
    (0, 2, 1, 1),
    (1, 0, 1, 1),
    (1, 2, 0, 1),
    (1, 2, 1, 0),
    ("1", "1", "test", "1")
])
def test_force_model(force_scale_factor, Km, tau_1, tau_2):
    if not isinstance(force_scale_factor, numbers.Number) or not isinstance(Km, numbers.Number) \
            or not isinstance(tau_1, numbers.Number) or not isinstance(tau_2, numbers.Number):
        with pytest.raises(TypeError):
            ForceModel(force_scale_factor, Km, tau_1, tau_2)
    elif force_scale_factor < 0 or Km < 0 or tau_1 < 0 or tau_2 <= 0:
        with pytest.raises(Exception):
            ForceModel(force_scale_factor, Km, tau_1, tau_2)


@pytest.mark.parametrize("F, CN, force_scale_factor, tau_1, Km, dF_result", [
    (1, 2, 1, 2, 1, 0.29167),
    (2, 2, 1, 2, 1, -0.08333),
    (2, 20, 1, 0, 1, -1.14762),
    (2, 20, 0, 2, 1, -0.67742),
    (2, 20, 1, 2, -1, 0.39746),
    (2, 20, 1, -2, 1, 0),
    ("2", "20", "1", "1", "test", 0)
])
def test_dF(F, CN, force_scale_factor, tau_1, Km, dF_result, force_model):
    if not isinstance(F, numbers.Number) or not isinstance(CN, numbers.Number) \
            or not isinstance(force_scale_factor, numbers.Number) or not isinstance(tau_1, numbers.Number) \
            or not isinstance(Km, numbers.Number):
        with pytest.raises(TypeError):
            force_model.dF(F, CN, force_scale_factor, tau_1, Km)
    elif force_scale_factor < 0 or tau_1 < 0:
        with pytest.raises(Exception):
            force_model.dF(F, CN, force_scale_factor, tau_1, Km)
    else:
        assert round(force_model.dF(F, CN, force_scale_factor, tau_1, Km), 5) == round(dF_result, 5)
