import unittest
from collections import defaultdict

from intcode import runProgram


class Game:
    EMPTY, WALL, BLOCK, PADDLE, BALL = 0, 1, 2, 3, 4

    def __init__(self, display=False):
        self.board = defaultdict(int)
        self.score = 0
        self.x, self.y, self.t = None, None, None
        self.ball, self.paddle = None, None
        self.display = display

    def read(self):
        if self.display:
            self.printBoard()
        if self.ball is None or self.paddle is None or self.ball == self.paddle:
            return 0
        return -1 if self.ball < self.paddle else 1

    def write(self, n):
        if self.x is None:
            self.x = n
        elif self.y is None:
            self.y = n
        elif self.t is None:
            self.t = n
            self.paint()

    def paint(self):
        if self.x == -1 and self.y == 0:
            self.score = self.t
        else:
            self.board[(self.x, self.y)] = self.t
            if self.t == Game.PADDLE:
                self.paddle = self.x
            elif self.t == Game.BALL:
                self.ball = self.x
        self.x, self.y, self.t = None, None, None

    def printBoard(self):
        value = {Game.EMPTY: ' ', Game.WALL: '|', Game.BLOCK: '#', Game.PADDLE: '_', Game.BALL: 'o'}
        width = max(x for (x, _) in self.board) + 1
        height = max(y for (_, y) in self.board) + 1
        for y in range(height):
            row = ''
            for x in range(width):
                row += value[self.board[(x, y)]]
            print(row)

    def countBlocks(self):
        return sum(1 if v == Game.BLOCK else 0 for v in self.board.values())


def playGame(program):
    game = Game()

    def read():
        return game.read()

    def write(n):
        game.write(n)

    runProgram(program, read, write)
    return game


class Day13(unittest.TestCase):
    def setUp(self):
        with open('input13') as fh:
            self.program = [int(n) for n in fh.readline().split(',')]

    def testPart1(self):
        self.assertEqual(playGame(self.program).countBlocks(), 363)

    def testPart2(self):
        self.program[0] = 2
        self.assertEqual(playGame(self.program).score, 17159)


if __name__ == '__main__':
    unittest.main()
