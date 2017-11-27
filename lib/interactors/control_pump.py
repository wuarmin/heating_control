from ..repositories.pump_control_rule_repository import PumpControlRuleRepository

class ControlPump(object):

  def __init__(self):
    self.pump_control_repo = PumpControlRuleRepository()

  def __call__(self, pump, current_time):
    self.pump = pump

  def rule(self):
    return self.pump_control_repo.find_for_pump_id(self.pump.id)