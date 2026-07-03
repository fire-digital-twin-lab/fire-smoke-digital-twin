"""Tests for artifact envelope tracking and IO."""

import datetime

import pytest
from pydantic import ValidationError

from fire_smoke_dt.shared.io_utils import make_envelope
from fire_smoke_dt.shared.schema import ArtifactEnvelope


def test_envelope_rejects_missing_schema_version():
    with pytest.raises(ValidationError):
        ArtifactEnvelope(
            producer_version="1.0",
            config_hash="abc",
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            payload={"data": "test"},
        )


def test_make_envelope_deterministic_hash():
    payload = {"result": 42}
    config = {"b": 2, "a": 1}
    config2 = {"a": 1, "b": 2}
    
    env1 = make_envelope(payload, config, schema_version="1.0")
    env2 = make_envelope(payload, config2, schema_version="1.0")
    
    assert env1.config_hash == env2.config_hash


def test_write_read_roundtrip(tmp_path):
    from fire_smoke_dt.shared.io_utils import write_artifact, read_artifact
    
    payload = {"result": 42}
    config = {"a": 1}
    env = make_envelope(payload, config, schema_version="1.0")
    
    path = tmp_path / "artifact.json"
    write_artifact(path, env)
    
    env_read = read_artifact(path)
    assert env_read.schema_version == "1.0"
    assert env_read.payload == payload
    assert env_read.config_hash == env.config_hash
