from datetime import datetime

def is_time_in_range(start_time, end_time):
    current_time = datetime.now().time()
    if start_time < end_time:
        return start_time <= current_time <= end_time
    else: # crosses midnight
        return start_time <= current_time or current_time <= end_time