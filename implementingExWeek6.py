#
#   Week 6
#
#
from unify import *
from sys import maxsize as max
# Prob 1
for _ in unify(123, 123):
    print("yay it works")
for _ in unify(123, 321):
    print("boo it broke")
X = var()
for _ in unify(X, 66):
    print(get(X))
for _ in unify(99, X):
    print(get(X))
print(get(X))
Y = var()
for _ in unify(X, 66):
    for _ in unify(X, Y):
        print(get(X), get(Y))
for _ in unify(X, Y):
    for _ in unify(X, 99):
        print(get(X), get(Y))
Z = var()
for _ in unify(X, Y):
    for _ in unify(Y, Z):
        for _ in unify(X, 1):
            print(get(X), get(Y), get(Z))
        for _ in unify(Y, 2):
            print(get(X), get(Y), get(Z))
        for _ in unify(Z, 3):
            print(get(X), get(Y), get(Z))
# Prob 2
def isEven(X):
    for i in range(0,10,2):
        unify(X, i)
        yield
for _ in isEven(2):
    print(get(X), "is even")
# Prob 3
def isTriple(X):
    for i in range(0, 10, 3):
        unify(X, i)
        yield
for _ in isTriple(X):
    print(get(X))
# Prob 4
def mult2or3(X):
    for _ in isEven(X):
        print(get(X))
    for _ in isTriple(X):
        print(get(X))
def mult2and3(X):
    for _ in isEven(X):
        for _ in isTriple(X):
            print(get(X))
for _ in mult2or3(X):
    print(get(X))
