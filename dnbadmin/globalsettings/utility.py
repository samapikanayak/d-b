import pytz
from django.utils.dateparse import parse_datetime



def convert_datetime_timezone(date_to_convert, source_zone, dest_zone):
    # breakpoint()
    '''
    params:- date, local_timezone, destination_time_zone
    converts time of local time zone to destination time zone
    '''
    # date_to_convert = parse_datetime(date_to_convert)
    source_zone = pytz.timezone(source_zone)
    dest_zone = pytz.timezone(dest_zone)

    date_to_convert = date_to_convert.astimezone(dest_zone)
    date_to_convert = date_to_convert.strftime("%Y-%m-%d %H:%M:%S")

    return date_to_convert


