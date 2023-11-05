from datetime import datetime

def to_date(date_string): 
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))
