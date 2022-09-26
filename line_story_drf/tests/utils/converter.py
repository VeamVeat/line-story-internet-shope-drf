from datetime import datetime


def convert_str_data_to_date(date):
    return datetime.strptime(date, '%Y-%m-%d').date()
