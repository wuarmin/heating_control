import sys
import pytest
import datetime
from collections import namedtuple
from datetime import datetime, time
from doubles import expect, InstanceDouble

from lib.entities.pump_control_rule import PumpControlRule
from lib.entities.pump_schedule import PumpSchedule
from lib.entities.time_control import TimeControl
from lib.interactors.get_next_pump_schedule import GetNextPumpSchedule

# fixtures


@pytest.fixture()
def pump():
    return namedtuple('Pump', ['id'])

# tests


def test_next_schedule_returns_none_because_subsequent_schedule_will_start_before_current_will_be_applied(pump):
    doubles = doubles_next_schedule_returns_none_because_subsequent_schedule_will_start_before_current_will_be_applied() 

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 3, 55, 59, 000000))

    assert next_schedule is None

def doubles_next_schedule_returns_none_because_subsequent_schedule_will_start_before_current_will_be_applied():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(22),
            end_at=time(
                3,
                59)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(4),
            end_at=time(8)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(sensor).current_temperature().and_return(33)

    outside_sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(outside_sensor).current_temperature().and_return(14)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')
    expect(sensor_repo).find('OUTSIDE').and_return(outside_sensor)
    expect(sensor_repo).find('OG').and_return(sensor)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)




def test_next_schedule_returns_a_schedule_which_is_in_current_time_control(pump):
    doubles = doubles_next_schedule_returns_a_schedule_which_is_in_current_time_control() 

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))

    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 25, 0, 0, 19)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 1, 57, 39)

def doubles_next_schedule_returns_a_schedule_which_is_in_current_time_control():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=8800,
            outdoor_max=15,
            start_at=time(22),
            end_at=time(21, 59)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(sensor).current_temperature().and_return(33)

    outside_sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(outside_sensor).current_temperature().and_return(14)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')
    expect(sensor_repo).find('OUTSIDE').and_return(outside_sensor)
    expect(sensor_repo).find('OG').and_return(sensor)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)




def test_next_schedule_returns_a_schedule_which_is_in_current_time_control_but_overnight(pump):
    doubles = doubles_next_schedule_returns_a_schedule_which_is_in_current_time_control_but_overnight() 

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )

    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 0, 30, 59)

def doubles_next_schedule_returns_a_schedule_which_is_in_current_time_control_but_overnight():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(22),
            end_at=time(
                3,
                59)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(4),
            end_at=time(8)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(sensor).current_temperature().and_return(33)

    outside_sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(outside_sensor).current_temperature().and_return(14)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')
    expect(sensor_repo).find('OUTSIDE').and_return(outside_sensor)
    expect(sensor_repo).find('OG').and_return(sensor)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)




def test_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_same_day(pump):
    doubles = doubles_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_same_day() 

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 24, 23, 51, 0)

def doubles_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_same_day():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(23),
            end_at=time(23, 50)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(23, 51),
            end_at=time(8)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(sensor).current_temperature().and_return(33)

    outside_sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(outside_sensor).current_temperature().and_return(14)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')
    expect(sensor_repo).find('OUTSIDE').and_return(outside_sensor)
    expect(sensor_repo).find('OG').and_return(sensor)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)




def test_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_next_day(pump):
    doubles = doubles_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_next_day()

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert isinstance(next_schedule, PumpSchedule)
    assert next_schedule.pump_id == 'OG'
    assert next_schedule.next_start == datetime(1989, 12, 24, 23, 42, 59)
    assert next_schedule.next_stop == datetime(1989, 12, 25, 0, 6, 0)

def doubles_starts_at_current_time_control_but_ends_with_start_of_subsequent_control_next_day():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Night",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(23),
            end_at=time(0, 5)),
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(0, 6),
            end_at=time(8)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(sensor).current_temperature().and_return(33)

    outside_sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(outside_sensor).current_temperature().and_return(14)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')
    expect(sensor_repo).find('OUTSIDE').and_return(outside_sensor)
    expect(sensor_repo).find('OG').and_return(sensor)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)




def test_returns_none_if_no_time_control_is_set(pump):
    doubles = doubles_returns_none_if_no_time_control_is_set()

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 23, 30, 59, 000000))
    
    assert next_schedule is None

def doubles_returns_none_if_no_time_control_is_set():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(0,6),
            end_at=time(8)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)




def test_returns_none_if_max_temperature_is_to_high(pump):
    doubles = doubles_returns_none_if_max_temperature_is_to_high()

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 4, 30, 59, 000000))    
    
    assert next_schedule is None

def doubles_returns_none_if_max_temperature_is_to_high():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(0,6),
            end_at=time(8)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(sensor).current_temperature().and_return(10)

    outside_sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(outside_sensor).current_temperature().and_return(15)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')
    expect(sensor_repo).find('OG').and_return(sensor)
    expect(sensor_repo).find('OUTSIDE').and_return(outside_sensor)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)




def test_returns_none_if_current_temperature_is_bigger_than_nominal_temperature(pump):
    doubles = doubles_returns_none_if_current_temperature_is_bigger_than_nominal_temperature()

    get_next_pump_schedule = GetNextPumpSchedule(
        pump_control_rule_repo=doubles.pump_control_rule_repo,
        sensor_repo=doubles.sensor_repo
    )
    next_schedule = get_next_pump_schedule(pump=pump('OG'), current_date_time=datetime(1989, 12, 24, 4, 30, 59, 000000))    
    
    assert next_schedule is None

def doubles_returns_none_if_current_temperature_is_bigger_than_nominal_temperature():
    pump_control_rule_repo = InstanceDouble('lib.repositories.pump_control_rule_repository.PumpControlRuleRepository')
    rule_for_test = PumpControlRule(nominal_temperature=45, start_temperature=30, temperature_sensor_id='OG', time_slots=4, time_controls=[
        TimeControl(
            name="Morning",
            check_interval=3600,
            outdoor_max=15,
            start_at=time(0,6),
            end_at=time(6)),
    ])
    expect(pump_control_rule_repo).find_for_pump_id('OG').and_return(rule_for_test)

    sensor = InstanceDouble('lib.entities.single_pin_sensor.SinglePinSensor')
    expect(sensor).current_temperature().and_return(46)

    sensor_repo = InstanceDouble('lib.repositories.sensor_repository.SensorRepository')
    expect(sensor_repo).find('OG').and_return(sensor)

    get_next_pump_schedule = InstanceDouble('lib.interactors.get_next_pump_schedule.GetNextPumpSchedule')

    Doubles = namedtuple('Doubles' , 'pump_control_rule_repo sensor_repo')
    return Doubles(pump_control_rule_repo, sensor_repo)