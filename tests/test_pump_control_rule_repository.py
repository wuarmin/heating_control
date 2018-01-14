import sys
import pytest
import datetime

from lib.repositories.pump_control_rule_repository import PumpControlRuleRepository
from lib.entities.pump_control_rule import PumpControlRule
from lib.entities.time_control import TimeControl

def test_find_for_pump_id():
  repo = PumpControlRuleRepository()
  
  pcr = repo.find_for_pump_id('OG')
  
  assert isinstance(pcr, PumpControlRule)
  assert pcr.start_temperature == 30
  assert pcr.nominal_temperature == 45
  assert pcr.time_slots == 4
  assert len(pcr.time_controls) == 2
  
  for tc in pcr.time_controls:
    assert isinstance(tc, TimeControl)

  first_tc = pcr.time_controls[0]
  assert first_tc.name == 'Night'
  assert first_tc.check_interval == 2400
  assert first_tc.outdoor_max == 15
  assert first_tc.start_at == datetime.time(0, 0)
  assert first_tc.end_at == datetime.time(3, 59)
