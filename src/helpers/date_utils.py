import datetime

def timestamp_as_datetime(timestamp):
    """
    Convert a timestamp to a datetime object.
    """
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)