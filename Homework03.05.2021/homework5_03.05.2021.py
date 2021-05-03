list1=[2,7,5,3,2,8,5,3,2]
list2=[]
for i in range(len(list1)):
    if list1[i] not in list2:
        list2.append(list1[i])
print(list2)
