from datetime import datetime

def days_from_today(input_date):
    date_format = "%Y-%m-%d"
    date1 = datetime.today()

    date2 = datetime.strptime(input_date, date_format)

    timedelta = date2 - date1

    return timedelta.days + 1