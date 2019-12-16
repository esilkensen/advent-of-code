import unittest


def phase1(signal, n=1, k=8):
    signal = [int(d) for d in signal]
    for i in range(n):
        signal = fft1(signal)
    return ''.join(str(d) for d in signal[:k])


def fft1(signal):
    pattern = [0, 1, 0, -1]
    nextSignal = ''
    for i in range(len(signal)):
        phase = i + 1
        p, r = 0, 1
        digit = 0
        for j in range(len(signal)):
            n = int(signal[j])
            if r == phase:
                r = 0
                p = (p + 1) % len(pattern)
            digit += n * pattern[p]
            r += 1
        nextSignal += str(abs(digit) % 10)
    return nextSignal


def phase2(signal, n=1, k=8):
    offset = int(signal[:7], 10)
    signal = (signal * 10000)[offset:]
    signal = [int(d) for d in signal]
    for i in range(n):
        signal = fft2(signal)
    return ''.join(str(d) for d in signal[:k])


def fft2(signal):
    s = sum(signal)
    nextSignal = []
    for i in range(len(signal)):
        nextSignal.append(s % 10)
        s -= signal[i]
    return nextSignal


class Day16(unittest.TestCase):
    def setUp(self):
        with open('input16') as fh:
            self.signal = fh.readline().strip()

    def testPart1(self):
        self.assertEqual(phase1(self.signal, 100, 8), '40921727')

    def testPart2(self):
        self.assertEqual(phase2(self.signal, 100), '89950138')

    def testPart1Example(self):
        self.assertEqual(phase1('12345678'), '48226158')
        self.assertEqual(phase1('48226158'), '34040438')
        self.assertEqual(phase1('34040438'), '03415518')
        self.assertEqual(phase1('03415518'), '01029498')

    def testPart1Larger(self):
        self.assertEqual(phase1('80871224585914546619083218645595', 100), '24176176')
        self.assertEqual(phase1('19617804207202209144916044189917', 100), '73745418')
        self.assertEqual(phase1('69317163492948606335995924319873', 100), '52432133')

    def testPart2Larger(self):
        self.assertEqual(phase2('03036732577212944063491565474664', 100), '84462026')
        self.assertEqual(phase2('02935109699940807407585447034323', 100), '78725270')
        self.assertEqual(phase2('03081770884921959731165446850517', 100), '53553731')


if __name__ == '__main__':
    unittest.main()
