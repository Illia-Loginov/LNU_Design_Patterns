import unittest
from task_2 import *


class TestTask2(unittest.TestCase):
    def test_get_area(self):
        polygon1 = Polygon([Point(1, 1), Point(-1, 7), Point(2, 4)])
        polygon2 = Polygon([Point(3, 7), Point(3, 2), Point(2, 1), Point(-9, 8)])
        polygon3 = Polygon([Point(0, 4), Point(5, 1), Point(9, 3), Point(3, 5), Point(2, 8), Point(-5, 3)])

        self.assertAlmostEqual(polygon1.get_area(), 6)
        self.assertAlmostEqual(polygon2.get_area(), 39)
        self.assertAlmostEqual(polygon3.get_area(), 31)

    def test_get_perimeter(self):
        polygon1 = Polygon([Point(1, 1), Point(-1, 7), Point(2, 4)])
        polygon2 = Polygon([Point(3, 7), Point(3, 2), Point(2, 1), Point(-9, 8)])
        polygon3 = Polygon([Point(0, 4), Point(5, 1), Point(9, 3), Point(3, 5), Point(2, 8), Point(-5, 3)])

        self.assertAlmostEqual(polygon1.get_perimeter(), 13.7294737)
        self.assertAlmostEqual(polygon2.get_perimeter(), 31.4942130)
        self.assertAlmostEqual(polygon3.get_perimeter(), 33.4912656)

    def test_get_bottom_left_corner(self):
        rectangle1 = Rectangle([Point(8, 12), Point(15, 12), Point(15, 6), Point(8, 6)])
        rectangle2 = Rectangle([Point(13, 8), Point(19, 8), Point(19, 4), Point(13, 4)])
        rectangle3 = Rectangle([Point(9, 13), Point(12, 13), Point(12, 5), Point(9, 5)])
        rectangle4 = Rectangle([Point(10, 11), Point(14, 11), Point(14, 9), Point(10, 9)])

        self.assertEqual(rectangle1.get_bottom_left_corner(), Point(8, 6))
        self.assertEqual(rectangle2.get_bottom_left_corner(), Point(13, 4))
        self.assertEqual(rectangle3.get_bottom_left_corner(), Point(9, 5))
        self.assertEqual(rectangle4.get_bottom_left_corner(), Point(10, 9))

    def test_get_top_right_corner(self):
        rectangle1 = Rectangle([Point(8, 12), Point(15, 12), Point(15, 6), Point(8, 6)])
        rectangle2 = Rectangle([Point(13, 8), Point(19, 8), Point(19, 4), Point(13, 4)])
        rectangle3 = Rectangle([Point(9, 13), Point(12, 13), Point(12, 5), Point(9, 5)])
        rectangle4 = Rectangle([Point(10, 11), Point(14, 11), Point(14, 9), Point(10, 9)])

        self.assertEqual(rectangle1.get_top_right_corner(), Point(15, 12))
        self.assertEqual(rectangle2.get_top_right_corner(), Point(19, 8))
        self.assertEqual(rectangle3.get_top_right_corner(), Point(12, 13))
        self.assertEqual(rectangle4.get_top_right_corner(), Point(14, 11))

    def test_intersection_area(self):
        rectangle1 = Rectangle([Point(8, 12), Point(15, 12), Point(15, 6), Point(8, 6)])
        rectangle2 = Rectangle([Point(13, 8), Point(19, 8), Point(19, 4), Point(13, 4)])
        rectangle3 = Rectangle([Point(9, 13), Point(12, 13), Point(12, 5), Point(9, 5)])
        rectangle4 = Rectangle([Point(10, 11), Point(14, 11), Point(14, 9), Point(10, 9)])

        self.assertAlmostEqual(rectangle1.intersection_area(rectangle2), 4)
        self.assertAlmostEqual(rectangle1.intersection_area(rectangle3), 18)
        self.assertAlmostEqual(rectangle1.intersection_area(rectangle4), 8)

        self.assertAlmostEqual(rectangle2.intersection_area(rectangle1), 4)
        self.assertAlmostEqual(rectangle2.intersection_area(rectangle3), 0)
        self.assertAlmostEqual(rectangle2.intersection_area(rectangle4), 0)

        self.assertAlmostEqual(rectangle3.intersection_area(rectangle1), 18)
        self.assertAlmostEqual(rectangle3.intersection_area(rectangle2), 0)
        self.assertAlmostEqual(rectangle3.intersection_area(rectangle4), 4)

        self.assertAlmostEqual(rectangle4.intersection_area(rectangle1), 8)
        self.assertAlmostEqual(rectangle4.intersection_area(rectangle2), 0)
        self.assertAlmostEqual(rectangle4.intersection_area(rectangle3), 4)
