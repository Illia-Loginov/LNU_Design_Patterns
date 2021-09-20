from abc import ABCMeta, abstractmethod
import math


class Shape(metaclass=ABCMeta):
    def __init__(self, color: str = 'red', filled: bool = True) -> None:
        self._color = color
        self._filled = filled

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value

    @property
    def filled(self) -> bool:
        return self._filled

    @filled.setter
    def filled(self, value: bool) -> None:
        self._filled = value

    @abstractmethod
    def get_area(self) -> float:
        pass

    @abstractmethod
    def get_perimeter(self) -> float:
        pass

    def __str__(self) -> str:
        return f'Shape[color={self._color}, filled={self._filled}]'


class Circle(Shape):
    def __init__(self, radius: float = 1.0, color: str = 'red', filled: bool = True) -> None:
        super().__init__(color, filled)
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        self._radius = value

    def get_area(self) -> float:
        return math.pi * self._radius * self._radius

    def get_perimeter(self) -> float:
        return 2 * math.pi * self._radius

    def __str__(self) -> str:
        return f'Circle[Shape[color={self._color}, filled={self._filled}], radius={self._radius}]'


class Rectangle(Shape):
    def __init__(self, width: float = 1.0, length: float = 1.0, color: str = 'red', filled: bool = True) -> None:
        super().__init__(color, filled)
        self._width = width
        self._length = length

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, value: float) -> None:
        self._length = value

    def get_area(self) -> float:
        return self._width * self._length

    def get_perimeter(self) -> float:
        return 2 * (self._width + self._length)

    def __str__(self) -> str:
        return f'Rectangle[Shape[color={self._color}, filled={self._filled}]' \
               f', width={self._width}, length={self._length}]'


class Square(Rectangle):
    def __init__(self, side: float = 1.0, color: str = 'red', filled: bool = True) -> None:
        super().__init__(side, side, color, filled)

    @property
    def side(self) -> float:
        return self._width

    @side.setter
    def side(self, value: float) -> None:
        self._width = value
        self._length = value

    @Rectangle.width.setter
    def width(self, value) -> None:
        self._width = value
        self._length = value

    @Rectangle.length.setter
    def length(self, value) -> None:
        self._width = value
        self._length = value

    def __str__(self):
        return f'Square[Rectangle[Shape[color={self._color}, filled={self._filled}]' \
            f', width={self._width}, length={self._length}]]'

