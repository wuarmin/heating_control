from datetime import datetime


class TimeControl(object):

    def __init__(self, name, check_interval, outdoor_max, start_at, end_at):
        self.name = name
        self.check_interval = check_interval
        self.outdoor_max = outdoor_max
        self.start_at = start_at
        self.end_at = end_at

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
