list1=[45,5,2,6,1,78,45,66,11,4]
count=0
for tiv in range(len(list1)):
    for i in range(len(list1)-1-tiv):
        if list1[i]>list1[i+1]:
            list1[i],list1[i+1]=list1[i+1],list1[i]
        count+=1
print(list1)
print(count)
