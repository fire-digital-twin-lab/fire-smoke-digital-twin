import numpy as np

from fire_smoke_dt.iot_sim.noise_models import delay


def test_delay_is_causal():
    out = delay(np.array([1.0, 2.0, 3.0]), 1)
    assert np.isnan(out[0])
    assert out[1:].tolist() == [1.0, 2.0]
