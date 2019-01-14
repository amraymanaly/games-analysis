#!/usr/bin/python3

#TODO: implement the Naked Pair strategy

import copy

# Example:

# # simple
matrix = [
    [0, 6, 9, 4, 0, 0, 0, 7, 0],
    [0, 7, 0, 8, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 7, 6, 0, 0, 0],
    [0, 1, 0, 0, 8, 0, 0, 4, 0],
    [4, 6, 2, 7, 0, 0, 9, 0, 0],
    [3, 0, 0, 0, 0, 9, 1, 0, 0],
    [0, 0, 3, 0, 0, 4, 0, 5, 7],
    [0, 0, 0, 0, 3, 8, 0, 0, 0],
    [0, 0, 0, 7, 5, 0, 8, 6, 3]
]

side_length = 3

# 0 6 9 0 7 0 0 3 0 is a row
# 0 4 0 0 0 0 0 0 0 is a col

# # complex
matrix = [
  [0, 5, 0, 3, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 8, 2, 5, 0],
  [0, 0, 8, 9, 0, 0, 0, 1, 0],
  [0, 1, 0, 0, 0, 5, 8, 0, 3],
  [0, 0, 0, 6, 0, 9, 0, 0, 0],
  [6, 0, 3, 4, 0, 0, 0, 2, 0],
  [0, 3, 0, 0, 0, 6, 7, 0, 0],
  [0, 1, 2, 5, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 4, 0, 9, 0]
]
side_length = 3

# debug
# matrix = [
#     [0, 7, 9, 0, 0, 1, 6, 2, 4],
#     [0, 0, 0, 0, 6, 7, 9, 0, 0],
#     [6, 0, 1, 0, 0, 0, 3, 7, 0],
#     [0, 0, 6, 0, 0, 0, 9, 3, 0],
#     [0, 0, 4, 1, 0, 5, 0, 0, 0],
#     [0, 0, 0, 0, 6, 0, 0, 0, 0],
#     [0, 6, 5, 7, 9, 8, 0, 0, 3],
#     [0, 0, 0, 0, 0, 3, 5, 8, 9],
#     [8, 9, 3, 5, 0, 0, 0, 0, 0]
# ]
#
# side_length = 3


class Group:
    def __init__(self, squares):

        self.squares = squares

        # Check for validity
        tmp = [sq.value for sq in self.squares if sq.value != 0]
        values = self.values()
        if 0 in values:
            tmp.append(0)
        if len(tmp) != len(values):
            raise ValueError('Invalid group')

        self.update_choices()
        self._done()
        # inform squares
        for square in self.squares:
            square.add_group(self)

    def _done(self):
        self.done = len([x for p in self.stack for x in self.stack[p]]) == 0

    def update_choices(self):
        self.stack = {}

        # populate stack
        values = self.values()
        for square in self.squares:
            if square.value == 0:
                to_remove = []
                for choice in square.choices:
                    if choice not in self.stack:
                        self.stack[choice] = []
                    if choice in values:
                        to_remove.append(choice)
                    else:
                        self.stack[choice].append(square)
                for p in to_remove:
                    square.choices.remove(p)
            elif square.value not in self.stack:
                self.stack[square.value] = []

    def values(self):
        return set([sq.value for sq in self.squares])

    def resolve_group(self):
        # This is where the strategies are applied! #

        if self.done:
            return

        # Hidden Single Pattern
        for p in self.stack:
            try:
                if len(self.stack[p]) == 1:
                    self.stack[p][0].choose(p)
            except KeyError:
                # Mathematically impossible! This is because squares step on each other's toes for choices
                raise ValueError('Cannot be solved')

        self._done()


class Square:
    def __init__(self, i, j, grid, val):
        self.value = val
        self.grid = grid
        # DEBUG ONLY #
        self.i = i
        self.j = j
        # DEBUG ONLY #
        self.choices = None if val != 0 else [i for i in range(1, (grid.side * grid.side)+1)]
        self.groups = []

    def choose(self, val):
        # DEBUG ONLY #
        if self.value != 0:
            raise ValueError('Already has a value')
        if val not in self.choices:
            raise ValueError('Not a choice')
        # DEBUG ONLY #

        self.choices = None
        self.value = val
        # inform associated groups
        self.inform_groups()

    def inform_groups(self):
        for group in self.groups:
            group.update_choices()

        for group in self.groups:
            group.resolve_group()

    def add_group(self, group):
        self.groups.append(group)
        if self.value != 0:
            return

        if len(self.choices) == 0:
            # Square cannot be in group
            raise ValueError()
        # elif len(self.choices) == 1 and self not in self.grid.naked:
        #     self.grid.naked.append(self)


