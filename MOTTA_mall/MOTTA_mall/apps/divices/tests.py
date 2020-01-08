import time
# print(time.localtime(time.time()))
import os

# os.system('ls -la')
# os.system('python3 tests.py')
# os.system('pwd')

# lists = [1,2,34,5,6,8]
# # print(len(lists))
# os.system('pwd')
# os.system("cd ~ && pwd")
# os.system('pwd')
# print(os.getcwd())
#
# print(30000/(1-0.005) +3)
def num_list(num):
    return [i for index,i in enumerate(num) if i %2 ==0 and index%2==0]

num = [0,1,2,3,4,4,4,5,6,7,8,9,10,11,10,10,10]
result = num_list(num)
print(result)
print(num[::2])