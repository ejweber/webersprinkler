from datetime import *

# return integer from 0-6 based on day input by user
def index_day(day):
    return {'Sunday': 0,
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6
            }[day]

# take day and time input by user and 'normalize' to week beggining 5/1/16
def normalize_input_datetime():
    raw_input = input('You know the drill: ')
    split_input = raw_input.split(' ')
    temp_day = index_day(split_input[0])
    temp_time = datetime.strptime(split_input[1], '%H:%M')
    stored_date = datetime(2016, 5, 1 + temp_day,)
    offset = timedelta(hours=temp_time.hour, minutes=temp_time.minute)
    stored_date += offset
    print(stored_date)
    return(stored_date)

# take current time and 'normalize' week beggining 5/1/16
def normalize_current_datetime():
    now = datetime.now()
    day = datetime.strftime(now, '%w')
    stored_date = datetime(2016, 5, 1 + int(day),
                           now.hour, now.minute, now.second)
    print(stored_date)
    return(stored_date)

# calculate the time until each event should run next using 'normalized' times
def schedule_stored_datetime(stored_datetime, current_datetime):
    subtraction = stored_datetime - current_datetime
    print(subtraction)
    if subtraction < timedelta():
        modified_subtraction = subtraction + timedelta(7)
        print(modified_subtraction)
    

stored_datetime = normalize_input_datetime()
current_datetime = normalize_current_datetime()
schedule_stored_datetime(stored_datetime, current_datetime)
