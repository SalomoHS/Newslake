import exception
from datetime import datetime

def _nnews(n_news):
    if n_news <= 0:
        raise exception.InvalidNNewsNumber(n_news)
    else:
        return

def _datetime(start_date, end_date):
    if (start_date!= None) and (end_date!=None):
        try:
            start_date = datetime.strptime(start_date,"%Y-%m-%d")
            end_date = datetime.strptime(end_date,"%Y-%m-%d")
        except ValueError:
            raise ValueError
        if end_date > datetime.now():
            raise exception.InvalidEndDateError()
        elif start_date > end_date:
            raise exception.InvalidDateRangeError()