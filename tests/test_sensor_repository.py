import pytest

from lib.repositories.sensor_repository import SensorRepository
from lib.entities.dual_pin_sensor import DualPinSensor
from lib.entities.single_pin_sensor import SinglePinSensor

# fixtures


@pytest.fixture()
def repo():
    return SensorRepository()

# tests


def test_finds_a_dual_pin_sensor(repo):
    dp_sensor = repo.find('OG')
    assert isinstance(dp_sensor, DualPinSensor)
    assert dp_sensor.id == 'OG'
    assert dp_sensor.pin_one == 12
    assert dp_sensor.pin_two == 13

def test_finds_a_single_pin_sensor(repo):
    sp_sensor = repo.find('OUTSIDE')
    assert isinstance(sp_sensor, SinglePinSensor)
    assert sp_sensor.id == 'OUTSIDE'
    assert sp_sensor.pin == 99

def test_returns_none_if_no_sensor_is_not_found(repo):
    sensor = repo.find('NONSENSE')
    assert sensor is None