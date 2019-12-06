import unittest
from collections import Counter, defaultdict, deque

def countOrbits(adj, start):
    orbits = Counter()
    Q = [start]
    while len(Q) > 0:
        u = Q.pop()
        for v in adj[u]:
            orbits[v] += orbits[u] + 1
            Q.append(v)
    return sum(orbits.values())

def countTransfers(adj, start, end):
    visited = set()
    Q = deque([(start, 0)])
    while len(Q) > 0:
        u, dist = Q.popleft()
        if u == end:
            return dist - 2 # no transfers between first/last orbits
        if u not in visited:
            visited.add(u)
            Q.extend((v, dist + 1) for v in adj[u])

def parseMap(path='input6', directed=True):
    adj = defaultdict(set)
    with open(path) as fh:
        for line in fh:
            u, v = line.strip().split(')')
            adj[u].add(v)
            if not directed:
                adj[v].add(u)
    return adj

class Day6(unittest.TestCase):
    def testPart1(self):
        adj = parseMap(directed=True)
        self.assertEqual(countOrbits(adj, 'COM'), 194721)

    def testPart2(self):
        adj = parseMap(directed=False)
        self.assertEqual(countTransfers(adj, 'YOU', 'SAN'), 316)

if __name__ == '__main__':
    unittest.main()
