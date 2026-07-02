import numpy as np

from fire_smoke_dt.shared.labels import arrival_time_abs, smoke_label, time_to_arrival


def test_smoke_label_requires_persistence():
    values = np.array([0.0, 24.0, 10.0, 24.0, 25.0])
    assert smoke_label(values, threshold=23.93, persistence_steps=2).tolist() == [0, 0, 0, 0, 1]


def test_arrival_and_tta_keep_invalid_mask():
    labels = np.array([[0, 0, 1], [0, 0, 0]])
    arrival, valid = arrival_time_abs(labels, np.array([0.0, 10.0, 20.0]))
    assert valid.tolist() == [1, 0]
    assert arrival[0] == 20.0 and np.isnan(arrival[1])
    tta = time_to_arrival(arrival, 5.0)
    assert tta[0] == 15.0 and np.isnan(tta[1])
