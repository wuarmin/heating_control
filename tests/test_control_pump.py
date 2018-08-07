import pytest
from datetime import datetime
from collections import namedtuple
from doubles import expect, InstanceDouble

from lib.interactors.control_pump import ControlPump
from lib.interactors.get_next_pump_schedule import GetNextPumpSchedule
from lib.repositories.pump_schedule_repository import PumpScheduleRepository
from lib.entities.pump_schedule import PumpSchedule
from lib.entities.pump import Pump

# fixtures


@pytest.fixture()
def pump():
    return Pump(id='OG', control_pin=14)
    

# tests


def test_initial_run_of_control_pump(pump):
    current_time = datetime(1990, 12, 24, 23, 30, 59, 000000)

    doubles = doubles_initial_run_of_control_pump(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.on == True

def doubles_initial_run_of_control_pump(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    next_schedule = PumpSchedule(
        pump_id=pump.id,
        next_start=datetime(1990, 12, 24, 23, 15, 59, 000000),
        next_stop=datetime(1990, 12, 25, 1, 00, 00, 000000)
    )
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(None)
    expect(pump_schedule_repo).create(next_schedule)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')
    expect(get_next_pump_schedule).__call__(current_time, pump).and_return(next_schedule)

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)




def test_switch_off_pump_if_next_schedule_is_none(pump):
    current_time = datetime(1990, 12, 24, 23, 30, 59, 000000)

    doubles = doubles_switch_off_pump_if_next_schedule_is_none(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.off == True

def doubles_switch_off_pump_if_next_schedule_is_none(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(None)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')
    expect(get_next_pump_schedule).__call__(current_time, pump).and_return(None)

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)




def test_switch_off_pump_if_current_time_is_before_next_start(pump):
    current_time = datetime(1990, 12, 24, 23, 30, 59, 000000)

    doubles = doubles_switch_off_pump_if_current_time_is_before_next_start(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.off == True

def doubles_switch_off_pump_if_current_time_is_before_next_start(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    next_schedule = PumpSchedule(
        pump_id=pump.id,
        next_start=datetime(1990, 12, 24, 23, 40, 59, 000000),
        next_stop=datetime(1990, 12, 25, 1, 00, 00, 000000)
    )
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(next_schedule)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)




def test_switch_off_pump_if_current_time_is_after_next_stop(pump):
    current_time = datetime(1990, 12, 24, 23, 30, 59, 000000)

    doubles = doubles_switch_off_pump_current_time_is_after_next_stop(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.off == True

def doubles_switch_off_pump_current_time_is_after_next_stop(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    next_schedule = PumpSchedule(
        pump_id=pump.id,
        next_start=datetime(1990, 12, 24, 23, 00, 59, 000000),
        next_stop=datetime(1990, 12, 24, 23, 30, 58, 000000)
    )
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(next_schedule)
    expect(pump_schedule_repo).delete(next_schedule)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)




def test_switch_on_pump_if_current_time_is_between_next_start_and_stop(pump):
    current_time = datetime(1990, 12, 24, 15, 30, 59, 000000)

    doubles = doubles_switch_on_pump_if_current_time_is_between_next_start_and_stop(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.on == True

def doubles_switch_on_pump_if_current_time_is_between_next_start_and_stop(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    next_schedule = PumpSchedule(
        pump_id=pump.id,
        next_start=datetime(1990, 12, 24, 15, 29, 59, 000000),
        next_stop=datetime(1990, 12, 24, 16, 00, 58, 000000)
    )
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(None)
    expect(pump_schedule_repo).create(next_schedule)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')
    expect(get_next_pump_schedule).__call__(current_time, pump).and_return(next_schedule)

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)




def test_keep_pump_switched_off_if_current_time_is_before_next_start(pump):
    pump.switch_off()
    current_time = datetime(1990, 12, 24, 15, 28, 59, 000000)

    doubles = doubles_keep_pump_switched_off_if_current_time_is_before_next_start(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.off == True

def doubles_keep_pump_switched_off_if_current_time_is_before_next_start(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    next_schedule = PumpSchedule(
        pump_id=pump.id,
        next_start=datetime(1990, 12, 24, 15, 29, 59, 000000),
        next_stop=datetime(1990, 12, 24, 16, 00, 58, 000000)
    )
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(None)
    expect(pump_schedule_repo).create(next_schedule)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')
    expect(get_next_pump_schedule).__call__(current_time, pump).and_return(next_schedule)

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)




def test_keep_pump_switched_off_and_delete_schedule_if_current_time_is_after_next_stop(pump):
    pump.switch_off()
    current_time = datetime(1990, 12, 24, 16, 1, 59, 000000)

    doubles = doubles_keep_pump_switched_off_and_delete_schedule_if_current_time_is_after_next_stop(current_time, pump)

    control_pump = ControlPump(
        pump_schedule_repo=doubles.pump_schedule_repo,
        get_next_pump_schedule=doubles.get_next_pump_schedule
    )
    control_pump(current_time=current_time, pump=pump)
    
    assert pump.off == True

def doubles_keep_pump_switched_off_and_delete_schedule_if_current_time_is_after_next_stop(current_time, pump):
    pump_schedule_repo = InstanceDouble('lib.repositories.pump_schedule_repository.PumpScheduleRepository')
    next_schedule = PumpSchedule(
        pump_id=pump.id,
        next_start=datetime(1990, 12, 24, 15, 29, 59, 000000),
        next_stop=datetime(1990, 12, 24, 16, 00, 58, 000000)
    )
    expect(pump_schedule_repo).find_by_pump_id('OG').and_return(None)
    expect(pump_schedule_repo).create(next_schedule)
    expect(pump_schedule_repo).delete(next_schedule)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')
    expect(get_next_pump_schedule).__call__(current_time, pump).and_return(next_schedule)

    Doubles = namedtuple('Doubles' , 'pump_schedule_repo get_next_pump_schedule')
    return Doubles(pump_schedule_repo, get_next_pump_schedule)