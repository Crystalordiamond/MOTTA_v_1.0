# 定 nums = [2, 7, 11, 15], target = 9
#
# 因为 nums[0] + nums[1] = 2 + 7 = 9
# 所以返回 [0, 1]
#
# def add(target, nums):
#     for index, i in enumerate(nums):
#         a = target - i
#         if a in nums and nums.index(a) != index:
#             return index, nums.index(a)
#
#
# print(add(18, [8, 9, 11, 9]))
# 1 在不改变列表中数据排列结构的前提下，找出以下列表中最接近最大值和最小值的平均值 的数
li = [-100, 1, 3, 2, 7, 6, 120, 121, 140, 23, 411, 99, 243, 33, 85, 55]

max = li[0]
min = li[0]
value = li[0]


def num(li):
    global max, min, value
    for i in li:
        if i > max:
            max = i
        if i < min:
            min = i
    a = (max + min) / 2
    print("平均数:", a)
    for i in li:
        if abs(a - i) < abs(a - value):
            value = i


num(li)
print("最大值：", max)
print("最小值：", min)
print(value)



