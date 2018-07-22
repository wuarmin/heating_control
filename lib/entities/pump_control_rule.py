class PumpControlRule(object):

    def __init__(self, start_temperature, nominal_temperature, temperature_sensor_id, time_slots, time_controls):
        self.start_temperature = start_temperature
        self.nominal_temperature = nominal_temperature
        self.temperature_sensor_id = temperature_sensor_id
        self.time_slots = time_slots
        self.time_controls = time_controls

    @property
    def temperature_delta(self):
        return self.nominal_temperature - self.start_temperature
