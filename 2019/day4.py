import unittest


def isPassword(n, start, end, strictDoubles=False):
    def isDouble(count):
        return (strictDoubles and count == 2) or (not strictDoubles and count >= 2)

    if n < start or n > end:
        return False

    digits = [int(d) for d in str(n)]

    count = 1
    doubles = 0

    for i in range(1, len(digits)):
        if digits[i] < digits[i - 1]:
            return False
        if digits[i] == digits[i - 1]:
            count += 1
            if i == len(digits) - 1 and isDouble(count):
                doubles += 1
        else:
            if isDouble(count):
                doubles += 1
            count = 1

    return doubles > 0


def countPasswords(start, end, strictDoubles=False):
    count = 0

    for n in range(start, end + 1):
        if isPassword(n, start, end, strictDoubles):
            count += 1

    return count


class Day4(unittest.TestCase):
    def testPart1(self):
        self.assertEqual(countPasswords(264793, 803935, strictDoubles=False), 966)

    def testPart2(self):
        self.assertEqual(countPasswords(264793, 803935, strictDoubles=True), 628)


if __name__ == '__main__':
    unittest.main()
