""""""
# a = [
#     [1, 3, 5, 7],
#     [10, 11, 16, 20],
#     [23, 30, 34, 50]
# ]

#
# def sum(arg):
#     b = []
#     for list in a:
#         print(list)
#
#         for x in list:
#             b.append(x)
#     print(b)
#     # while b:
#     if arg in b:
#         return True
#     else:
#         return False
#
#
# # sum(50)
# print("--------------------")
# print(sum(50))
"""
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

示例:

给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
"""


class Solution(object):
    def twoSum(self, num, list):
        for num1 in range(len(list)):
            for num2 in range(num1 + 1, len(list)):
                if list[num1] + list[num2] == num:

                    return num1, num2


num = Solution()
n = num.twoSum(8, [2, 3, 4, 5, 6, 7])
print(n)
