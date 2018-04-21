import datetime
import time


def date_to_timestamp(date_str, format='%Y-%m-%d'):
    return int(time.mktime(datetime.datetime.strptime(date_str, format).timetuple()))


def timestamp_to_date(timestamp, format='%Y-%m-%d'):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime(format)


if __name__ == '__main__':
    timestamp = date_to_timestamp('2018-01-01')
    print(timestamp)
    print(timestamp_to_date(timestamp))