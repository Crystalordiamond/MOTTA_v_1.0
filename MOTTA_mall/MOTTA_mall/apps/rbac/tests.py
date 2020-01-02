import random, time

print("生成1-50的随机整数", random.randint(1, 50))
print("生成1-50的随机偶数", random.randrange(0, 50, 2))
print("生成随机浮点数", random.random())
print("生成1-10的随机浮点数", random.uniform(1, 10))
print("生成随机字符串", random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()'))
print("生成5个随机字符串列表形式", random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 5))
print("生成5个随机字符串字符串形式", ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 5)))
items = [1, 2, 3, 4, 5, 'u', 10, 'y']
random.shuffle(items)
print("重新生成随机列表", items)

print("生成当前时间戳：",time.time())
print("格式化时间戳为本地的时间:",time.localtime(time.time()))
print("最简单的获取可读的时间形式",time.asctime(time.localtime(time.time())))
time_data = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
data_time = time.strptime('2019-1-1 23:8:0','%Y-%m-%d %H:%M:%S')
print("将时间转化为格式化字符串:",time_data)
print("将字符串转化为时间类型:",data_time)
