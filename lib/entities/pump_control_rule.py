class PumpControlRule(object):

    def __init__(self, start_temperature, nominal_temperature, time_slots, time_controls):
        self.start_temperature = start_temperature
        self.nominal_temperature = nominal_temperature
        self.time_slots = time_slots
        self.time_controls = time_controls

    @property
    def temperature_delta(self):
        return self.nominal_temperature - self.start_temperature
