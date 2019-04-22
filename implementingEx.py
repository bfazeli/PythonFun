
#   Week 5
#
#

# Prob 1&2
def gen():
    if False:
        yield False
for _ in gen():
    print("This should not be printed")
# Prob 3
def isEven(x):
    if x % 2 == 0:
        yield
for _ in isEven(0):
    print(0)
for _ in isEven(1):
    print(1)
for _ in isEven(2):
    print(2)
for _ in isEven(3):
    print(3)
for i in range(4, 20):
    for _ in isEven(i):
        print(i)
# Prob 4
def isTriple(x):
    if x % 3 == 0:
        yield
for i in range(20):
    for _ in isTriple(i):
        print(i)
# Prob 5
for i in range(20):
    for _ in isEven(i):
        print(i)
    for _ in isTriple(i):
        print(i)
# Prob 6
for i in range(20):
    for _ in isEven(i):
        for _ in isTriple(i):
            print(i)
#
class var:
    def __init__(self):
        self.bound = False
        self.value = None
Number = var()
def set(v, x):
    if v.bound:
        if v.value == x:
            yield False
    else:
        v.value = x
        v.bound = True
        yield
        v.bound = False
def get(v):
    if isinstance(v, var) and v.bound:
        return get(v.value)
    return v
#
# Prob 7
def isEven1(P):
    for i in (0, 10, 2):
        for _ in set(P, i):
            yield False
Number = var()
for _ in isEven1(Number):
    print(get(Number))
# Prob 8
def isTriple1(P):
    for i in range(0, 10, 3):
        for _ in set(P, i):
            yield False
Number = var()
for _ in isTriple1(Number):
    print(get(Number))
# Prob 9
for _ in set(Number, 66):
    print(get(Number))
for _ in set(Number, 99):
    print(get(Number))
# Prob 10&11 modified isEven1 & isTriple1
# Prob 12 Modified var and set to check if var is bound during exec
# Prob 13, doesn't print
for _ in set(Number, 4):
    for _ in isEven1(Number):
        print(get(Number))
# Prob 14 Extended set to allow loop body to run once iff it's trying to set a boundvar
# Prob 15
for _ in isEven1(Number):
    print(get(Number))
# These never run
for _ in isEven1(Number):
    for _ in set(Number, 4):
        print(get(Number))
for _ in set(Number, 4):
    for _ in isEven1(Number):
        print(get(Number))
# Prob 16
X, Y = var(), var()
for _ in isEven1(X):
    print(get(X))
for _ in isEven1(X):
    print(get(X))
for _ in set(Y, X):
    for _ in isEven1(X):
        print(get(X), get(Y))
# Prob 17 extended get to recursively call itself on the val of the var
# Prob 18
def unify(L, R):
    Lval, Rval = get(L), get(R)
    if isinstance(Lval, var):
        for _ in set(Lval, Rval):
            yield False
    elif isinstance(Rval, var):
        for _ in set(Rval, Lval):
            yield False
    else: # the two vals are the same
        if Lval == Rval:
            yield
X, Y = var(), var()
for _ in set(Y, 77):
    for _ in unify(X, Y):
        print("X", get(X), "Y", get(Y))
for _ in set(X, 88):
    for _ in unify(X, Y):
        print("X", get(X), "Y", get(Y))
for _ in set(X, 99):
    for _ in set(Y, 99):
        for _ in unify(X, Y):
            print("X", get(X), "Y", get(Y))
# Prob 19 Modified unify (added else clause)
for _ in unify(123, 123):
    print("yay it works")
for _ in unify(321, 123):
    print("boo it broke")




























