import math



# 1) Vypocet obvodu kruhu
r = 5
print('Hello world!')


def polomer(x):
    return math.pi * x * 2


print(f"Obvod kruhu s polomerom {r} je {polomer(r)}")
# 2) pytagorova veta

a = 3
b = 4


def prepona(x, y):
    return math.sqrt(x ** 2 + y ** 2)


print(f"Prepona pravouhleho trojuholnika s odvesnami {a} a {b} je {prepona(a,b)}")


# 3) praca s textom

s = "Tato uloha pracuje s retazcom"

print(s[::2])
