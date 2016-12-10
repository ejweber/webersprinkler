from datetime import datetime

y = input('Enter weekday and time for program to run: ')
x = datetime.strptime(y, '%A %H:%M')
print(datetime.ctime(x))
