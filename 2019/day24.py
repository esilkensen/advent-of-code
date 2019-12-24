import unittest


def firstRepeatingState(tiles):
    def key(tiles):
        return ''.join(tiles)

    keys = set()
    k = key(tiles)
    while k not in keys:
        keys.add(k)
        tiles = nextState(tiles)
        k = key(tiles)
    return tiles


def nextState(tiles):
    nextTiles = []
    for row in range(len(tiles)):
        nextRow = ''
        for col in range(len(tiles[row])):
            bugs = adjacentBugs(tiles, row, col)
            if tiles[row][col] == '#':
                nextRow += '#' if bugs == 1 else '.'
            else:
                nextRow += '#' if bugs == 1 or bugs == 2 else '.'
        nextTiles.append(nextRow)
    return nextTiles


def adjacentBugs(tiles, row, col):
    count = 0
    for dr, dc in (0, 1), (0, -1), (1, 0), (-1, 0):
        row2, col2 = row + dr, col + dc
        if 0 <= row2 < len(tiles) and 0 <= col2 < len(tiles[row2]):
            if tiles[row2][col2] == '#':
                count += 1
    return count


def biodiversityRating(tiles):
    rating = 0
    for row in range(len(tiles)):
        for col in range(len(tiles[row])):
            n = row * len(tiles[row]) + col
            if tiles[row][col] == '#':
                rating += 2 ** n
    return rating


def nextRecursiveStates(levels):
    nextLevels = []
    levels = [emptyTiles()] + levels + [emptyTiles()]
    for depth in range(len(levels)):
        tiles = levels[depth]
        nextTiles = []
        for row in range(len(tiles)):
            nextRow = ''
            for col in range(len(tiles[row])):
                if row == 2 and col == 2:
                    nextRow += '.'
                else:
                    bugs = recursiveAdjacentBugs(row, col, depth, levels)
                    if tiles[row][col] == '#':
                        nextRow += '#' if bugs == 1 else '.'
                    else:
                        nextRow += '#' if bugs == 1 or bugs == 2 else '.'
            nextTiles.append(nextRow)
        nextLevels.append(nextTiles)
    return nextLevels


def recursiveAdjacentBugs(row, col, depth, levels):
    count = 0
    tiles = levels[depth]
    mid = len(tiles) // 2

    if row == mid and col == mid:
        return 0

    for dr, dc in (0, 1), (0, -1), (1, 0), (-1, 0):
        row2, col2 = row + dr, col + dc
        if 0 <= row2 < len(tiles) and 0 <= col2 < len(tiles[row2]):
            if row2 == mid and col2 == mid and depth < len(levels) - 1:
                count += nextAdjacentBugs(levels[depth + 1], dr, dc)
            elif tiles[row2][col2] == '#':
                count += 1
        elif depth > 0:
            prevTiles = levels[depth - 1]
            if prevTiles[mid + dr][mid + dc] == '#':
                count += 1

    return count


def nextAdjacentBugs(tiles, dr, dc):
    count = 0
    if dr == 0:
        for r in range(len(tiles)):
            if tiles[r][0 if dc == 1 else -1] == '#':
                count += 1
    else:
        for c in range(len(tiles[0])):
            if tiles[0 if dr == 1 else -1][c] == '#':
                count += 1
    return count


def emptyTiles(rows=5, cols=5):
    row = '.' * cols
    return [row for _ in range(rows)]


def loopFor(levels, n):
    for i in range(n):
        levels = nextRecursiveStates(levels)
    return levels


def bugsPresentAfter(levels, n):
    levels = loopFor(levels, n)
    bugs = 0
    for level in levels:
        bugs += sum(row.count('#') for row in level)
    return bugs


class Day24(unittest.TestCase):
    def setUp(self):
        with open('input24') as fh:
            self.tiles = [line.strip() for line in fh]

    def testFirstRepeatingState(self):
        tiles = ['....#',
                 '#..#.',
                 '#..##',
                 '..#..',
                 '#....']
        firstTiles = ['.....',
                      '.....',
                      '.....',
                      '#....',
                      '.#...']
        self.assertEqual(firstRepeatingState(tiles), firstTiles)

    def testNextState(self):
        tiles = ['....#',
                 '#..#.',
                 '#..##',
                 '..#..',
                 '#....']
        nextTiles = ['#..#.',
                     '####.',
                     '###.#',
                     '##.##',
                     '.##..']
        self.assertEqual(nextState(tiles), nextTiles)

    def testBiodiversityRating(self):
        tiles = ['.....',
                 '.....',
                 '.....',
                 '#....',
                 '.#...']
        self.assertEqual(biodiversityRating(tiles), 2129920)

    def testBugsPresentAfter(self):
        levels = [['....#',
                   '#..#.',
                   '#..##',
                   '..#..',
                   '#....']]
        self.assertEqual(bugsPresentAfter(levels, 10), 99)

    def testPart1(self):
        tiles = firstRepeatingState(self.tiles)
        self.assertEqual(biodiversityRating(tiles), 32509983)

    def testPart2(self):
        self.assertEqual(bugsPresentAfter([self.tiles], 200), 2012)


if __name__ == '__main__':
    unittest.main()
