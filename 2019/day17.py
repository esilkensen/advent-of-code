import unittest

from intcode import runProgram, runProgramIO


def scan(program):
    scaffold = ''

    def read():
        pass

    def write(n):
        nonlocal scaffold
        scaffold += chr(n)

    runProgram(program, read, write)
    return scaffold.split()


def scaffoldIntersections(scaffold, debug=False):
    intersections = set()
    for y in range(1, len(scaffold) - 1):
        for x in range(1, len(scaffold[y]) - 1):
            if scaffold[y][x] == '#' and \
               scaffold[y+1][x] == '#' and scaffold[y-1][x] == '#' and \
               scaffold[y][x+1] == '#' and scaffold[y][x-1] == '#':
                intersections.add((x, y))
    if debug:
        for y in range(len(scaffold)):
            line = ''
            for x in range(len(scaffold[y])):
                line += 'O' if (x, y) in intersections else scaffold[y][x]
            print(line)

    return intersections


def alignmentParameters(intersections):
    return (x * y for (x, y) in intersections)


def calibrate(scaffold, debug=False):
    intersections = scaffoldIntersections(scaffold, debug)
    return sum(alignmentParameters(intersections))


def findRobot(scaffold):
    for y in range(len(scaffold)):
        for x in range(len(scaffold[y])):
            if scaffold[y][x] in '<^>v':
                return (x, y)


def inbounds(scaffold, x, y):
    return 0 <= y < len(scaffold) and 0 <= x < len(scaffold[y])


left = {'^': '<', '>': '^', 'v': '>', '<': 'v'}
right = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
moves = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}


def firstDirection(scaffold, x, y):
    d = scaffold[y][x]
    for m in moves:
        dx, dy = moves[m]
        x2, y2 = x + dx, y + dy
        if inbounds(scaffold, x2, y2):
            if scaffold[y2][x2] == '#':
                t = None
                if left[d] == m:
                    t = 'L'
                elif right[d] == m:
                    t = 'R'
                return m, t


def nextDirection(scaffold, x, y, d):
    dlx, dly = moves[left[d]]
    drx, dry = moves[right[d]]
    lx, ly = x + dlx, y + dly
    rx, ry = x + drx, y + dry
    if inbounds(scaffold, lx, ly) and scaffold[ly][lx] == '#':
        return left[d], 'L'
    elif inbounds(scaffold, rx, ry) and scaffold[ry][rx] == '#':
        return right[d], 'R'
    return None, None


def nextPath(scaffold, x, y, d=None):
    t = None
    if d is None:
        d, t = firstDirection(scaffold, x, y)
    else:
        d, t = nextDirection(scaffold, x, y, d)
    if d is None and t is None:
        return '', x, y, d

    path = [] if t is None else [t]

    dx, dy = moves[d]
    count = 1
    x2, y2 = x + dx, y + dy
    while inbounds(scaffold, x2, y2) and scaffold[y2][x2] == '#':
        x2, y2 = x2 + dx, y2 + dy
        count += 1
    x2, y2 = x2 - dx, y2 - dy
    count -= 1

    path.append(str(count))
    return ','.join(path), x2, y2, d


def findPath(scaffold):
    paths = []

    (x, y), d = findRobot(scaffold), None
    path, x2, y2, d2 = nextPath(scaffold, x, y, d)
    while len(path) > 0:
        paths.append(path)
        path, x2, y2, d2 = nextPath(scaffold, x2, y2, d2)

    return ','.join(paths)


def run(program, main, A, B, C, feed):
    program = [n for n in program]
    program[0] = 2
    inputValues = [ord(c) for c in list('\n'.join(['\n' + feed, C[::-1], B[::-1], A[::-1], main[::-1]]))]
    return runProgramIO(program, inputValues)[-1]


class Day17(unittest.TestCase):
    def setUp(self):
        with open('input17') as fh:
            self.program = [int(n) for n in fh.readline().split(',')]

    def testCalibrate(self):
        scaffold = ['..#..........',
                    '..#..........',
                    '#######...###',
                    '#.#...#...#.#',
                    '#############',
                    '..#...#...#..',
                    '..#####...^..']
        self.assertEqual(calibrate(scaffold), 76)

    def testPart1(self):
        self.assertEqual(calibrate(scan(self.program), False), 9876)

    def testFindPath(self):
        scaffold = ['..#..........',
                    '..#..........',
                    '#######...###',
                    '#.#...#...#.#',
                    '#############',
                    '..#...#...#..',
                    '..#####...^..']
        self.assertEqual(findPath(scaffold), '4,R,2,R,2,R,12,R,2,R,6,R,4,R,4,R,6')

    def testFindPath2(self):
        scaffold = ['#######...#####',
                    '#.....#...#...#',
                    '#.....#...#...#',
                    '......#...#...#',
                    '......#...###.#',
                    '......#.....#.#',
                    '^########...#.#',
                    '......#.#...#.#',
                    '......#########',
                    '........#...#..',
                    '....#########..',
                    '....#...#......',
                    '....#...#......',
                    '....#...#......',
                    '....#####......']
        self.assertEqual(findPath(scaffold), 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2')

    def testPart2(self):
        main = 'A,B,A,C,B,C,B,A,C,B'
        A, B, C = 'L,10,L,6,R,10', 'R,6,R,8,R,8,L,6,R,8', 'L,10,R,8,R,8,L,10'
        self.assertEqual(findPath(scan(self.program)), ','.join([A, B, A, C, B, C, B, A, C, B]))
        self.assertEqual(run(self.program, main, A, B, C, 'n'), 1234055)


if __name__ == '__main__':
    unittest.main()
