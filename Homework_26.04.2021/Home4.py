def is_even(a):
    if a%2==0:
        return True
    return False
def xoranard(a):
    if is_even(a):
        return a**3
    return None
print(xoranard(13))
