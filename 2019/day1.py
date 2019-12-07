import unittest


def fuelRequired(mass):
    return max(0, mass // 3 - 2)


def totalFuelRequired(mass):
    fuel = fuelRequired(mass)
    if fuel > 0:
        fuel += totalFuelRequired(fuel)
    return fuel


class Day1(unittest.TestCase):
    def setUp(self):
        with open('input1') as fh:
            self.modules = [int(line.strip()) for line in fh]

    def testPart1(self):
        self.assertEqual(sum(fuelRequired(mass) for mass in self.modules), 3502510)

    def testPart2(self):
        self.assertEqual(sum(totalFuelRequired(mass) for mass in self.modules), 5250885)


if __name__ == '__main__':
    unittest.main()
