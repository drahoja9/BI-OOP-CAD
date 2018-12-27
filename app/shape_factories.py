from app.shapes import *


class ShapeFactory:
    def __init__(self, shape: Shape):
        self._shape = shape

    def get_shape(self):
        return self._shape


"--------------- Rectangle ---------------"


class DimensionsRectFactory(ShapeFactory):
    def __init__(self, **kwargs):
        start_point_x = kwargs['start_point_x']
        start_point_y = kwargs['start_point_y']
        width = kwargs['width']
        height = kwargs['height']
        color = kwargs['color']

        rectangle = Rectangle(
            Point(start_point_x, start_point_y),
            width,
            height,
            Color(*color)
        )
        super().__init__(rectangle)


class PointsRectFactory(ShapeFactory):
    def __init__(self, **kwargs):
        start_point_x = kwargs['start_point_x']
        start_point_y = kwargs['start_point_y']
        end_point_x = kwargs['end_point_x']
        end_point_y = kwargs['end_point_y']
        color = kwargs['color']

        width = abs(start_point_x - end_point_x)
        height = abs(start_point_y - end_point_y)
        rectangle = Rectangle(
            Point(min(start_point_x, end_point_x), min(start_point_y, end_point_y)),
            width,
            height,
            Color(*color)
        )
        super().__init__(rectangle)


"--------------- Circle ---------------"


class DimensionsCircleFactory(ShapeFactory):
    def __init__(self, **kwargs):
        center_x = kwargs['center_x']
        center_y = kwargs['center_y']
        radius = kwargs['radius']
        color = kwargs['color']

        center = (center_x, center_y)
        circle = Circle(
            Point(*center),
            int(radius),
            Color(*color)
        )
        super().__init__(circle)


class PointsCircleFactory(ShapeFactory):
    def __init__(self, **kwargs):
        start_point_x = kwargs['start_point_x']
        start_point_y = kwargs['start_point_y']
        end_point_x = kwargs['end_point_x']
        end_point_y = kwargs['end_point_y']
        color = kwargs['color']

        center = (start_point_x, start_point_y)
        radius = distance(Point(*center), Point(end_point_x, end_point_y))
        circle = Circle(
            Point(*center),
            int(radius),
            Color(*color)
        )
        super().__init__(circle)
