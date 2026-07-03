"""Tests for the scenario sampler to avoid Cartesian explosions."""

from fire_smoke_dt.scenario.sampler import sample_scenarios


def test_sampler_no_cartesian_explosion():
    # 10 factors with 4 values each = 4^10 = 1,048,576 combinations
    # This would take a lot of memory if fully materialized
    factors = {f"f{i}": [1, 2, 3, 4] for i in range(10)}
    
    # We sample just 10 scenarios
    samples = sample_scenarios(factors, count=10, seed=42)
    
    assert len(samples) == 10
    
    # Check that they have the right keys
    assert set(samples[0].keys()) == set(factors.keys())


def test_sampler_respects_seed():
    factors = {"a": [1, 2], "b": [3, 4, 5], "c": [6, 7]}
    
    s1 = sample_scenarios(factors, count=3, seed=42)
    s2 = sample_scenarios(factors, count=3, seed=42)
    s3 = sample_scenarios(factors, count=3, seed=99)
    
    assert s1 == s2
    assert s1 != s3


def test_sampler_no_duplicates_small_space():
    factors = {"a": [1, 2], "b": [3, 4]}  # 4 combinations total
    
    samples = sample_scenarios(factors, count=10, seed=42)
    
    # Should just return all 4, shuffled, no duplicates
    assert len(samples) == 4
    
    # Check uniqueness
    unique = {tuple(sorted(s.items())) for s in samples}
    assert len(unique) == 4
