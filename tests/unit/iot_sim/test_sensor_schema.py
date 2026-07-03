"""Tests for IoT sensor schema."""

import pytest

from fire_smoke_dt.iot_sim.sensor_schema import SensorConfig, SensorDevice


def test_sensor_config_from_yaml(tmp_path):
    yaml_content = """
devices:
  - device_id: "SD_01"
    node_id: "R1"
    sensor_type: "smoke"
    height_m: 2.8
  - device_id: "TEMP_01"
    node_id: "R2"
    sensor_type: "temperature"
"""
    
    yaml_file = tmp_path / "sensors.yaml"
    yaml_file.write_text(yaml_content)
    
    config = SensorConfig.from_yaml(yaml_file)
    
    assert len(config.devices) == 2
    assert config.devices[0].device_id == "SD_01"
    assert config.devices[0].node_id == "R1"
    assert config.devices[0].sensor_type == "smoke"
    assert config.devices[0].height_m == 2.8
    
    assert config.devices[1].device_id == "TEMP_01"
    assert config.devices[1].sensor_type == "temperature"
    assert config.devices[1].height_m == 2.5  # default value


def test_sensor_config_empty_yaml(tmp_path):
    yaml_file = tmp_path / "empty.yaml"
    yaml_file.write_text("")
    
    config = SensorConfig.from_yaml(yaml_file)
    assert len(config.devices) == 0
