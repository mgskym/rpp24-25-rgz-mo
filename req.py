import requests
from datetime import datetime


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

date = f'{day}/{month}/{year} {hour}:{minute}:{second}'
print(date)

a = requests.post('http://127.0.0.1:5000/add', json={
    "user_id": 4,
    "amount": 125.01,
    "category": "Еда, питание",
    "description": "Купил 3 шоколадных батончика",
    "created_at": date
})

print(a)