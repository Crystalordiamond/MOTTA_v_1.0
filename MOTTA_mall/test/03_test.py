import datetime
abs = "2019-11-27 16:15:32"
aaaa = datetime.datetime.strptime(abs, "%Y-%m-%d %H:%M:%S")
# print(datetime.datetime.strptime("00:59:00", "%Y-%m-%d %H:%M:%S"))
time_data = datetime.datetime.strptime("2019-11-27 16:16:32", "%Y-%m-%d %H:%M:%S")
if time_data - aaaa > datetime.timedelta(days=1/24/60/10):
    print(time_data - aaaa)
    print(datetime.timedelta(days=1/24/60/60))