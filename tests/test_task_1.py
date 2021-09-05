import unittest
from task_1 import *


class TestTask1(unittest.TestCase):
    def test_authorized(self):
        check = Check(322, 'Mobile Top-Up', '1337')
        credit = Credit(720, '0451', 'Standard', '04.09.2023')

        self.assertTrue(check.authorized())
        self.assertTrue(credit.authorized())

    def test_get_tax(self):
        item1 = Item(0.2, 'Bottle')
        item2 = Item(3, 'Vase')
        item3 = Item(10, 'Dumbbell')

        self.assertAlmostEqual(item1.get_tax(), 0.0004)
        self.assertAlmostEqual(item2.get_tax(), 0.006)
        self.assertAlmostEqual(item3.get_tax(), 0.02)

    def test_get_price(self):
        item1 = Item(0.2, 'Bottle')
        item2 = Item(3, 'Vase')
        item3 = Item(10, 'Dumbbell')

        self.assertAlmostEqual(item1.get_price(), 12)
        self.assertAlmostEqual(item2.get_price(), 180)
        self.assertAlmostEqual(item3.get_price(), 600)

    def test_calc_tax(self):
        order1 = Order('04.09.2021', 'Being delivered', 5, 'Paid', Item(0.2, 'Bottle'))
        order2 = Order('13.08.2021', 'Delivered', 3, 'Paid', Item(3, 'Vase'))
        order3 = Order('04.09.2021', 'Stored in a warehouse', 2, 'Paid', Item(10, 'Dumbbell'))

        self.assertAlmostEqual(order1.calc_tax().amount, 0.024)
        self.assertAlmostEqual(order2.calc_tax().amount, 3.24)
        self.assertAlmostEqual(order3.calc_tax().amount, 24)

    def test_calc_total(self):
        order1 = Order('04.09.2021', 'Being delivered', 5, 'Paid', Item(0.2, 'Bottle'))
        order2 = Order('13.08.2021', 'Delivered', 3, 'Paid', Item(3, 'Vase'))
        order3 = Order('04.09.2021', 'Stored in a warehouse', 2, 'Paid', Item(10, 'Dumbbell'))

        self.assertAlmostEqual(order1.calc_total().amount, 60.024)
        self.assertAlmostEqual(order2.calc_total().amount, 543.24)
        self.assertAlmostEqual(order3.calc_total().amount, 1224)
