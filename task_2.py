import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Shape:
    pass


class Polygon(Shape):
    def __init__(self, points):
        self.points = points

    def get_area(self):
        area = 0
        for i in range(len(self.points) - 1):
            area += (self.points[i + 1].x - self.points[i].x) * (self.points[i + 1].y + self.points[i].y) * 0.5
        area += (self.points[0].x - self.points[len(self.points) - 1].x) * (self.points[0].y + self.points[len(self.points) - 1].y) * 0.5

        if area < 0:
            return -1 * area
        else:
            return area

    def get_perimeter(self):
        perimeter = 0
        for i in range(len(self.points) - 1):
            perimeter += math.sqrt((self.points[i + 1].x - self.points[i].x) * (self.points[i + 1].x - self.points[i].x) + (self.points[i + 1].y - self.points[i].y) * (self.points[i + 1].y - self.points[i].y))
        perimeter += math.sqrt((self.points[0].x - self.points[len(self.points) - 1].x) * (self.points[0].x - self.points[len(self.points) - 1].x) + (self.points[0].y - self.points[len(self.points) - 1].y) * (self.points[0].y - self.points[len(self.points) - 1].y))
        return perimeter


class Triangle(Polygon):
    def __init__(self, points):
        super().__init__(points[0:3])


class Rectangle(Polygon):
    def __init__(self, points):
        super().__init__(points[0:4])

    def get_bottom_left_corner(self):
        blc = self.points[0]
        for point in self.points:
            if point.x <= blc.x and point.y <= blc.y:
                blc = point
        return blc

    def get_top_right_corner(self):
        trc = self.points[0]
        for point in self.points:
            if point.x >= trc.x and point.y >= trc.y:
                trc = point
        return trc

    def intersection_area(self, second_rectangle):
        r1 = [self.get_bottom_left_corner(), self.get_top_right_corner()]
        r2 = [second_rectangle.get_bottom_left_corner(), second_rectangle.get_top_right_corner()]

        if r1[0].x <= r2[0].x <= r1[1].x:
            left = r2[0].x
        elif r2[0].x <= r1[0].x <= r2[1].x:
            left = r1[0].x
        else:
            return 0

        if r1[0].x <= r2[1].x <= r1[1].x:
            right = r2[1].x
        elif r2[0].x <= r1[1].x <= r2[1].x:
            right = r1[1].x
        else:
            return 0

        if r1[0].y <= r2[0].y <= r1[1].y:
            bottom = r2[0].y
        elif r2[0].y <= r1[0].y <= r2[1].y:
            bottom = r1[0].y
        else:
            return 0

        if r1[0].y <= r2[1].y <= r1[1].y:
            top = r2[1].y
        elif r2[0].y <= r1[1].y <= r2[1].y:
            top = r1[1].y
        else:
            return 0

        return (right - left) * (top - bottom)
