# Framework for enforcing insertions

# Keeps track of all contracts being defined, 'class registration'
_contracts = { }
class Contract:

    # Own the "dot"
    @classmethod
    def __init_subclass__(cls):
        _contracts[cls.__name__] = cls


    # Own the 'dot' (Descriptor protocol)
    #   Check val then set the corresponding type of it to that val
    def __set__(self, instance, value):
        self.check(value)
        instance.__dict__[self.name] = value

    # Set the name of the type you want to check for
    def __set_name__(self, _cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        pass

# Doing this to reduce repition of having it be a part of every contract
# Making Typed to check on type generic
class Typed(Contract):
    type = None

    @classmethod
    def check(cls, value):
        try:
            assert isinstance(value, cls.type)  # Assert val is an inst of some type
        except AssertionError:
            print(f'Got {value}; expected {cls.type}')

        super().check(value)    # Allows for mul inheritance

class Integer(Typed):
    type = int

class String(Typed):
    type = str

class Float(Typed):
    type = float

# contract for expressing something is positive
class Positive(Contract):
    @classmethod
    def check(cls, value):
        # print(f'checking <{value}> for positive')
        try:
            assert value > 0
        except AssertionError:
            print(f'Got {value}; expected > 0.')

        super().check(value) # Allows for mul inheritance

# Contract for expressing the length of a val is greater than 0
class Nonempty(Contract):
    @classmethod
    def check(cls,value):
        try:
            assert '__len__' in dir(value) and len(value) > 0
        except AssertionError:
            val = value if value != '' else "''"
            print(f'Got {val}; expected {val} to have a __len__ attribute and that len({val}) > 0.')
        super().check(value)

# Multiple inheritencce, "composition"
class PositiveInteger(Positive, Integer):
    pass
class NonemptyString(String, Nonempty):
    pass

from functools import wraps
from inspect import signature
from collections import ChainMap

# Decorator
# Pass in a fnx and process it's sig
def checked(func):
    sig = signature(func)
    ann = ChainMap(
        func.__annotations__,
        func.__globals__.get('_annotations__', {})
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs) # Signature bind
        for (name, val) in bound.arguments.items():
            if name in ann:
                ann[name].check(val)
        return func(*args, **kwargs)

    return wrapper

print(f'\n>>> PositiveInteger.check(-2) #=>')
PositiveInteger.check(-2)
print(f'\n>>> PositiveInteger.check(2.3) #=>')
PositiveInteger.check(2.3)

@checked
def gcd(a: PositiveInteger, b: PositiveInteger):
    """
    Compute greatest common divisor
    """
    while b:
        (a, b) = (b, a % b)
    return a

print(f'\n>>> gcd(21, 35) #=> {gcd(21, 35)}')


# Recall how we used this in Heathrow-to-London
class BaseMeta(type):

    @classmethod
    def __prepare__(mcs, *args):
        return ChainMap({ }, _contracts)

    # Discards the contracts
    def __new__(mcs, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(mcs, name, bases, methods)

# A way to monitor the def of the child
class Base(metaclass=BaseMeta):
    # 3.6+
    @classmethod
    def __init_subclass__(cls):

        # Apply checked decorator
        for (name, val) in cls.__dict__.items():
            if callable(val):
                # apply @checked as a decorator to methods.
                setattr(cls, name, checked(val))

        # Instantiate the contracts
        for (name, val) in cls.__annotations__.items():
            contracts = val() # Integer()
            contracts.__set_name__ (cls, name)
            setattr(cls, name, contracts)

    def __init__(self, *args):
        ann = self.__annotations__
        try:
            assert len(args) == len(ann), f'Expected {len(ann)} arguments '
        except AssertionError:
            print(f'The {len(args)} arguments {args} don\'t pair up with the \n    {len(ann)} annotations {ann}')

        # 3.6 - Depends on ordered dictionary
        for (name, val) in zip(ann, args):
            setattr(self, name, val)

    def __repr__(self):
        # A list comprehension whose elements are generated by a lambda expression.
        # For each key in  self.__annotations__ the lambda expression is executed with argument getattr(self, key)
        # Note that the value of getattr(self, key) is bound to the parameter attr of the lambda expression.
        strs = [ ( lambda attr: repr(attr) + ': ' + repr(type(attr)) ) (getattr(self, key))
                                                                           for key in self.__annotations__]
        args = ', '.join(strs)
        return f'{type(self).__name__}({args})'

# Module Annotation 'typemap'
dx: PositiveInteger

class Player(Base):
    # Class annotations
    name: NonemptyString
    x: Integer
    y: Integer
    z: Integer

    def left(self, dx):
      self.x -= dx

    def right(self, dx):
        self.x += dx


print(f'\n\n>>> Player(\'Guido\', 0, 0)')

p = Player('Guido', 0, 0)
print(f'\n>>> p = Player(\'Guido\', 0, 0) #=>   {p}\n')

print(f'>>> p.x = \'23\'  #=>  ')
p.x = '23'
print(f'>>> p.name = \'\'  #=>  ')
p.name = ''
print(f'>>> p.name = 123  #=>  ')
p.name = 123
print(f'\n>>> p #=> {p}\n')

print('_contracts:')
for (contract, cls) in _contracts.items():
    print(f'{contract}:  {cls})')

print(f"\ntype.__prepare__('Player', 'Base') #=> {type.__prepare__('Player', 'Base')}")
d = BaseMeta.__prepare__('Player', 'Base')
print('\nd = BaseMeta.__prepare__(\'Player\', \'Base\')')
print(f'>>> d #=> \n      {d}')

d['x'] = 23
print('>>> d[\'x\'] = 23')
d['y'] = 45
print('>>> d[\'y\'] = 45')
print(f'>>> d #=>\n      {d}')
