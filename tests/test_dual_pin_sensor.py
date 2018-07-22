import pytest

from lib.entities.dual_pin_sensor import DualPinSensor

def test_init():
    dp_sensor = DualPinSensor(id='OG', pin_one=14, pin_two=15)
    assert isinstance(dp_sensor, DualPinSensor)
    assert dp_sensor.id == 'OG'
    assert dp_sensor.pin_one == 14
    assert dp_sensor.pin_two == 15

def test_returns_current_temperature():
    dp_sensor = DualPinSensor(id='OG', pin_one=14, pin_two=15)
    assert dp_sensor.current_temperature() == 33.0