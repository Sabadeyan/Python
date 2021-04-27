def run(x,y):
    days=0

    while x<y:
        x=x*1.1
        days+=1
    return days
print(run(5,4))