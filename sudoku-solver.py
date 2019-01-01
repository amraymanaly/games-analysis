#!/usr/bin/python3

# Example:

# matrix = [
#     [0, 6, 9, 4, 0, 0, 0, 7, 0],
#     [0, 7, 0, 8, 0, 0, 0, 0, 0],
#     [0, 3, 0, 0, 7, 6, 0, 0, 0],
#     [0, 1, 0, 0, 8, 0, 0, 4, 0],
#     [4, 6, 2, 7, 0, 0, 9, 0, 0],
#     [3, 0, 0, 0, 0, 9, 1, 0, 0],
#     [0, 0, 3, 0, 0, 4, 0, 5, 7],
#     [0, 0, 0, 0, 3, 8, 0, 0, 0],
#     [0, 0, 0, 7, 5, 0, 8, 6, 3]
# ]
#
# side_length = 3

# 0 6 9 0 7 0 0 3 0 is a row
# 0 4 0 0 0 0 0 0 0 is a col


class Group:
    def __init__(self, squares):

        self.squares = squares
        self.update_choices()
        # inform squares
        for square in self.squares:
            square.add_group(self)

        self.resolve_group()

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
        for p in self.stack:
            if len(self.stack[p]) == 1:
                self.stack[p][0].choose(p)


class Square:
    def __init__(self, i, j, side_length, val):
        self.i = i
        self.j = j
        self.value = val
        self.side_length = side_length
        self.choices = None if val != 0 else [i for i in range(1, side_length+1)]
        self.groups = []

    def choose(self, val):
        if self.value != 0: raise ValueError('Already has a value')
        if val not in self.choices: raise ValueError('Not a choice')
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
        if self.value != 0: return

        if len(self.choices) == 0:
            raise ValueError('Square cannot be in group')


class Grid:
    def __init__(self, n, matrix):
        # basic props
        self.side = n
        self.matrix = matrix
        self.squares = []
        # groups
        self.big_squares = []
        self.rows = []
        self.cols = []

        length = n * n
        # convert matrix to square objects matrix, and identify big square groups
        for i in range(length):
            self.squares.append([])
            for j in range(length):
                self.squares[i].append(Square(i, j, length, self.matrix[i][j]))

            self.big_squares.append(Group(self.squares[i]))

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
        for n in range(length):
            for square in self.squares[n]:
                square.inform_groups()

    def to_matrix(self):
        matrix = []
        for i in range(self.side * self.side):
            matrix.append([])
            for square in self.squares[i]:
                matrix[i].append(square.value)

        return matrix


def print_matrix(matrix, side_length):
    """prints a suduko matrix ordered in big square by big square fashion"""
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
        print('Enter the values of the squares in square groups, starting from the top left square group, move right, go down, then start from the left again.\n\
            Empty squares have the value 0')
        for i in range(s*s):
            m.append([])
            for j in range(s*s):
                m[i].append(int(input('Square %d of Group %d: ' % (j+1, i+1))))

        return s, m
    except (ValueError, KeyboardInterrupt, EOFError):
        print('Error!')
        exit(1)


if __name__ == '__main__':
    side_length, matrix = get_matrix()
    grid = Grid(side_length, matrix)
    declare(lambda: print('Before'), True)
    declare(lambda: print_matrix(matrix, side_length))
    declare(lambda: print('After'))
    declare(lambda: print_matrix(grid.to_matrix(), side_length))
