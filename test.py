from datetime import datetime, time, timedelta

t1 = time(9, 0)  # 10 am
t2 = time(8, 0)  # 9 am


def time_around(t1, t2, hrsdiff):
    dt1 = datetime.combine(datetime.min, t1)
    dt2 = datetime.combine(datetime.min, t2)
    if dt1 > dt2:
        return (dt1 - dt2) <= timedelta(hours=hrsdiff)
    return (dt2 - dt1) <= timedelta(hours=hrsdiff)


print(time_around(t1, t2, 1), time_around(t2, t1, 1))
