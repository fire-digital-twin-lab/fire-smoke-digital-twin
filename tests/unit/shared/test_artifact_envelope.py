"""Tests for artifact envelope tracking and IO."""

import datetime

import pytest
from pydantic import ValidationError

from fire_smoke_dt.shared.io_utils import make_envelope, read_artifact, write_artifact
from fire_smoke_dt.shared.schema import ArtifactEnvelope
from fire_smoke_dt.shared.validation import validate_envelope

SAMPLE_UNITS = {"room_area": "m2", "HRR": "kW", "temperature": "C"}


def test_envelope_rejects_missing_schema_version():
    with pytest.raises(ValidationError):
        ArtifactEnvelope(
            producer_version="1.0",
            config_hash="abc",
            created_at=datetime.datetime.now(datetime.UTC).isoformat(),
            units=SAMPLE_UNITS,
            payload={"data": "test"},
        )


def test_envelope_rejects_missing_units():
    with pytest.raises(ValidationError):
        ArtifactEnvelope(
            schema_version="1.0",
            producer_version="1.0",
            config_hash="abc",
            created_at=datetime.datetime.now(datetime.UTC).isoformat(),
            payload={"data": "test"},
        )


def test_validate_envelope_rejects_empty_units():
    env = ArtifactEnvelope(
        schema_version="1.0",
        producer_version="1.0",
        config_hash="abc",
        created_at=datetime.datetime.now(datetime.UTC).isoformat(),
        units={},
        payload={"data": "test"},
    )
    with pytest.raises(ValueError, match="units must not be empty"):
        validate_envelope(env)


def test_make_envelope_deterministic_hash():
    payload = {"result": 42}
    config = {"b": 2, "a": 1}
    config2 = {"a": 1, "b": 2}

    env1 = make_envelope(payload, config, schema_version="1.0", units=SAMPLE_UNITS)
    env2 = make_envelope(payload, config2, schema_version="1.0", units=SAMPLE_UNITS)

    assert env1.config_hash == env2.config_hash


def test_write_read_roundtrip(tmp_path):
    payload = {"result": 42}
    config = {"a": 1}
    env = make_envelope(payload, config, schema_version="1.0", units=SAMPLE_UNITS)

    path = tmp_path / "artifact.json"
    write_artifact(path, env)

    env_read = read_artifact(path)
    assert env_read.schema_version == "1.0"
    assert env_read.payload == payload
    assert env_read.config_hash == env.config_hash
    assert env_read.units == SAMPLE_UNITS
