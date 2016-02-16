class Puzzle:

    up = -3
    down = 3
    left = -1
    right = 1

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
        return format_str.format(*self.__tuple)

    def __eq__(self, other):
        return self.__list == other.__list

    def __swap(self, i, j):
        self.__list[i], self.__list[j] = self.__list[j], self.__list[i]

    @property
    def __tuple(self):
        temp_list = [0] * 9
        for i, num in enumerate(self.__list):
            temp_list[i] = num if num != 0 else ' '
        return tuple(temp_list)

    def position(self, num):
        if not 0 <= num < 9:
            raise Exception("cannot check position for {}".format(num))
        index = self.__list.index(num)
        return index // 3, index % 3

    def can_move(self, orientation):
        pass

    @property
    def step(self):
        return len(self.history)

    @property
    def can_move_up(self):
        return self.position(0)[0] > 0

    @property
    def can_move_down(self):
        return self.position(0)[0] < 2

    @property
    def can_move_left(self):
        return self.position(0)[1] > 0

    @property
    def can_move_right(self):
        return self.position(0)[1] < 2

    def move_up(self):
        if self.can_move_up:
            pos = self.__list.index(0)
            new_pos = pos + Puzzle.up
            self.__swap(pos, new_pos)
            self.history.append(Puzzle.up)

    def move_down(self):
        if self.can_move_down:
            pos = self.__list.index(0)
            new_pos = pos + Puzzle.down
            self.__swap(pos, new_pos)
            self.history.append(Puzzle.down)

    def move_left(self):
        if self.can_move_left:
            pos = self.__list.index(0)
            new_pos = pos + Puzzle.left
            self.__swap(pos, new_pos)
            self.history.append(Puzzle.left)

    def move_right(self):
        if self.can_move_right:
            pos = self.__list.index(0)
            new_pos = pos + Puzzle.right
            self.__swap(pos, new_pos)
            self.history.append(Puzzle.right)

    def go_back(self):
        if len(self.history) != 0:
            pos = self.__list.index(0)
            new_pos = pos - self.history.pop(-1)
            self.__swap(pos, new_pos)

    def heuristic(self, goal):
        dist = 0
        for i in range(1, 9):
            dist += abs(self.position(i)[0] - goal.position(i)[0])
            dist += abs(self.position(i)[1] - goal.position(i)[1])
        return dist


p = Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)
p.move_down()
p.move_right()
p.go_back()
print(p, p.heuristic(Puzzle(0, 1, 2, 3, 4, 5, 6, 7, 8)))
print(p.history)

