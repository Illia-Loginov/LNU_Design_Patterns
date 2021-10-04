from dataclasses import dataclass
from abc import ABC, ABCMeta, abstractmethod


@dataclass
class Customization:
    extra_milk: float
    sugar: float
    mug_size: float


@dataclass
class Preparation:
    milk: float
    water: float
    sugar: float
    coke: float
    liquid_coffee: float
    added_flavour: float
    tea: float


class Product(metaclass=ABCMeta):
    def __init__(self, cust: Customization) -> None:
        self.cust = cust
        self.prep = Preparation(0, 0, 0, 0, 0, 0, 0)
        self.make()

    @abstractmethod
    def make() -> None:
        pass


class Cappuccino(Product):
    def make(self) -> None:
        self.set_milk()
        self.set_sugar()
        self.set_coffee()

    def set_milk(self) -> None:
        self.prep.milk = 0.475

    def set_sugar(self) -> None:
        self.prep.sugar = 0.05

    def set_coffee(self) -> None:
        self.prep.liquid_coffee = 0.475


class BlackCoffee(Product):
    def make(self) -> None:
        self.set_water()
        self.set_coffee()

    def set_water(self) -> None:
        self.prep.water = 0.5

    def set_coffee(self) -> None:
        self.prep.liquid_coffee = 0.5


class Lemonade(Product):
    def make(self) -> None:
        self.set_water()
        self.set_sugar()
        self.set_lemon_juice()

    def set_water(self) -> None:
        self.prep.water = 0.4

    def set_sugar(self) -> None:
        self.prep.sugar = 0.2

    def set_lemon_juice(self) -> None:
        self.prep.added_flavour = 0.4


class HotMilk(Product):
    def make(self) -> None:
        self.set_milk()

    def set_milk(self) -> None:
        self.prep.milk = 1
    

class CocaCola(Product):
    def make(self) -> None:
        self.set_water()
        self.set_coke()

    def set_water(self) -> None:
        self.prep.water = 0.3

    def set_coke(self) -> None:
        self.prep.coke = 0.7


class ProductFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_product(self, customization: Customization) -> Product:
        pass

    @staticmethod
    def get_product_factory(factory_type: str):
        if factory_type == 'Cappuccino':
            return CappuccinoFactory()
        elif factory_type == 'BlackCoffee':
            return BlackCoffeeFactory()
        elif factory_type == 'Lemonade':
            return LemonadeFactory()
        elif factory_type == 'HotMilk':
            return HotMilkFactory()
        elif factory_type == 'CocaCola':
            return CocaColaFactory()
        else:
            return None


class CappuccinoFactory(ProductFactory):
    def get_product(self, customization: Customization) -> Product:
        return Cappuccino(customization)


class BlackCoffeeFactory(ProductFactory):
    def get_product(self, customization: Customization) -> Product:
        return BlackCoffee(customization)


class LemonadeFactory(ProductFactory):
    def get_product(self, customization: Customization) -> Product:
        return Lemonade(customization)


class HotMilkFactory(ProductFactory):
    def get_product(self, customization: Customization) -> Product:
        return HotMilk(customization)


class CocaColaFactory(ProductFactory):
    def get_product(self, customization: Customization) -> Product:
        return CocaCola(customization)


def client(factory_type: str, customization: Customization) -> Product:
    product_factory = ProductFactory.get_product_factory(factory_type)
    if product_factory is not None:
        return product_factory.get_product(customization)
    else:
        return None
