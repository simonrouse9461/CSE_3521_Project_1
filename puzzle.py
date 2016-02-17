class Puzzle:

    Up = -1, 0
    Down = 1, 0
    Left = 0, -1
    Right = 0, 1
    Actions = (Up, Down, Left, Right)

    @staticmethod
    def raw(move):
        return move[0]*3 + move[1]

    def __init__(self, *args):
        if len(args) != 9:
            raise Exception('9 arguments expected')
        if len(set(args)) != 9:
            raise Exception('arguments must be unique')
        self.__list = [0] * 9
        for i, num in enumerate(args):
            if 0 <= num < 9:
                self.__list[i] = num
            else:
                del self.__list
                raise Exception('argument out of range')
        self.history = []

    def __str__(self):
        format_str = '\n+---+---+---+\n| {} | {} | {} |' * 3 + '\n+---+---+---+\n'
        return format_str.format(*self.tuple)

    def __eq__(self, other):
        return self.__list == other.__list

    def __swap(self, i, j):
        self.__list[i], self.__list[j] = self.__list[j], self.__list[i]

    @property
    def tuple(self):
        temp_list = [0] * 9
        for i, num in enumerate(self.__list):
            temp_list[i] = num if num != 0 else ' '
        return tuple(temp_list)

    @property
    def copy(self):
        copy = Puzzle(*self.__list)
        copy.history = self.history
        return copy

    @property
    def step(self):
        return len(self.history)

    def position(self, num):
        if not 0 <= num < 9:
            raise Exception("cannot check position for {}".format(num))
        index = self.__list.index(num)
        return index // 3, index % 3

    def can_move(self, orientation):
        return self.position(0)[0] + orientation[0] in range(0, 3) and \
            self.position(0)[1] + orientation[1] in range(0, 3)

    def move(self, *movements):
        for move in movements:
            if self.can_move(move):
                pos = self.__list.index(0)
                new_pos = pos + Puzzle.raw(move)
                self.__swap(pos, new_pos)
                self.history.append(move)

    def undo(self, steps):
        if steps == 0:
            return
        pos = self.__list.index(0)
        old_pos = pos - Puzzle.raw(self.history.pop(-1))
        self.__swap(pos, old_pos)
        self.undo(steps - 1)

    def heuristic(self, goal):
        dist = 0
        for i in range(1, 9):
            dist += abs(self.position(i)[0] - goal.position(i)[0])
            dist += abs(self.position(i)[1] - goal.position(i)[1])
        return dist


p = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
p.move(Puzzle.Down, Puzzle.Right, Puzzle.Down, Puzzle.Right, Puzzle.Up,
       Puzzle.Down, Puzzle.Right, Puzzle.Down, Puzzle.Right, Puzzle.Up)
print(p)
print("heuristic: ", p.heuristic(Puzzle(8, 7, 6, 5, 4, 3, 2, 1, 0)))
print("history: ", p.history)
q = p.copy
q.undo(5)
print(q)
