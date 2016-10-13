from datetime import timedelta

def wib_to_utc(time_wib):
    return time_wib + timedelta(hours=-7)
