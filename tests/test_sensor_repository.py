import sys
import pytest
import time

from lib.repositories.sensor_repository import SensorRepository
# from lib.entities.sensor import Sensor

# fixtures
@pytest.fixture()
def repo():
  return SensorRepository()

# tests
@pytest.mark.skip(reason="no way of currently testing this")
def test_find():
  repo.find()