class Grid:
    def __init__(self, n, matrix):
        # basic props
        self.side = n
        self.matrix = matrix
        self.squares = []
        # self.naked = []
        # groups
        self.regions = []
        self.rows = []
        self.cols = []

        length = n * n
        # convert matrix to square objects matrix, and identify big square groups
        for i in range(length):
            self.squares.append([])
            for j in range(length):
                self.squares[i].append(Square(i, j, self, self.matrix[i][j]))

            self.regions.append(Group(self.squares[i]))

        # identify row and column groups
        for n in range(length):
            row, col, big_square = [], [], []
            c = ((n//self.side) * self.side)

            for i in range(self.side):
                for j in range(self.side):
                    row.append(self.squares[i + (n % self.side) * self.side][j + c])
                    col.append(self.squares[i * self.side + n//self.side][j * self.side + n % self.side])

            self.rows.append(Group(row))
            self.cols.append(Group(col))

        # now that the groups are ready..

        # Group Strategies
        for g in [self.regions, self.rows, self.cols]:
            for group in g:
                group.update_choices()
                group.resolve_group()

        # Naked Single Pattern
        # for square in self.naked:
        #     if square.choices:
        #         square.choose(square.choices[0])

    def to_matrix(self):
        matrix = []
        for i in range(self.side * self.side):
            matrix.append([])
            for square in self.squares[i]:
                matrix[i].append(square.value)

        return matrix

    def hypothesize(self):
        # This is where it gets more fantasy than science ;)
        # So here's the strategy, pick a square with the least number of choices, and guess... yeh...
        # We create sandboxes first

        def find_easy_square(grid):
            # find square most likely to yield good results
            for n in range(2, grid.side * grid.side + 1):
                for g in grid.regions:
                    if g.done:
                        continue
                    for square in g.squares:
                        if square.value == 0 and len(square.choices) == n:
                            if (square.i, square.j) not in try_once.tried:
                                return square.i, square.j, n

        def try_once(states):
            branch = list(states.keys())[-1]
            n = 0
            c = -1

            if try_once.error:
                if try_once.last_try[2] < n - 2:
                    try_once.error = False
                    c = try_once.last_try[2]
                else:
                    try_once.tried.append((try_once.last_try[0], try_once.last_try[1]))
                    i, j, n = find_easy_square(branch)

            if n == 0:
                i, j, n = find_easy_square(branch)

            while c < n - 1:
                c += 1
                virtual = copy.deepcopy(branch)
                dice = virtual.squares[i][j]

                try_once.last_try = (i, j, c)
                try:
                    dice.choose(dice.choices[c])
                except ValueError:
                    continue
                states[virtual] = try_once.last_try
                return states

            # state is corrupted
            if len(states) == 1:
                raise ValueError('Cannot hypothesize')
            try_once.error = True
            return try_once(states)

        sandbox = self
        states = {self: None}
        try_once.tried = []
        while not list(states.keys())[-1].is_solved():
            try_once.error = False
            states = try_once(states)
            declare(lambda: print('Virtual'))
            declare(lambda: print_matrix(list(states.keys())[-1].to_matrix(), sandbox.side))

        return sandbox

    def is_solved(self):
        return len([0 for g in self.regions if g.done]) == len(self.regions)


def print_matrix(matrix, side_length):
    """prints a sudoku matrix ordered in big square by big square fashion"""
    rows = []
    for i in range(side_length * side_length):
        rows.append([])
    for i in range(side_length * side_length):
        for j in range(side_length * side_length):
            rows[j // side_length + (i // side_length) * side_length].append(matrix[i][j])
    for row in rows:
        print(', '.join([str(val) for val in row]))


def declare(func, start=False):
    if start:
        print('#' * (side_length * side_length * 3 - 2))
    func()
    print('#' * (side_length * side_length * 3 - 2))


def get_matrix():
    try:
        s = int(input('Side Length? '))
        m = []
        print('Enter the values of the squares in square groups, starting from the top left square group,\
move right, go down, then start from the left again.\nEmpty squares have the value 0')
        for i in range(s*s):
            m.append([])
            for j in range(s*s):
                m[i].append(int(input('Square %d of Group %d: ' % (j+1, i+1))))

        return s, m
    except (ValueError, KeyboardInterrupt, EOFError):
        print('Error!')
        exit(1)


if __name__ == '__main__':
    # side_length, matrix = get_matrix()
    grid = None
    try:
        grid = Grid(side_length, matrix)
    except ValueError as e:
        print('Invalid Sudoku Matrix%s!' % ((': ' + e.args[0]) if len(e.args) == 1 else ''))
        exit(1)
    declare(lambda: print('Before'), True)
    declare(lambda: print_matrix(matrix, side_length))
    declare(lambda: print('Before Hypothesis'))
    declare(lambda: print_matrix(grid.to_matrix(), side_length))
    # grid = grid.hypothesize()
    declare(lambda: print('After'))
    declare(lambda: print_matrix(grid.to_matrix(), side_length))
    print('Done!')
