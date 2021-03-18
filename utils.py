from datetime import datetime, time

import businesstime
from businesstime.holidays.usa import USFederalHolidays


def calculate_cycle_time(start, end):
    delta = end - start
    return delta.days + 1


def calculate_working_hours(start, end):
    # 5am EST to 7pm EST in UTC
    bt = businesstime.BusinessTime(
        business_hours=(time(10), time(23)),
        holidays=USFederalHolidays()
    )

    delta = bt.businesstimedelta(start, end)
    return int(delta.total_seconds() // 3600)


def to_size_enum(num_of_lines):
    if num_of_lines <= 50:
        return 'TINY'
    if num_of_lines <= 100:
        return 'SMALL'
    if num_of_lines <= 250:
        return 'MEDIUM'
    if num_of_lines <= 1000:
        return 'LARGE'
    if num_of_lines > 1000:
        return 'HUGE'


def to_cycle_time_enum(days_of_cycle):
    if days_of_cycle <= 1:
        return 'FAST'
    if days_of_cycle <= 2:
        return 'FINE'
    if days_of_cycle <= 3:
        return 'OKAY'
    if days_of_cycle <= 7:
        return 'CONCERNING'
    if days_of_cycle > 7:
        return 'ALARMING'
