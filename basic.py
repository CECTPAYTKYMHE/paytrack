# import requests

# endpoint = 'http://localhost:8000/home/'

# get_response = requests.get(endpoint, json = {'query' : 'hello world'})
# print(get_response.text)

from datetime import date, timedelta, datetime
import calendar

def all_dates_current_month():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    delta = last_date - first_date
    print(first_date,last_date)
all_dates_current_month()
