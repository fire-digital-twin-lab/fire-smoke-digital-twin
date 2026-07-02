from fire_smoke_dt.dataset.split_builder import split_groups


def test_split_has_no_overlap():
    split = split_groups([f"S{i}" for i in range(20)], train=0.7, val=0.15, seed=1)
    train, val, test = map(set, [split["train"], split["validation"], split["test"]])
    assert not train & val
    assert not train & test
    assert not val & test
