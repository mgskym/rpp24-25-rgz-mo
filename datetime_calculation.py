from datetime import datetime

def current_datetime_sql():
    current_datetime = datetime.now()
    if len(str(current_datetime.day)) == 1:
        day = f'0{current_datetime.day}'
    else:
        day = current_datetime.day
    if len(str(current_datetime.month)) == 1:
        month = f'0{current_datetime.month}'
    else:
        month = current_datetime.month
    year = current_datetime.year

    if len(str(current_datetime.hour)) == 1:
        hour = f'0{current_datetime.hour}'
    else:
        hour = current_datetime.hour
    if len(str(current_datetime.minute)) == 1:
        minute = f'0{current_datetime.minute}'
    else:
        minute = current_datetime.minute
    if len(str(current_datetime.second)) == 1:
        second = f'0{current_datetime.second}'
    else:
        second = current_datetime.second

    result = f'{day}/{month}/{year} {hour}:{minute}:{second}'
    return result
