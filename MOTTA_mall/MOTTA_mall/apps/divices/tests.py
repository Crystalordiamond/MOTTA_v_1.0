import re
from functools import reduce

a = "2019-07-19 12:00:39"
b = "2019-07-19"

aa = re.match(r'^\S+', a)
print(aa.group())


# def list_dict_duplicate_removal():
#     data_list = [{"a": "123", "c": "132", "b": "321"}, {"a": "123", "c": "1233", "b": "321"},
#                  {"a": "123", "c": "14442", "b": "9"}]
#     run_function = lambda x, y: x if y in x else x + [y]
#     return reduce(run_function, [[], ] + data_list)
#
#
# if __name__ == '__main__':
#     print(list_dict_duplicate_removal())


class HostScheduler(object):

    def __init__(self, resource_list):

        self.resource_list = resource_list

    def MergeHost(self):
        allResource = []
        allResource.append(self.resource_list[0])
        for dict in self.resource_list:
            # print len(l4)
            k = 0
            for item in allResource:
                # print 'item'
                if dict['host'] != item['host']:
                    k = k + 1
                    # continue
                else:
                    break
                if k == len(allResource):
                    allResource.append(dict)
        taskhost = []
        for item in allResource:
            taskhost.append(item['host'])
        return taskhost


# 该函数实现嵌套列表中，按某一元素去重复
def deleteRepeat():
    # 1、列表中嵌套列表。按元素‘b’实现去重复
    # l1 = [['b', 1], ['b', 2], ['c', 3], ['a', 1], ['b', 1], ['b', 1]]
    # l2 = []
    # l2.append(l1[0])
    # for data in l1:
    #     print(len(l2))
    #     k = 0
    #     for item in l2:
    #         # print 'item'
    #         if data[0] != item[0]:
    #             k = k + 1
    #         else:
    #             break
    #         if k == len(l2):
    #             l2.append(data)
    # print("l2: ", l2)

    # 2、列表中嵌套字典。按键值host实现去重复
    l3 = [{'host': 'compute21', 'cpu': 2}, {'host': 'compute21', 'cpu': 2}, {'host': 'compute22', 'cpu': 2},
          {'host': 'compute23', 'cpu': 2}, {'host': 'compute22', 'cpu': 2}, {'host': 'compute23', 'cpu': 2},
          {'host': 'compute24', 'cpu': 2}]
    l4 = []
    l4.append(l3[0])
    for dict in l3:
        # print len(l4)
        k = 0
        for item in l4:
            # print 'item'
            if dict['host'] != item['host']:
                k = k + 1
                # continue
            else:
                break
            if k == len(l4):
                l4.append(dict)
    print("l4: ", l4)


if __name__ == '__main__':
    deleteRepeat()
    resource_list = [{'host': 'compute21', 'cpu': 2}, {'host': 'compute21', 'cpu': 2}, {'host': 'compute22', 'cpu': 2},
                     {'host': 'compute23', 'cpu': 2}, {'host': 'compute22', 'cpu': 2}, {'host': 'compute23', 'cpu': 2},
                     {'host': 'compute24', 'cpu': 2}]

    hostSchedule = HostScheduler(resource_list)
    taskhost = hostSchedule.MergeHost()
    print('taskhost: ')
    print(taskhost)
