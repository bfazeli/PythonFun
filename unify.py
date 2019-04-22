class var():
    def __init__(self):
        self.bound = False
        self.value = None
def _assign(v, x): # _assign to remind people to use unify instead
    if not v.bound:
       v.value = x
       v.bound = True
       yield
       v.bound = False
def get(v):
    if isinstance(v, var) and v.bound: 
        return get(v.value)
    return v
def unify(L, R):
    Lval, Rval = get(L), get(R)
    if isinstance(Lval, var):
        for _ in _assign(Lval, Rval): 
            yield
    elif isinstance(Rval, var):
        for _ in _assign(Rval, Lval):
            yield
    else:
        if Lval == Rval:
            yield
