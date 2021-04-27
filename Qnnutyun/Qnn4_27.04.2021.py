def tari(x):
    if x % 4==0:
        if x%100==0:
            if x%400==0:
                return "Yes"
            else:
                return "No"
        else:
            return "Yes"
    else:
        return "No"
print(tari(1600))