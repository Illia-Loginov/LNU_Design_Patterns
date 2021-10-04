import unittest
from task_2 import *


class TestTask2(unittest.TestCase):
    def setUp(self) -> None:
        self.customization = Customization(0.1, 0.05, 1.5)

    def test_get_product_factory(self) -> None:
        self.assertEqual(type(ProductFactory.get_product_factory('Cappuccino')), type(CappuccinoFactory()))
        self.assertEqual(type(ProductFactory.get_product_factory('BlackCoffee')), type(BlackCoffeeFactory()))
        self.assertEqual(type(ProductFactory.get_product_factory('Lemonade')), type(LemonadeFactory()))
        self.assertEqual(type(ProductFactory.get_product_factory('HotMilk')), type(HotMilkFactory()))
        self.assertEqual(type(ProductFactory.get_product_factory('CocaCola')), type(CocaColaFactory()))
        self.assertEqual(type(ProductFactory.get_product_factory('Lorem Ipsum')), type(None))

    def test_get_product(self) -> None:
        preparations = [
            Preparation(0.475, 0, 0.05, 0, 0.475, 0, 0),
            Preparation(0, 0.5, 0, 0, 0.5, 0, 0),
            Preparation(0, 0.4, 0.2, 0, 0, 0.4, 0),
            Preparation(1, 0, 0, 0, 0, 0, 0),
            Preparation(0, 0.3, 0, 0.7, 0, 0, 0),
        ]

        self.assertEqual(CappuccinoFactory().get_product(self.customization).prep, preparations[0])
        self.assertEqual(BlackCoffeeFactory().get_product(self.customization).prep, preparations[1])
        self.assertEqual(LemonadeFactory().get_product(self.customization).prep, preparations[2])
        self.assertEqual(HotMilkFactory().get_product(self.customization).prep, preparations[3])
        self.assertEqual(CocaColaFactory().get_product(self.customization).prep, preparations[4])

    def test_client(self) -> None:
        self.assertEqual(type(client('Cappuccino', self.customization)), type(Cappuccino(self.customization)))
        self.assertEqual(type(client('BlackCoffee', self.customization)), type(BlackCoffee(self.customization)))
        self.assertEqual(type(client('Lemonade', self.customization)), type(Lemonade(self.customization)))
        self.assertEqual(type(client('HotMilk', self.customization)), type(HotMilk(self.customization)))
        self.assertEqual(type(client('CocaCola', self.customization)), type(CocaCola(self.customization)))
        self.assertEqual(type(client('Lorem Ipsum', self.customization)), type(None))