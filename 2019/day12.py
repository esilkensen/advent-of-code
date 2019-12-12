import re
import unittest


def step(positions, velocities):
    for i in range(len(positions)):
        x1, y1, z1 = positions[i]
        for j in range(i + 1, len(positions)):
            x2, y2, z2 = positions[j]
            dx = -1 if x1 > x2 else 1 if x1 < x2 else 0
            dy = -1 if y1 > y2 else 1 if y1 < y2 else 0
            dz = -1 if z1 > z2 else 1 if z1 < z2 else 0
            velocities[i] = [velocities[i][0] + dx, velocities[i][1] + dy, velocities[i][2] + dz]
            velocities[j] = [velocities[j][0] - dx, velocities[j][1] - dy, velocities[j][2] - dz]

    for i in range(len(positions)):
        positions[i] = [positions[i][j] + velocities[i][j] for j in range(len(positions[i]))]


def snapshot(positions, velocities):
    states = []
    for d in range(3):
        states.append(''.join(str(p[d]) for p in positions) + ''.join(str(v[d]) for v in velocities))
    return states


def totalEnergy(position, velocity):
    return sum(abs(p) for p in position) * sum(abs(v) for v in velocity)


def parseInput(path='input12'):
    with open(path) as fh:
        positions, velocities = [], []
        for line in fh:
            match = re.search('^<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>$', line.strip())
            x, y, z = int(match.group(1)), int(match.group(2)), int(match.group(3))
            positions.append([x, y, z])
            velocities.append([0, 0, 0])
        return positions, velocities


def totalEnergyAfter(positions, velocities, n):
    for i in range(n):
        step(positions, velocities)
    return sum(totalEnergy(positions[i], velocities[i]) for i in range(len(positions)))


def findCycle(positions, velocities):
    cycles = [None, None, None]
    allStates = [set(), set(), set()]
    states = snapshot(positions, velocities)
    while None in cycles:
        for i in range(len(cycles)):
            if cycles[i] is None and states[i] in allStates[i]:
                cycles[i] = len(allStates[i])
            allStates[i].add(states[i])
        step(positions, velocities)
        states = snapshot(positions, velocities)
    return lcm3(cycles[0], cycles[1], cycles[2])


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def lcm3(a, b, c):
    return lcm(a, lcm(b, c))


class Day12(unittest.TestCase):
    def testPart1(self):
        positions, velocities = parseInput('input12')
        self.assertEqual(totalEnergyAfter(positions, velocities, 1000), 10944)

    def testPart2(self):
        positions, velocities = parseInput('input12')
        self.assertEqual(findCycle(positions, velocities), 484244804958744)

    def testEnergy1(self):
        positions, velocities = parseInput('input12-1')
        self.assertEqual(totalEnergyAfter(positions, velocities, 10), 179)

    def testEnergy2(self):
        positions, velocities = parseInput('input12-2')
        self.assertEqual(totalEnergyAfter(positions, velocities, 100), 1940)

    def testCycle1(self):
        positions, velocities = parseInput('input12-1')
        self.assertEqual(findCycle(positions, velocities), 2772)

    def testCycle2(self):
        positions, velocities = parseInput('input12-2')
        self.assertEqual(findCycle(positions, velocities), 4686774924)


if __name__ == '__main__':
    unittest.main()
