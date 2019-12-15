import unittest


def render(w, h, image):
    layers = getLayers(w, h, image)
    finalImage = [[None for _ in range(w)] for _ in range(h)]
    for i in range(h):
        for j in range(w):
            finalImage[i][j] = finalPixel(i, j, layers)
    return [''.join(row) for row in finalImage]


def finalPixel(i, j, layers):
    for layer in layers:
        if layer[i][j] in '01':
            return 'x' if layer[i][j] == '1' else ' '
    return ' '


def getLayers(w, h, image):
    layers = []
    for i in range(0, len(image), w * h):
        flat = image[i:i+(w*h)]
        layer = []
        for j in range(0, len(flat), w):
            layer.append(flat[j:j+w])
        layers.append(layer)
    return layers


class Day8(unittest.TestCase):
    def setUp(self):
        with open('input8') as fh:
            self.image = fh.readline().strip()

    def testPart1(self):
        minCount, minLayer = float('+inf'), ''
        for layer in getLayers(25, 6, self.image):
            layer = ''.join(layer)
            count = layer.count('0')
            if count < minCount:
                minCount, minLayer = count, layer
        ones, twos = minLayer.count('1'), minLayer.count('2')
        self.assertEqual(ones * twos, 1088)

    def testPart2(self):
        image = ['x     xx  x   xx  x xxx  ',
                 'x    x  x x   xx  x x  x ',
                 'x    x     x x xxxx xxx  ',
                 'x    x xx   x  x  x x  x ',
                 'x    x  x   x  x  x x  x ',
                 'xxxx  xxx   x  x  x xxx  ']
        self.assertEqual(render(25, 6, self.image), image)


if __name__ == '__main__':
    unittest.main()
