from datetime import datetime
import time

def retreive_date():
    raw_datetime = input('Enter date in mm/dd/yy hh:mm format: ')
    stripped_datetime = datetime.strptime(raw_datetime, '%x %H:%M')
    print(stripped_datetime)
    return stripped_datetime

def schedule_next(stripped_datetime):
    return time.mktime(datetime.timetuple(stripped_datetime))
    
stripped_datetime = retreive_date()
abs_time = schedule_next(stripped_datetime, '%A %H:%M')
print(abs_time)
print(time.time())
