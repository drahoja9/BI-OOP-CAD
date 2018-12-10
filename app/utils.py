class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '[' + str(self.x) + ', ' + str(self.y) + ']'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            # Calling __init__ of given class even though we return the same instance
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
