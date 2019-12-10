from collections import defaultdict
import unittest


def detect(grid):
    asteroids = set(asteroidLocations(grid))
    views = [[set() for _ in row] for row in grid]
    hits = [[defaultdict(set) for _ in row] for row in grid]

    for y1 in range(len(grid)):
        for x1 in range(len(grid[y1])):
            for (x2, y2) in asteroids:
                if x1 != x2 or y1 != y2:
                    m = (y2 - y1) / (x2 - x1) if x2 != x1 else '+inf' if y2 > y1 else '-inf'
                    b = y1 - m * x1 if isinstance(m, int) else ('+%s' % y1) if x2 > x1 else ('-%s' % y1) # TODO: WTF
                    views[y1][x1].add((m, b))
                    hits[y1][x1][(m, b)].add((x2, y2))

    detections = [[0 for _ in row] for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            detections[y][x] = len(views[y][x])
    return detections, views, hits


def bestLocation(grid):
    asteroids = set(asteroidLocations(grid))
    detections = detect(grid)[0]
    best, maxDetections = None, 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in asteroids and maxDetections < detections[y][x]:
                best, maxDetections = (x, y), detections[y][x]
    return best, maxDetections


def vaporize(grid, startingLocation=None):
    x1, y1 = bestLocation(grid)[0] if startingLocation is None else startingLocation
    detections, views, hits = detect(grid)
    asteroids = set(asteroidLocations(grid))

    dist = [[0 for _ in row] for row in grid]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            dist[y][x] = abs(x - x1) + abs(y - y1)

    while len(hits[y1][x1]) > 0:
        #print('=== hits: %d ===' % len(hits[y1][x1]))
        # 1. m == '-inf', find closest y
        #print('=== 1 ===')
        mm, bb, x, y = None, None, None, None
        for m, b in hits[y1][x1]:
            if m == '-inf':
                for x2, y2 in hits[y1][x1][(m, b)]:
                    if (x2, y2) in asteroids and ((x, y) == (None, None) or abs(y - y1) > abs(y2 - y1)):
                        mm, bb, x, y = m, b, x2, y2
        if (x, y) != (None, None):
            asteroids.remove((x, y))
            hits[y1][x1][(mm, bb)].remove((x, y))
            if len(hits[y1][x1][(mm, bb)]) == 0:
                del hits[y1][x1][(mm, bb)]
            yield (x, y)

        # 2. m < 0
        #print('=== 2 ===')
        scan2 = True
        lm, lb = None, None
        while scan2:
            mm, bb, x, y = None, None, None, None
            for m, b in hits[y1][x1]:
                if not isinstance(m, str) and m < 0 and (mm == None or m < mm) and (lm == None or m > lm):
                    for x2, y2 in hits[y1][x1][(m, b)]:
                        if (x2, y2) in asteroids and x2 > x1 and y2 < y1:
                            if mm == None or (x, y) == (None, None) or m < mm or (m == mm and dist[y2][x2] < dist[y][x]):
                                mm, bb, x, y = m, b, x2, y2
            if (x, y) != (None, None):
                asteroids.remove((x, y))
                hits[y1][x1][(mm, bb)].remove((x, y))
                if len(hits[y1][x1][(mm, bb)]) == 0:
                    del hits[y1][x1][(mm, bb)]
                lm, lb = mm, bb
                yield (x, y)
            else:
                scan2 = False

        # 3. str(m) == '0.0', closest x
        #print('=== 3 ===')
        mm, bb, x, y = None, None, None, None
        for m, b in hits[y1][x1]:
            if str(m) == '0.0':
                for x2, y2 in hits[y1][x1][(m, b)]:
                    if (x2, y2) in asteroids and ((x, y) == (None, None) or abs(x - x1) > abs(x2 - x1)):
                        mm, bb, x, y = m, b, x2, y2
        if (x, y) != (None, None):
            asteroids.remove((x, y))
            hits[y1][x1][(mm, bb)].remove((x, y))
            if len(hits[y1][x1][(mm, bb)]) == 0:
                del hits[y1][x1][(mm, bb)]
            yield (x, y)

        # 4. m > 0
        #print('=== 4 ===')
        scan4 = True
        lm, lb = None, None
        while scan4:
            mm, bb, x, y = None, None, None, None
            for m, b in hits[y1][x1]:
                if not isinstance(m, str) and m > 0 and (mm == None or m < mm) and (lm == None or m > lm):
                    for x2, y2 in hits[y1][x1][(m, b)]:
                        if (x2, y2) in asteroids and x2 > x1 and y2 > y1:
                            if mm == None or (x, y) == (None, None) or m < mm or (m == mm and dist[y2][x2] < dist[y][x]):
                                mm, bb, x, y = m, b, x2, y2
            if (x, y) != (None, None):
                asteroids.remove((x, y))
                hits[y1][x1][(mm, bb)].remove((x, y))
                if len(hits[y1][x1][(mm, bb)]) == 0:
                    del hits[y1][x1][(mm, bb)]
                lm, lb = mm, bb
                yield (x, y)
            else:
                scan4 = False

        # 5. m == '+inf', closest y
        #print('=== 5 ===')
        mm, bb, x, y = None, None, None, None
        for m, b in hits[y1][x1]:
            if m == '+inf':
                for x2, y2 in hits[y1][x1][(m, b)]:
                    if (x2, y2) in asteroids and ((x, y) == (None, None) or abs(y - y1) > abs(y2 - y1)):
                        mm, bb, x, y = m, b, x2, y2
        if (x, y) != (None, None):
            asteroids.remove((x, y))
            hits[y1][x1][(mm, bb)].remove((x, y))
            if len(hits[y1][x1][(mm, bb)]) == 0:
                del hits[y1][x1][(mm, bb)]
            yield (x, y)

        # 6. m < 0
        #print('=== 6 ===')
        scan6 = True
        lm, lb = None, None
        while scan6:
            mm, bb, x, y = None, None, None, None
            for m, b in hits[y1][x1]:
                if not isinstance(m, str) and m < 0 and (mm == None or m < mm) and (lm == None or m > lm):
                    for x2, y2 in hits[y1][x1][(m, b)]:
                        if (x2, y2) in asteroids and x2 < x1 and y2 > y1:
                            if mm == None or (x, y) == (None, None) or m < mm or (m == mm and dist[y2][x2] < dist[y][x]):
                                mm, bb, x, y = m, b, x2, y2
            if (x, y) != (None, None):
                asteroids.remove((x, y))
                hits[y1][x1][(mm, bb)].remove((x, y))
                if len(hits[y1][x1][(mm, bb)]) == 0:
                    del hits[y1][x1][(mm, bb)]
                lm, lb = mm, bb
                yield (x, y)
            else:
                scan6 = False

        # 7. str(m) == '-0.0', closest x
        #print('=== 7 ===')
        mm, bb, x, y = None, None, None, None
        for m, b in hits[y1][x1]:
            if str(m) == '-0.0':
                for x2, y2 in hits[y1][x1][(m, b)]:
                    if (x2, y2) in asteroids and ((x, y) == (None, None) or abs(x - x1) > abs(x2 - x1)):
                        mm, bb, x, y = m, b, x2, y2
        if (x, y) != (None, None):
            asteroids.remove((x, y))
            hits[y1][x1][(mm, bb)].remove((x, y))
            if len(hits[y1][x1][(mm, bb)]) == 0:
                del hits[y1][x1][(mm, bb)]
            yield (x, y)

        # 8. m > 0
        #print('=== 8 ===')
        scan8 = True
        lm, lb = None, None
        while scan8:
            mm, bb, x, y = None, None, None, None
            for m, b in hits[y1][x1]:
                if not isinstance(m, str) and m > 0 and (mm == None or m < mm) and (lm == None or m > lm):
                    for x2, y2 in hits[y1][x1][(m, b)]:
                        if (x2, y2) in asteroids and x2 < x1 and y2 < y1:
                            if mm == None or (x, y) == (None, None) or m < mm or (m == mm and dist[y2][x2] < dist[y][x]):
                                mm, bb, x, y = m, b, x2, y2
            if (x, y) != (None, None):
                asteroids.remove((x, y))
                hits[y1][x1][(mm, bb)].remove((x, y))
                if len(hits[y1][x1][(mm, bb)]) == 0:
                    del hits[y1][x1][(mm, bb)]
                lm, lb = mm, bb
                yield (x, y)
            else:
                scan8 = False


def asteroidLocations(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '#':
                yield (x, y)


def parseInput(path='input10'):
    with open(path) as fh:
        return [line.strip() for line in fh]


class Day10(unittest.TestCase):
    def testPart1(self):
        grid = parseInput('input10')
        self.assertEqual(bestLocation(grid), ((19, 11), 230))

    def testPart2(self):
        grid = parseInput('input10')
        asteroids = list(vaporize(grid))
        x, y = asteroids[199]
        self.assertEqual((x, y), (12, 5))
        self.assertEqual(x * 100 + y, 1205)

    def testDetect1(self):
        grid = parseInput('input10-1')
        detections = [[8, 7, 9, 9, 7],
                      [8, 9, 9, 9, 8],
                      [6, 7, 7, 7, 5],
                      [10, 8, 10, 10, 7],
                      [8, 8, 8, 8, 7]]
        self.assertEqual(detect(grid)[0], detections)

    def testBestLocation1(self):
        grid = parseInput('input10-1')
        self.assertEqual(bestLocation(grid), ((3, 4), 8))

    def testBestLocation2(self):
        grid = parseInput('input10-2')
        self.assertEqual(bestLocation(grid), ((5, 8), 33))

    def testBestLocation3(self):
        grid = parseInput('input10-3')
        self.assertEqual(bestLocation(grid), ((1, 2), 35))

    def testBestLocation4(self):
        grid = parseInput('input10-4')
        self.assertEqual(bestLocation(grid), ((6, 3), 41))

    def testBestLocation5(self):
        grid = parseInput('input10-5')
        self.assertEqual(bestLocation(grid), ((11, 13), 210))

    def testVaporized5(self):
        grid = parseInput('input10-5')
        asteroids = list(vaporize(grid))
        self.assertEqual(len(asteroids), 299)
        self.assertEqual(asteroids[0], (11, 12))
        self.assertEqual(asteroids[1], (12, 1))
        self.assertEqual(asteroids[2], (12, 2))
        self.assertEqual(asteroids[9], (12, 8))
        self.assertEqual(asteroids[19], (16, 0))
        self.assertEqual(asteroids[49], (16, 9))
        self.assertEqual(asteroids[99], (10, 16))
        self.assertEqual(asteroids[198], (9, 6))
        self.assertEqual(asteroids[199], (8, 2))
        self.assertEqual(asteroids[200], (10, 9))
        self.assertEqual(asteroids[298], (11, 1))

    def testVaporize6(self):
        grid = parseInput('input10-6')
        asteroids = [(8, 1), (9, 0), (9, 1), (10, 0), (9, 2), (11, 1), (12, 1), (11, 2), (15, 1),
                     (12, 2), (13, 2), (14, 2), (15, 2), (12, 3), (16, 4), (15, 4), (10, 4), (4, 4),
                     (2, 4), (2, 3), (0, 2), (1, 2), (0, 1), (1, 1), (5, 2), (1, 0), (5, 1),
                     (6, 1), (6, 0), (7, 0), (8, 0), (10, 1), (14, 0), (16, 1), (13, 3), (14, 3)]
        self.assertEqual(list(vaporize(grid, (8, 3))), asteroids)


if __name__ == '__main__':
    unittest.main()
