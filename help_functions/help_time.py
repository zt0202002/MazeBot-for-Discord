from datetime import datetime, timedelta

def time_display(cur):
    start = cur['start']
    pause = timedelta(seconds=0) if cur['pause'] is None else datetime.now() - cur['pause']
    duration = timedelta(seconds=cur['duration'])
    now = datetime.now()
    t_played = now - start - pause
    return f'[{str(t_played).split(".")[0]}/{str(duration).split(".")[0]}]'

def total_time_display(num, cur):
    start = cur['start']
    pause = timedelta(seconds=0) if cur['pause'] is None else datetime.now() - cur['pause']
    duration = timedelta(seconds=num)
    now = datetime.now()
    total_time = duration - (now - start - pause)
    return f'[{str(total_time).split(".")[0]}]'