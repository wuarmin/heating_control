from ..repositories.pump_control_rule_repository import PumpControlRuleRepository

class Pump(object):

  def __init__(self, id, control_pin):
    self.id = id
    self.control_pin = control_pin

  @property
  def rule(self):
    return PumpControlRuleRepository().find_for_pump_id(self.id)
