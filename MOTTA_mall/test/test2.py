list = []
a = {"a": "11", "b": 14}
b = {"c": "11", "bd": ""}
c = {"a": "11", "b": 16}

list.append(a)
list.append(b)
list.append(c)
# print(list)
print(a.update(b))
print(a)