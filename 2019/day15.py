from collections import defaultdict, deque
import unittest

from intcode import runProgram


WALL, MOVE, OXYGEN = 0, 1, 2
NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
DIRS = {NORTH: (0, -1), WEST: (-1, 0), SOUTH: (0, 1), EAST: (1, 0)}


def scanBoard(program):
    d = NORTH
    x, y, ox, oy = 0, 0, None, None
    X, Y = (0, 0), (0, 0)
    board = defaultdict(lambda: None)
    board[(x, y)] = MOVE
    tried = defaultdict(set)

    def read():
        nonlocal d, x, y, X, Y
        if boardFilled(board, X, Y):
            return None
        x1, y1, d1 = None, None, None
        for e in (NORTH, SOUTH, EAST, WEST):
            if e not in tried[(x, y)]:
                if board[adj(x, y, e)] is None or None in (x1, y1, d1):
                    (x1, y1), d1 = adj(x, y, e), e
        tried[(x, y)].add(d1)
        x, y, d = x1, y1, d1
        X = (min(x, min(X)), max(x, max(X)))
        Y = (min(y, min(Y)), max(y, max(Y)))
        return d

    def write(n):
        nonlocal x, y, ox, oy
        board[(x, y)] = n
        if n == WALL:
            x, y = adj(x, y, d, reverse=True)
        elif n == OXYGEN:
            ox, oy = x, y

    runProgram(program, read, write)
    return board, (ox, oy)


def boardFilled(board, X, Y):
    for y in range(min(Y), max(Y) + 1):
        for x in range(min(X), max(X) + 1):
            if board[(x, y)] == MOVE:
                for d in DIRS:
                    if board[adj(x, y, d)] is None:
                        return False
    return True


def adj(x, y, d, reverse=False):
    dx, dy = DIRS[d]
    return (x - dx, y - dy) if reverse else (x + dx, y + dy)


def findOxygen(program):
    board, _ = scanBoard(program)
    visited = set()
    Q = deque([(0, 0, 0)])
    while len(Q) > 0:
        x, y, dist = Q.popleft()
        if board[(x, y)] == OXYGEN:
            return dist
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in DIRS.values():
                x1, y1 = x + dx, y + dy
                if board[(x1, y1)] not in (None, WALL):
                    Q.append((x1, y1, dist + 1))


def fillOxygen(program):
    board, (x, y) = scanBoard(program)
    minutes = None
    Q = deque([(x, y, 0)])
    while len(Q) > 0:
        x, y, minutes = Q.popleft()
        for dx, dy in DIRS.values():
            x1, y1 = x + dx, y + dy
            if board[(x1, y1)] == MOVE:
                board[(x1, y1)] = OXYGEN
                Q.append((x1, y1, minutes + 1))
    return minutes


class Day15(unittest.TestCase):
    def setUp(self):
        with open('input15') as fh:
            self.program = [int(n) for n in fh.readline().split(',')]

    def testPart1(self):
        self.assertEqual(findOxygen(self.program), 404)

    def testPart2(self):
        self.assertEqual(fillOxygen(self.program), 406)


if __name__ == '__main__':
    unittest.main()
