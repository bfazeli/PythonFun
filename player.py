from FunOfReinvention import Base, PositiveInteger
dx: PositiveInteger
class Player(Base):
    name: NonemptyString
    x: Integer
    y: Integer
    z: Integer
    def left(self, dx):
        self.x -= dx
    def right(self, dx):
        self.x += dx
print(f'\n\n >>> Player(\'Guido\', 0, 0)')

p = Player('Guido', 0, 0)
print(f'\n >>> p = Player(\'Guido\', 0, 0) #=> {p}\n')
print(f' >>> p.x = \'23\' #=> ')
p.x = '23'
print(f' >>> p.name = \'\' #=> ')
p.name = ''
print(f' >>> p.name = 123 #=> ')
p.name = 123
print(f'\n >>> p #=> {p}\n')