import re
from month import month_day

def day_by_table(ws, day_week, parity):
    multiplace_last_cell = 0
    multiplace_first_cell = 0
    if bool(re.search('понедельник', day_week)) is True or bool(re.search('ПОНЕДЕЛЬНИК', day_week)) is True or bool(re.search('Понедельник', day_week)) is True:
        if parity == 1:
            multiplace_last_cell = 1
            multiplace_first_cell = 0
        elif parity == 2:
            multiplace_last_cell = 7
            multiplace_first_cell = 6
        return month_day(ws, parity, multiplace_first_cell, multiplace_last_cell)
    elif bool(re.search('вторник', day_week)) is True or bool(re.search('ВТОРНИК', day_week)) is True or bool(re.search('Вторник', day_week)) is True:
        if parity == 1:
            multiplace_last_cell = 2
            multiplace_first_cell = 1
        elif parity == 2:
            multiplace_last_cell = 8
            multiplace_first_cell = 7
        return month_day(ws, parity,multiplace_first_cell,multiplace_last_cell)
    elif bool(re.search('среда', day_week)) is True or bool(re.search('СРЕДА', day_week)) is True or bool(re.search('Среда', day_week)) is True:
        if parity == 1:
            multiplace_last_cell = 3
            multiplace_first_cell = 2
        elif parity == 2:
            multiplace_last_cell = 9
            multiplace_first_cell = 8
        return month_day(ws, parity,multiplace_first_cell,multiplace_last_cell)
    elif bool(re.search('четверг', day_week)) is True or bool(re.search('ЧЕТВЕРГ', day_week)) is True or bool(re.search('Четверг', day_week)) is True:
        if parity == 1:
            multiplace_last_cell = 4
            multiplace_first_cell = 3
        elif parity == 2:
            multiplace_last_cell = 10
            multiplace_first_cell = 9
        return month_day(ws, parity,multiplace_first_cell,multiplace_last_cell)
    elif bool(re.search('пятница', day_week)) is True or bool(re.search('ПЯТНИЦА', day_week)) is True or bool(re.search('Пятница', day_week)) is True:
        if parity == 1:
            multiplace_last_cell = 5
            multiplace_first_cell = 4
        elif parity == 2:
            multiplace_last_cell = 11
            multiplace_first_cell = 10
        return month_day(ws, parity,multiplace_first_cell,multiplace_last_cell)
    elif bool(re.search('суббота', day_week)) is True or bool(re.search('СУББОТА', day_week)) is True or bool(re.search('Суббота', day_week)) is True:
        if parity == 1:
            multiplace_last_cell = 6
            multiplace_first_cell = 5
        elif parity == 2:
            multiplace_last_cell = 11.7
            multiplace_first_cell = 11
        return month_day(ws, parity,multiplace_first_cell,multiplace_last_cell)