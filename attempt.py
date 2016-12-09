from datetime import *

def index_day(day):
    return {'Sunday': 0,
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6
            }[day]

reference = datetime(2016, 5, 1)
raw_input = input('You know the drill: ')
split_input = raw_input.split(' ')
temp_day = index_day(split_input[0])
temp_time = datetime.strptime(split_input[1], '%H:%M')
stored_date = datetime(2016, 5, 1 + temp_day,)
offset = timedelta(hours=temp_time.hour, minutes=temp_time.minute)
stored_date += offset
print(reference)
print(stored_date)
