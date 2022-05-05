from datetime import date
import calendar
curr_date = date.today()
print(calendar.day_name[curr_date.weekday()])
