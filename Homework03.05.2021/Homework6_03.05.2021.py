list1=[56,2,66,1,34,9,70,3,45,33,67,89,67,45]
list2=[]
# for i in list1:
#     if list1.count(i)==1:
#         list2.append(i)

for i in range(len(list1)):
    if list1.count(list1[i])==1:
        list2.append(list1[i])




print(list1)
print(list2)
