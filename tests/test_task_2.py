import unittest
from task_2 import *


class TestTask2(unittest.TestCase):
    def setUp(self) -> None:
        self.circles = [
            Circle(),
            Circle(3.22, 'green'),
            Circle(13.37, 'blue', False)
        ]

        self.rectangles = [
            Rectangle(),
            Rectangle(198.6),
            Rectangle(8.3, 1.7)
        ]

        self.squares = [
            Square(),
            Square(3.14)
        ]

    def test_getters(self) -> None:
        self.assertAlmostEqual(self.circles[0].radius, 1.0)
        self.assertAlmostEqual(self.circles[1].radius, 3.22)
        self.assertAlmostEqual(self.circles[2].radius, 13.37)

        self.assertEqual(self.circles[0].color, 'red')
        self.assertEqual(self.circles[1].color, 'green')
        self.assertEqual(self.circles[2].color, 'blue')

        self.assertTrue(self.circles[0].filled)
        self.assertTrue(self.circles[1].filled)
        self.assertFalse(self.circles[2].filled)

        self.assertAlmostEqual(self.rectangles[0].width, 1.0)
        self.assertAlmostEqual(self.rectangles[0].length, 1.0)
        self.assertAlmostEqual(self.rectangles[1].width, 198.6)
        self.assertAlmostEqual(self.rectangles[1].length, 1.0)
        self.assertAlmostEqual(self.rectangles[2].width, 8.3)
        self.assertAlmostEqual(self.rectangles[2].length, 1.7)

        self.assertAlmostEqual(self.squares[0].side, 1.0)
        self.assertAlmostEqual(self.squares[0].width, 1.0)
        self.assertAlmostEqual(self.squares[0].length, 1.0)
        self.assertAlmostEqual(self.squares[1].side, 3.14)
        self.assertAlmostEqual(self.squares[1].width, 3.14)
        self.assertAlmostEqual(self.squares[1].length, 3.14)

    def test_setters(self) -> None:
        self.circles[0].radius = 1.44
        self.assertAlmostEqual(self.circles[0].radius, 1.44)

        self.circles[0].color = 'black'
        self.assertEqual(self.circles[0].color, 'black')

        self.circles[0].filled = False
        self.assertFalse(self.circles[0].filled)

        self.rectangles[0].width = 1.44
        self.assertAlmostEqual(self.rectangles[0].width, 1.44)

        self.rectangles[0].length = 1.44
        self.assertAlmostEqual(self.rectangles[0].length, 1.44)

        self.squares[0].side = 1.44
        self.assertAlmostEqual(self.squares[0].side, 1.44)
        self.assertAlmostEqual(self.squares[0].width, 1.44)
        self.assertAlmostEqual(self.squares[0].length, 1.44)

        self.squares[0].width = 2.71
        self.assertAlmostEqual(self.squares[0].side, 2.71)
        self.assertAlmostEqual(self.squares[0].width, 2.71)
        self.assertAlmostEqual(self.squares[0].length, 2.71)

        self.squares[0].length = 9.81
        self.assertAlmostEqual(self.squares[0].side, 9.81)
        self.assertAlmostEqual(self.squares[0].width, 9.81)
        self.assertAlmostEqual(self.squares[0].length, 9.81)

    def test_get_area(self) -> None:
        self.assertAlmostEqual(self.circles[0].get_area(), 3.14159265359)
        self.assertAlmostEqual(self.circles[1].get_area(), 32.5732892695)
        self.assertAlmostEqual(self.circles[2].get_area(), 561.581363818)

        self.assertAlmostEqual(self.rectangles[0].get_area(), 1.0)
        self.assertAlmostEqual(self.rectangles[1].get_area(), 198.6)
        self.assertAlmostEqual(self.rectangles[2].get_area(), 14.11)

        self.assertAlmostEqual(self.squares[0].get_area(), 1.0)
        self.assertAlmostEqual(self.squares[1].get_area(), 9.8596)

    def test_get_perimeter(self) -> None:
        self.assertAlmostEqual(self.circles[0].get_perimeter(), 6.28318530718)
        self.assertAlmostEqual(self.circles[1].get_perimeter(), 20.2318566891)
        self.assertAlmostEqual(self.circles[2].get_perimeter(), 84.006187557)

        self.assertAlmostEqual(self.rectangles[0].get_perimeter(), 4)
        self.assertAlmostEqual(self.rectangles[1].get_perimeter(), 399.2)
        self.assertAlmostEqual(self.rectangles[2].get_perimeter(), 20)

        self.assertAlmostEqual(self.squares[0].get_perimeter(), 4)
        self.assertAlmostEqual(self.squares[1].get_perimeter(), 12.56)

    def test_to_string(self) -> None:
        self.assertEqual(str(self.circles[0]), 'Circle[Shape[color=red, filled=True], radius=1.0]')
        self.assertEqual(str(self.circles[1]), 'Circle[Shape[color=green, filled=True], radius=3.22]')
        self.assertEqual(str(self.circles[2]), 'Circle[Shape[color=blue, filled=False], radius=13.37]')

        self.assertEqual(str(self.rectangles[0]), 'Rectangle[Shape[color=red, filled=True], '
                                                  'width=1.0, length=1.0]')
        self.assertEqual(str(self.rectangles[1]), 'Rectangle[Shape[color=red, filled=True], '
                                                  'width=198.6, length=1.0]')
        self.assertEqual(str(self.rectangles[2]), 'Rectangle[Shape[color=red, filled=True], '
                                                  'width=8.3, length=1.7]')

        self.assertEqual(str(self.squares[0]), 'Square[Rectangle[Shape[color=red, filled=True], '
                                               'width=1.0, length=1.0]]')
        self.assertEqual(str(self.squares[1]), 'Square[Rectangle[Shape[color=red, filled=True], '
                                               'width=3.14, length=3.14]]')
