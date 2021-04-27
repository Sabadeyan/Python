def erankyun(a,b,c):
    if a+b<=c or a+c<=b or b+c<=a:
        return "triangle with such sides does not exist"
    elif a==b and b==c and c==a:
        return "isosceles"
    elif a==b or b==c or a==c:
        return "2 side equal"
    else:
        return "simlpe"

print(erankyun(11,11,13))