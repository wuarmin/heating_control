import sys
import pytest
import time
import collections

from ..lib.interactors.control_pump import ControlPump

def test_control_pump():
  Pump = collections.namedtuple('Pump', ['id'])
  ControlPump()(current_time=time.gmtime(), pump=Pump('OG'))
