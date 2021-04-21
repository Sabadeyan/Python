from math import pi


def vol(radius):
    return (4*pi*radius**3)/3


def makeres(radius):
    return pi*radius**2


def paragic(radius):
    return 2*pi*radius

r=7


def yaniprint(radius):
    print("P=", paragic(radius))
    print("S=", makeres(radius))
    print("V=", vol(radius))
yaniprint(12)









# print(paragic(r))
#
#
#
#
#
#
#
#
# print(makeres(r))
#
#
# volume=vol(r)
# print(volume)

