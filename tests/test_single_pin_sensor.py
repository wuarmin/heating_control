import pytest

from lib.entities.single_pin_sensor import SinglePinSensor

def test_init():
    sp_sensor = SinglePinSensor(id='OG', pin=14)
    assert isinstance(sp_sensor, SinglePinSensor)
    assert sp_sensor.id == 'OG'
    assert sp_sensor.pin == 14

def test_returns_current_temperature():
    sp_sensor = SinglePinSensor(id='OG', pin=14)
    assert sp_sensor.current_temperature() == 33

