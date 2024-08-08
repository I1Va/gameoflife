import random
class Cell:
    def __init__(self, i, j, field):
        self.i = i
        self.j = j
        self.field = field
        self.N = len(field)
        self.M = len(field[0])
        al = [[self.i + 1, self.j], [self.i - 1, self.j], [self.i, self.j + 1], [self.i, self.j - 1]]
        self.death_neigh = list(filter(lambda x: self.field[x[0]][x[1]] == "0", list(filter(lambda x: 0 <= x[0] < self.N, al[:2])) + list(filter(lambda x: 0 <= x[1] < self.M, al[2:]))))
        self.neigh = list(filter(lambda x: self.field[x[0]][x[1]] != "0", list(filter(lambda x: 0 <= x[0] < self.N, al[:2])) + list(filter(lambda x: 0 <= x[1] < self.M, al[2:]))))
    def __str__(self):
        return str(len(self.neigh))
class Death_Cell(Cell):
        def act(self):
            if len(self.neigh) == 3:
                return "*"
            else:
                return "0"
class Frank(Cell):
    def act(self):
        if len(self.death_neigh) == 0:
            return [["0", self.i, self.j]]
        else:
            m = [["Ф", self.i, self.j]]
            for h in self.death_neigh:
                if random.random() <= 0.2:
                    m.append([random.choice(["*", "М", "Ф"]), h[0], h[1]])

            return m


class Maniac(Cell):
    def act(self):
        if len(self.neigh) == 0:
            return [["0", self.i, self.j]]
        else:
            if random.random() <= 0.25:

                return [["0", x[0], x[1]] for x in self.neigh] + [["М", self.i, self.j]]

            else:
                return [["М", self.i, self.j]]

class Alive_Cell(Cell):
    def act(self):
        l = len(list(filter(lambda x: x != '0', self.neigh)))
        if l == 2 or l == 3:
            return "*"
        else:
            return "0"
class Field:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.N = len(a)
        self.M = len(a[0])
    def next(self):
        for i in range(self.N):
            for j in range(self.M):
                if self.a[i][j] == "0":
                    self.b[i][j] = Death_Cell(i, j, self.a).act()
                elif self.a[i][j] == "*":
                    self.b[i][j] = Alive_Cell(i, j, self.a).act()
                elif self.a[i][j] == "М":
                    for el in Maniac(i, j, self.a).act():
                        self.b[el[1]][el[2]] = el[0]
                else:
                    for el in Frank(i, j, self.a).act():
                        self.b[el[1]][el[2]] = el[0]
        self.a = self.b.copy()
    def show(self):
        for i in range(self.N):
            for j in range(self.M):
                text = f"{self.a[i][j]}"
                if self.a[i][j] == "*":
                    print("\033[32m{}".format(text), end = ' ') #\033[33m{} - выбор цвета текста
                elif self.a[i][j] == "М":
                    print("\033[31m{}".format(text), end=' ')  # \033[33m{} - выбор цвета текста
                elif self.a[i][j] == "Ф":
                    print("\033[34m{}".format(text), end=' ')  # \033[33m{} - выбор цвета текста
                else:
                    print("\033[30m{}".format(text), end=' ')  # \033[33m{} - выбор цвета текста
            print()
        print("\033[37m{}".format("="*(2* self.M)))
def simp_generate(N, M):
    a = [[0 for i in range(M)] for j in range(M)]
    for i in range(N):
        for j in range(M):
            if random.random() <= 0.1:
                a[i][j] = "М"
            elif 0.1 < random.random() <= 0.25:
                a[i][j] = "Ф"
            else:
                if random.random() < 0.5:
                    a[i][j] = "*"
                else:
                    a[i][j] = "0"
    return a




a1 = int(input("укажите длину стороны игрового поля: "))
a = simp_generate(a1, a1)
field = Field(a, a.copy())
while True:

    ch = input("следующий цикл: y/n ")
    if ch == "y":
        field.show()
        field.next()
    else:
        break
