from datetime import datetime, timedelta

# potentially help loading user/guild history playtime, may break being longer than 24 hours
def time_str_to_delta(str): # str = '13:42:10'
    dt = datetime.strptime(str, "%H:%M:%S")
    total_sec = dt.hour*3600 + dt.minute*60 + dt.second  # total seconds calculation
    td = timedelta(seconds=total_sec)
    return td

def time_played_int(cur):
    start = cur['start']
    pause = timedelta(seconds=0) if cur['pause'] is None else datetime.now() - cur['pause']
    now = datetime.now()
    t_played = now - start - pause
    return str(t_played)

def time_display(cur):
    start = cur['start']
    pause = timedelta(seconds=0) if cur['pause'] is None else datetime.now() - cur['pause']
    duration = timedelta(seconds=cur['duration'])
    now = datetime.now()
    t_played = now - start - pause
    return f'[{str(t_played).split(".")[0]}/{str(duration).split(".")[0]}]'

def total_time_display(num, curr):
    start = curr['start']
    pause = timedelta(seconds=0) if curr['pause'] is None else datetime.now() - curr['pause']
    duration = timedelta(seconds=num)
    curr_duration = timedelta(seconds=curr['duration'])
    now = datetime.now()
    total_time = duration + curr_duration - (now - start - pause)
    return f'[{str(total_time).split(".")[0]}]'