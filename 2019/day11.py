from collections import defaultdict
import unittest

from intcode import runProgram


class Painter:
    def __init__(self, program):
        self.program = program

    def run(self, firstColor=0):
        def read():
            return self.panels[(self.x, self.y)]

        def write(n):
            if self.color is None:
                self.color = n
                self.paintLocation()
            else:
                self.direction = self.nextDirection(n)
                self.color = None
                self.goToNextLocation()

        self.reset(firstColor)
        runProgram(self.program, read, write)

    def reset(self, firstColor):
        self.panels = defaultdict(int)
        self.panels[(0, 0)] = firstColor

        self.x, self.y = 0, 0
        self.X, self.Y = (0, 0), (0, 0)
        self.color, self.direction = None, 'U'

    def paintLocation(self):
        self.panels[(self.x, self.y)] = self.color
        self.X = (min(self.x, min(self.X)), max(self.x, max(self.X)))
        self.Y = (min(self.y, min(self.Y)), max(self.y, max(self.Y)))

    def goToNextLocation(self):
        dxdy = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
        dx, dy = dxdy[self.direction]
        self.x += dx
        self.y += dy

    def nextDirection(self, turn):
        left = {'U': 'L', 'R': 'U', 'D': 'R', 'L': 'D'}
        right = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}
        return left[self.direction] if turn == 0 else right[self.direction]

    def render(self):
        rows = []
        for y in range(min(self.Y), max(self.Y) + 1):
            row = ''
            for x in range(min(self.X), max(self.X) + 1):
                row += '.' if self.panels[(x, y)] == 0 else '#'
            rows.append(row)
        return rows


class Day11(unittest.TestCase):
    def setUp(self):
        with open('input11') as fh:
            self.program = [int(n) for n in fh.readline().split(',')]

    def testPart1(self):
        painter = Painter(self.program)
        painter.run(0)
        self.assertEqual(len(painter.panels), 2041)

    def testPart2(self):
        painter = Painter(self.program)
        painter.run(1)
        reg = ['.####.###..####.###..#..#.####.####.###....',
               '....#.#..#....#.#..#.#.#..#.......#.#..#...',
               '...#..#..#...#..#..#.##...###....#..#..#...',
               '..#...###...#...###..#.#..#.....#...###....',
               '.#....#.#..#....#....#.#..#....#....#.#....',
               '.####.#..#.####.#....#..#.####.####.#..#...']
        self.assertEqual(painter.render(), reg)


if __name__ == '__main__':
    unittest.main()
