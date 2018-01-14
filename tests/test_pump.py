import sys
import pytest
import datetime

from lib.entities.pump import Pump
from lib.entities.pump_control_rule import PumpControlRule

def test_init():
  pump = Pump(id='OG', control_pin=14)
  assert isinstance(pump, Pump)
  assert pump.id           == 'OG'
  assert pump.control_pin  == 14

def test_switch_on_off():
  pump = Pump(id='OG', control_pin=14)
  pump.switch_off()
  pump.on = False
  pump.switch_on()
  pump.on = True

def test_returns_its_rule():
  pump = Pump(id='OG', control_pin=14)
  rule = pump.rule
  assert isinstance(rule, PumpControlRule)
  assert rule.start_temperature   == 30
  assert rule.nominal_temperature == 45
  assert rule.time_slots          == 4