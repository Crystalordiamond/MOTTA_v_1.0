import copy

alist = [2, 4, 5, 6, 8, 7, 7, 7, 7]
# # 第一种方法
blist = copy.deepcopy(alist)
for i in alist:
    if i % 2 == 0:
        blist.remove(i)
print(blist)
#
# # 第二种方法
b = [i for i in alist if i % 2 != 0]
print(b)
#
# # 第三种方法
for i in alist[::-1]:
    if i % 2 == 0:
        alist.remove(i)
print(alist)
# 第四种方法
while 7 in alist:
    alist.remove(7)
print(alist)


"""
引用/深拷贝/浅拷贝
先分为：
    不可变对象：number（数字）string（字符串） tuple（元组）:number和string在 a = 1,b =1 ,a=b=1,内存地址一样。
                                                        tuple a=b=1地址一样,a =1 b=1时候地址不一样
    可变对象：list[],dict{},set()
"""
a, b, c = 14325243532452143214, "aa", ("aa",)
a1, b1, c1 = a, b, c

#